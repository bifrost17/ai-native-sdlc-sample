# 0027 독립 최종 검토

2026-09-15. 기준 `b9af49ac0627183db7607f2efaf6549c7e767c40`, 검토 HEAD
`79dedb88b155b414cd02eb2df1db695329d63efa`와 당시 작업 사본 전체.
브랜치는 `codex/single-template-skill-parity`다. main은 기준 코드와 같았다.
추적 변경, 미추적 Claude 안내·Codex patch·설치 근거·단일 템플릿 결정문을 포함했다.
리뷰 중 root가 마친 `docs/experiments/README.md`와 실행 README 정정도 읽었다.

중요한 발견은 없다. T01–T03의 구현·설치 전달 범위는 현재 intent/spec/plan과 맞는다.
이 보고서는 개발자에게 반환하는 검토 결과이며 사람의 수락이나 Git 통합을 대신하지 않는다.

## What ran

`CLAUDE.md`, `.claude/agents/verifier.md`, `REVIEW.md`,
`tdd-optional/org-skills/agents/sdlc-verifier.md`의 Review criteria와 0027의
intent/spec/plan·실행 기록을 읽었다. 북극성 색인과 V6-04(스킬 본문·호출),
V8-02/04(작업 중 검증과 독립 최종 확인)를 대조했다. 현재 배포 안내 추가가 과거 행동 판정을
승격하지 않는지 확인했다.

다음 명령을 실행했다.

```text
make check
exit=0

claude plugin validate --strict .claude-plugin/marketplace.json
exit=0
claude plugin validate --strict tdd-optional/.claude-plugin/marketplace.json
exit=0
claude plugin validate --strict tdd-optional/org-skills
exit=0

git diff --check b9af49a
exit=0 (초기 추적 변경만; 당시 미추적 patch는 이 명령에 포함되지 않음)
git diff --cached --check
exit=2 (root가 새 patch를 stage한 뒤 마지막 확인; 아래 기록 참조)
git diff --name-only 00fd7334 b9af49a
exit=0
git rev-parse HEAD main
exit=0
```

추가 Python 관측은 새 임시 제품에서 Codex README의 bash 블록을 추출해 경로만 바꿔 실행했다.
원본 제품 파일과 동반 자료를 비교하고 재설치 중단, 명시 사용 설정을 확인했다.
설치 기록의 실제 경로를 다시 읽어 source/Claude/Codex/OpenCode의 240파일 해시를 대조했다.
훅에는 `INTENT_TASK=fix`와 테스트 파일 Edit JSON을 stdin으로 전달했다.
이 입력은 훅 판단용이며 실제 Edit나 테스트 파일 쓰기를 실행하지 않았다.
폐기 판에는 `SDLC_EDITION=tdd-first`로 `bash evals/run.sh`를 호출했다.
실제 실행한 관측 코드는 아래에 보존했다.

## What was observed

`make check`의 출력 전체를 읽었고 실패는 없었다. 결과 발췌:

```text
Ran 103 tests in 29.176s

OK (skipped=1)
test_hooks: 28 passed, 0 failed
8 passed, 0 failed
org/managed-settings.example.json 키 11개 전부 공식 목록 안
PASS  managed-settings 키·훅 계약
```

세 manifest 검사 모두 `✔ Validation passed`였다. 독립 추가 관측 출력:

```text
Evidence rehash: 16 skills x source/Claude/Codex/OpenCode; 240 files identical to recorded hashes
Fresh Codex README install rc=0; all four patches applied
Fresh Codex: 16 folders, companion bytes, four explicit-only policies, original product files preserved; repeat rc=1
Controlled hook rc=2: [protect-tests.sh] BLOCKED: tests/test_template_editions.py is a test file and INTENT_TASK=fix. Reason: the failing test committed before the fix is the proof the bug is gone; if the fix can rewrite it, it proves nothing. Route: fix the code, not the test. If the test itself is wrong, that is a separate task — start a session without INTENT_TASK=fix and say so in the PR.
Retired edition rc=2: UNDECIDABLE: invalid SDLC_EDITION: tdd-first (expected tdd-optional)
Review criteria: Claude=OpenCode; Codex identical after declared AGENTS.md entry normalization
Previous chain 0026 own diff: 83 files, listed package/authoring/policy/evidence families; old records unchanged in 0027
```

추가 기준 비교의 첫 시도는 검토자가 TOML의 끝 구분자를 `"""`로 잘못 예상해
`AssertionError`로 종료했다. 실제 파일의 `'''`를 확인해 관측 코드만 바로잡았다.
직접 diff에서 확인한 본문 차이는 Codex의 프로젝트 진입 목록에 추가한 `AGENTS.md`뿐이었다.
구현이나 검토 기준을 검사에 맞춰 변경하지 않았다.

