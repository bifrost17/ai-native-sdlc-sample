#!/usr/bin/env python3
"""L14 1032: "at 2σ it invokes Claude read-only to diagnose, and at 3σ
Claude may act, though only by opening a PR into the review gate or triggering
a pre-approved runbook."

모델은 저장소를 Read/Grep만 할 수 있고 stdout으로 진단 JSON을 돌려준다. 파일 기록과
intent 생성은 이 결정론 실행기가 맡는다. 승인·코드 변경·PR 생성 권한은 주지 않는다.
"""
import argparse
import json
import os
import subprocess
import sys


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_EMITTER = os.path.join(os.path.dirname(__file__), "emit_intent.py")
TIERS = ("none", "1sigma", "2sigma", "3sigma")
READ_TOOLS = "Read,Grep"


class RunError(Exception):
    """사용자에게 설명하고 비0으로 끝낼 실행 오류."""


class DiagnosisError(RunError):
    """모델 프로세스는 끝났지만 진단 계약을 읽을 수 없는 오류."""


class ArtifactError(RunError):
    """모델 결과 파일을 보존할 수 없는 오류."""


def write_text(path, text):
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def write_json(path, data):
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def save_record(path, record):
    try:
        write_json(path, record)
    except OSError as exc:
        raise RunError("실행 기록을 쓸 수 없다: %s (%s)" % (path, exc))


def load_detection(path):
    try:
        data = json.loads(open(path, encoding="utf-8").read())
    except (OSError, ValueError) as exc:
        raise RunError("탐지 결과를 읽을 수 없다: %s (%s)" % (path, exc))
    if not isinstance(data, dict) or data.get("tier") not in TIERS:
        raise RunError("detect_bands.py 출력이 아니다: tier 필드 없음/모름")
    return data


def parse_diagnosis(raw):
    try:
        envelope = json.loads(raw)
        if not isinstance(envelope, dict):
            raise DiagnosisError("Claude JSON envelope가 객체가 아니다")
        if envelope.get("is_error") is True:
            raise RunError("Claude가 오류 결과를 반환했다: %s" % envelope.get("subtype", "unknown"))
        result = envelope["result"]
        diagnosis = json.loads(result) if isinstance(result, str) else result
    except (ValueError, KeyError, TypeError) as exc:
        raise DiagnosisError("모델 진단 산출물이 약속한 JSON이 아니다: %s" % exc)
    if not isinstance(diagnosis, dict) or not isinstance(diagnosis.get("evidence"), str):
        raise DiagnosisError("모델 진단에 evidence 문자열이 없다")
    questions = diagnosis.get("open_questions")
    if not isinstance(questions, list) or not all(isinstance(x, str) for x in questions):
        raise DiagnosisError("모델 진단에 open_questions 문자열 배열이 없다")
    return {"evidence": diagnosis["evidence"], "open_questions": questions}


def prompt_for(input_path, tier):
    authority = (
        "This is a 2sigma read-only diagnosis. Do not propose code changes or a pull request."
        if tier == "2sigma" else
        "This is a 3sigma diagnosis for a proposal draft. Do not change code or open a pull request."
    )
    return (
        "Read the band detection JSON at %s and inspect this repository read-only. %s "
        "Return only a JSON object with exactly these fields: "
        "{\"evidence\": \"concise repository-grounded diagnosis\", "
        "\"open_questions\": [\"question\"]}. Do not use Markdown fences."
        % (os.path.abspath(input_path), authority)
    )


def run_model(claude, input_path, tier, out_dir):
    cmd = [claude, "--tools", READ_TOOLS, "--allowedTools", READ_TOOLS,
           "--output-format", "json", "-p", prompt_for(input_path, tier)]
    try:
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    except OSError as exc:
        try:
            write_text(os.path.join(out_dir, "model-error.txt"), str(exc) + "\n")
        except OSError:
            pass
        raise RunError("모델을 실행할 수 없다: %s" % exc)
    try:
        write_text(os.path.join(out_dir, "model-output.json"), proc.stdout)
        write_text(os.path.join(out_dir, "model-error.txt"), proc.stderr)
    except OSError as exc:
        raise ArtifactError("모델 실행 기록을 쓸 수 없다: %s" % exc)
    if proc.returncode != 0:
        raise RunError("모델 실행 실패(rc=%d)" % proc.returncode)
    return parse_diagnosis(proc.stdout)