보고서 작성 중 root가 구현을 stage한 뒤 전체 whitespace 검사에서는 새
`tdd-optional/org-skills/codex/patches/pr-loop.patch`의 빈 context 줄을 경고했다.
첫 출력은 `tdd-optional/org-skills/codex/patches/pr-loop.patch:13: trailing whitespace.`이며,
13·15·24·33·35행과 마지막 빈 줄만 대상이다. unified diff의 빈 context 줄에 필요한
한 칸과 끝 빈 줄이므로 설치 실패나 의미 변경으로 보지 않는다. 전체 staged whitespace 검사가
깨끗하다고 보고하지 않는다. 이 patch의 실제 적용은 새 임시 설치에서 통과했다.

## What does not match plan.md

없음. 실제 변경을 다음 범위로 대조했다.

- T01 / SP01 / FR01·NFR01: 추적 기본형 133파일 삭제, 단일 marketplace 항목,
  루트 작성 라우터·현재 채택 안내 정리. 폐기한 경로의 과거 기록은 Git 기준판을 안내하며 남아 있다.
- T02 / SP01·03 / FR03·AC01: 평가 생성·채점·기록의 기본값과 허용 판을 선택형으로 맞췄다.
  거부 사례와 fake CLI 회귀는 모델 호출 이전 거부, 현재 제품·플러그인·출력 경로를 확인한다.
  두 판 동등성 검사 삭제는 폐기된 대상 제거이며, 남은 판의 자료 격리와 실패 분기 검사는 유지했다.
- T03 / SP02·03 / FR02·NFR02: 공통 작성 3개·팀 13개, 전체 참고 자료와 명시 전용 4개를
  보존한다. Claude는 팀 플러그인과 프로젝트 작성 폴더를 구분한다. Codex의 새 PR patch는
  입력·선실행 문법을 변환하고 `Team settings` 이후의 작업·보호·종료 규칙을 보존한다.
  검증 전략과 TDD 선택 지침·프로젝트 정책 우선순위는 변경되지 않았다.
- AC03·04: 제공된 실제 격리 Claude 설치/list, Codex 설치/검사, OpenCode patch 근거를 읽고
  현존 파일 해시를 다시 대조했다. 새 Codex 설치·충돌 중단은 별도 임시 제품에서 재실행했다.
  전역 사용자 설치나 기존 제품을 바꾸는 작업은 수행하지 않았다.

Bugs, Security, Compliance 패스에서 이 범위의 중요한 차이를 발견하지 못했다.
새 endpoint·로그 필드·인증 경계나 의미 검사기는 없다. 기존 훅의 통제 범위를 유지한다.
직전 0026 계획은 자기 기준 `00fd7334..b9af49a`의 83파일 변경과 대조했고,
양 판의 작성·정책·패키지·인계 근거라는 계획 범위에 맞았다.
0027이 그 과거 intent·실행 근거를 다시 쓰지 않은 것도 확인했다.

## What could not be checked

전체 103시험 중 기존 1건 skip은 이번 결과에도 남는다. fake CLI 평가와 manifest/설치 검사는
실제 모델의 자연 스킬 선택·본문 적용·검증자 위임과 대기를 증명하지 않는다.
0.1.8의 실제 모델 턴, hosted PR 변경, 전체 제품 개발이나 장기 운영은 실행하지 않았다.
이 한계는 현재 문서와 설치 기록에도 명시돼 있으며 이번 사용자 요청의 필수 실행 범위가 아니다.

Claude 프로젝트 플러그인 설치는 작업자가 남긴 CLI 원본과 실제 캐시를 검증했고,
검토자가 별도 Claude 설치를 한 번 더 실행하지는 않았다.
OpenCode도 실제 모델 실행 없이 제공 patch 결과·원본 자료·검토 기준을 대조했다.
새 Codex 임시 설치와 maker 회귀는 이 검토자가 직접 실행했다.

검토 시점 main은 기준 코드 그대로여서 추가 upstream 변경과의 충돌은 없었다.
후속 구현 커밋과 main fast-forward 결과는 아직 없으므로 root가 통합 뒤 확인해야 한다.
초기 문서 커밋 순서는 Git에서 확인했지만, 모든 미커밋 내부 수정의 시간 순서를
최종 파일만으로 추정하지 않았다. 본 검토는 코드를 수정·커밋·push하거나 인수를 승인하지 않았다.

## Independent observation commands

첫 관측은 다음 Python 본문을 `python3 -c`의 인자로 실행했다(종료 코드 0).

```python
import hashlib,json,os,re,shutil,subprocess,tempfile
from pathlib import Path
root=Path.cwd()
e=json.loads((root/"intent/0027-single-template-skill-parity/execution/parity-installation.json").read_text())
count=0
for row in e["inventory"]:
    for role in ("source","claude","codex","opencode"):
        folder=Path(row[role])
        actual={str(p.relative_to(folder)):hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.rglob("*") if p.is_file()}
        assert actual==row[role+"_hashes"],(row["skill"],role)
        count+=len(actual)
print("Evidence rehash: 16 skills x source/Claude/Codex/OpenCode; %d files identical to recorded hashes"%count)
with tempfile.TemporaryDirectory(prefix="0027-independent-") as td:
    target=Path(td)/"product"
    shutil.copytree(root/"tdd-optional/project",target)
    before={str(p.relative_to(target)):p.read_bytes() for p in target.rglob("*") if p.is_file()}
    guide=(root/"tdd-optional/org-skills/codex/README.md").read_text()
    block=re.search(r"```bash\n(.*?)```",guide,re.S).group(1)
    block=block.replace("/absolute/path/to/tdd-optional/org-skills",str(root/"tdd-optional/org-skills")).replace("/absolute/path/to/adopted-product",str(target))
    first=subprocess.run(["bash","-c",block],capture_output=True,text=True)
    assert first.returncode==0,first.stdout+first.stderr
    print("Fresh Codex README install rc=0; all four patches applied")
    names=sorted(p.name for p in (target/".agents/skills").iterdir())
    assert len(names)==16,names
    for row in e["inventory"]:
        installed=target/".agents/skills"/row["skill"]
        for rel,h in row["source_hashes"].items():
            if rel!="SKILL.md":
                assert hashlib.sha256((installed/rel).read_bytes()).hexdigest()==h
    for n in ("capture-intent","design-spec","plan","to-questionnaire"):
        assert "allow_implicit_invocation: false" in (target/".agents/skills"/n/"agents/openai.yaml").read_text()
    assert all((target/p).read_bytes()==b for p,b in before.items())
    repeat=subprocess.run(["bash","-c",block],capture_output=True,text=True)
    assert repeat.returncode!=0
    print("Fresh Codex: 16 folders, companion bytes, four explicit-only policies, original product files preserved; repeat rc=%d"%repeat.returncode)
payload={"tool_name":"Edit","cwd":str(root),"tool_input":{"file_path":"tests/test_template_editions.py","old_string":"review-test","new_string":"not-applied"}}
p=subprocess.run(["bash",".claude/hooks/protect-tests.sh"],input=json.dumps(payload),capture_output=True,text=True,env=dict(os.environ,INTENT_TASK="fix"))
print("Controlled hook rc=%d: %s"%(p.returncode,p.stderr.strip()))
assert p.returncode==2 and "BLOCKED" in p.stderr
p=subprocess.run(["bash","evals/run.sh"],capture_output=True,text=True,env=dict(os.environ,SDLC_EDITION="tdd-first"))
print("Retired edition rc=%d: %s"%(p.returncode,p.stderr.strip()))
assert p.returncode==2 and "invalid SDLC_EDITION" in p.stderr

```

기준·이전 사슬 비교의 보정된 본문도 `python3 -c`로 실행했다(종료 코드 0).

```python
from pathlib import Path
import subprocess
r=Path.cwd()
base=r/"tdd-optional/org-skills"
claude=(base/"agents/sdlc-verifier.md").read_text().split("## Review criteria\n",1)[1].strip()
opencode=(base/"opencode/agents/sdlc-verifier.md").read_text().split("## Review criteria\n",1)[1].strip()
codex=(base/"codex/agents/sdlc-verifier.toml").read_text().split("## Review criteria\n",1)[1].rsplit(chr(39)*3,1)[0].strip()
assert claude==opencode
assert claude==codex.replace("AGENTS.md, CLAUDE.md","CLAUDE.md")
print("Review criteria: Claude=OpenCode; Codex identical after declared AGENTS.md entry normalization")
changed=subprocess.check_output(["git","diff","--name-only","00fd7334","b9af49a"],text=True).splitlines()
assert all(p.startswith(("tdd-first/","tdd-optional/","intent/0026-traceable-artifact-handoff/")) or p==".claude-plugin/marketplace.json" for p in changed)
assert not subprocess.check_output(["git","diff","b9af49a","--","intent/0026-traceable-artifact-handoff"],text=True)
print("Previous chain 0026 own diff: %d files, listed package/authoring/policy/evidence families; old records unchanged in 0027"%len(changed))
print("HEAD/main:",subprocess.check_output(["git","rev-parse","HEAD","main"],text=True).strip())

```