def emit(emitter, input_path, diagnosis_path, intent_id, out_dir):
    cmd = [sys.executable, emitter, "--input", input_path, "--id", intent_id,
           "--out", out_dir, "--diagnosis", diagnosis_path]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if proc.returncode != 0:
        write_text(os.path.join(out_dir, "draft-error.txt"), proc.stderr)
        raise RunError("intent 초안 생성 실패(rc=%d)" % proc.returncode)
    return os.path.join(out_dir, intent_id, "intent.md")


def main(argv=None):
    parser = argparse.ArgumentParser(description="bands tier 실행기")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--id", required=True, dest="intent_id")
    parser.add_argument("--claude", default="claude")
    parser.add_argument("--emit-script", default=DEFAULT_EMITTER)
    args = parser.parse_args(argv)

    try:
        os.makedirs(args.out, exist_ok=True)
    except OSError as exc:
        sys.stderr.write("실행 기록 디렉터리를 만들 수 없다: %s (%s)\n" % (args.out, exc))
        return 2
    record_path = os.path.join(args.out, "run.json")
    try:
        data = load_detection(args.input)
        tier = data["tier"]
        record = {"schema_version": 1, "tier": tier, "action": data.get("action"),
                  "detected_at": data.get("detected_at")}
        if tier in ("none", "1sigma"):
            record.update({"status": "recorded", "model": "not_required"})
            save_record(record_path, record)
            print(json.dumps(record, ensure_ascii=False))
            return 0

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            record["model"] = "skipped_no_api_key"
            if tier == "2sigma":
                record["status"] = "diagnosis_skipped"
                save_record(record_path, record)
                print(json.dumps(record, ensure_ascii=False))
                return 0
            diagnosis = {
                "evidence": "모델 진단 미실행: ANTHROPIC_API_KEY가 설정되지 않았다.",
                "open_questions": ["API key가 있는 실행에서 저장소 근거를 확인해야 한다."],
            }
        else:
            record["model"] = "running"
            save_record(record_path, record)
            try:
                diagnosis = run_model(args.claude, args.input, tier, args.out)
            except ArtifactError as exc:
                record["status"] = "model_artifact_write_failed"
                record["model"] = "failed"
                record["error"] = str(exc)
                save_record(record_path, record)
                sys.stderr.write(str(exc) + "\n")
                return 2
            except DiagnosisError as exc:
                record["status"] = "diagnosis_invalid"
                record["model"] = "invalid_output"
                record["error"] = str(exc)
                save_record(record_path, record)
                sys.stderr.write(str(exc) + "\n")
                return 3
            except RunError as exc:
                record["status"] = "model_failed"
                record["model"] = "failed"
                record["error"] = str(exc)
                save_record(record_path, record)
                sys.stderr.write(str(exc) + "\n")
                return 3

        diagnosis_path = os.path.join(args.out, "diagnosis.json")
        try:
            write_json(diagnosis_path, diagnosis)
        except OSError as exc:
            record.update({"status": "diagnosis_write_failed", "error": str(exc)})
            save_record(record_path, record)
            sys.stderr.write("진단 산출물을 쓸 수 없다: %s\n" % exc)
            return 2
        try:
            intent_path = emit(args.emit_script, args.input, diagnosis_path,
                               args.intent_id, args.out)
        except (RunError, OSError) as exc:
            record.update({"status": "draft_failed", "error": str(exc)})
            save_record(record_path, record)
            sys.stderr.write(str(exc) + "\n")
            return 4
        record.update({"status": "diagnosed" if tier == "2sigma" else "proposal_drafted",
                       "intent": intent_path})
        if tier == "3sigma" and "routes" in data:
            record["routes"] = data["routes"]
        if api_key:
            record["model"] = "completed"
        save_record(record_path, record)
        print(json.dumps(record, ensure_ascii=False))
        return 0
    except RunError as exc:
        sys.stderr.write(str(exc) + "\n")
        return 2
    except OSError as exc:
        sys.stderr.write("bands 실행 기록 오류: %s\n" % exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
