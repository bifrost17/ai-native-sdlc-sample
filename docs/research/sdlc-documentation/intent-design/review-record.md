# intent 양식 작성·독립 리뷰 기록

2026-09-11. 작성과 수정: Codex root. 제작 브랜치: `codex/intent-template-design`.
제작 사슬: [0020](../../../../intent/0020-intent-form/plan.md).

## 판단 기준과 범위

북극성 Lesson 2의 원문을 기준으로 요청자의 말과 의도, 이유, 제약을 포착하고 사람이 정정할 수
있는지 검토했다. [입력](examples-inputs.md)에서 기능·버그·불완전한 요청의 예시를 먼저 쓰고,
[두 후보](alternatives.md)를 비교하여 다섯 구획의 간결한 형태를 골랐다.
입력에 없는 수치·담당자·원인·제약을 발명하지 않는지와 다음 독자가 무엇을 원하는지 이해하는지도
평가했다. 원문에서 허용하는 제안을 보존하면서 확정된 기술 선택과 구별한다.

평가 대상은 양식, 기존 capture-intent 스킬, 예시 세 개다. 두 리뷰어 모두 파일을 읽고 보고만
했으며 root가 작성·수정했다. 같은 [최초 요청](review-request.md)을 사용했고 최초 판정 전에
상호 리뷰를 공유하지 않았다. F01/B01의 공개 카드만 사용했으며 숨겨진 human.json 답은 사용하지 않았다.

## 후보와 리뷰

| 판 | 후보 SHA256 | Astra | Claude Code Fable |
|---|---|---|---|
| R1 | `f9d625f18407ae07f5abbe235e9da25eb92b731ca541d27a96b33d2a319f1ed9` | [PASS](reviews/astra-r1.md) | [PASS, 비차단 메모](reviews/fable-r1.md) |
| R2 | `4d8431b42d872243d71ac727eef2086ed474be53856da1d2eb4a3d78bdd3a118` | [PASS](reviews/astra-r2.md) | [PASS](reviews/fable-r2.md) |

후보의 개별 파일 해시와 합산 방법은 [R1](reviews/candidate-r1.json), [R2](reviews/candidate-r2.json)에 있다.
Astra는 `gpt-6-astra` / `ultra`로 설정했다. Fable은 실제 Claude Code CLI에서
`--model fable --effort max`로 호출했으며 두 응답의 실제 모델은 `claude-fable-5-1`이다.
Fable은 Read/Glob/Grep만 허용한 읽기 전용 세션으로 원문·입력·소비자를 대조했고 같은 세션에서
최종 수정분을 검토했다. 설치된 사용자 커스터마이징은 safe-mode로 분리했다. 이 호출은 설치된
스킬의 자연 호출 실험이 아니다. [최초 호출 설정](reviews/fable-r1-invocation.json),
[최초 결과 메타데이터](reviews/fable-r1-summary.json), [CLI 출력](reviews/fable-r1.jsonl),
[최종 호출 설정](reviews/fable-r2-invocation.json), [최종 결과 메타데이터](reviews/fable-r2-summary.json),
[최종 CLI 출력](reviews/fable-r2.jsonl)을 보존했다. 저장한 CLI 출력은 비공개 추론 블록만 제외한
내보내기이며, 도구 입력·출력과 최종 판정은 보존했다. [내보내기 기록](reviews/cli-log-export.json).

Astra는 파일 해시를 직접 재계산했다. Fable은 셸 없이 실제 파일을 읽고 제공된 영수증의 해시를
판정에 명시했다. root가 최종 리뷰 후 다섯 파일이 R2 영수증과 그대로 일치하는지 다시 확인했다.
Fable CLI가 보고한 사용량 비용 추정은 R1 $3.93602325, R2 $0.6347455이며 실제 청구액을 뜻하지 않는다.

## 발견과 root의 처리

| 발견 | 처리와 이유 |
|---|---|
| 기존 스킬의 해결 제안 배제·무조건적인 수치/재현 요구 | 요청자의 제안은 목적과 함께 보존하고 확정 제약과 구별한다. 없는 근거는 만들지 않고 중요한 미확인 사항을 질문으로 남긴다. |
| Fable: F01의 현재 환경을 외부 연결 도입 금지로 굳힘 | R2에서 환경 사실을 Affected users and systems로 옮겼다. 확인받지 않은 제약을 추가하지 않는다. |
| Fable: 불완전한 요청의 원인 확인 문장이 별도 절차 지시로도 읽힘 | R2에서 원인과 적합성이 아직 미확인이라는 사실만 남겼다. |
| Fable: 기존 스킬의 0002/0007 역사 참조 | R2에서 제거했다. 새 팀이 쓰는 작성 지침에 불필요하다. |
| Fable: 제목에 해결책 이름을 쓰지 말라는 안내 제안 | 추가하지 않았다. 이미 바라는 변화로 이름 붙이는 안내와 결과 중심 예시가 있고, 확인된 기술 제약도 있을 수 있어 포괄적 금지를 되살리지 않는다. |
| Fable: 버그 예시의 추가 질문·저장소에서 확인할 사소한 사실 생략 | 유지했다. 추가 질문은 미확인으로 표시되어 있고, 구현 세부를 모두 intent에 복제할 필요는 없다. |
| 기존 skill quick validator가 description의 꺾쇠 경로를 거부 | R2에서 설명 문장의 경로를 일반 표현으로 바꿨다. 도구와 검증 규칙은 변경하지 않았다. |

두 모델은 세 예시를 읽고 바라는 결과·이유·유지할 조건·미선택 제안·열린 질문을 다시 설명했다.
이것은 원래 대화 없이 문서에서 의미를 읽는 점검이며 에이전트가 실제 요청자와 대화하여 작성한
성능 실험은 아니다. A/B 비교도 root의 예시 기반 수작업 비교이며 무작위 대조 실험이 아니다.

## 검사와 남은 범위

독립 verifier는 `gpt-5.6-sol` / `high`로 호출하여 기존 검사·계획 범위·인접 흐름을 확인했다.
문서 설계 판단은 Astra/Fable에 맡기고 이 역할은 회귀와 증거 대조로 제한했다.

- `make check`: rc=0. unittest 96개 중 1 skip, hooks 28개, eval fixture 검사 8개,
  managed settings 검사 통과. [전체 출력](reviews/make-check.log).
  skip은 대소문자를 구별하지 않는 이 파일시스템에서 해당 구별을 전제로 한 검사다.
- 명시한 소비자 proof: rc=0, 30개 통과. 자동 intent 생성, 2σ 진단 인계, 3σ 제안 생성,
  스킬 펜스와 양식 동일성을 포함한다. [이름이 표시된 출력](reviews/proof-tests.log).
- 기존 skill quick validation: rc=0, `Skill is valid!`. [출력](reviews/skill-validate.log).
- production-gate에 잘못된 JSON 입력: 예상대로 rc=2, 저장소 변경 없음.
  [차단 출력](reviews/hook-bad-input.stderr).
- 제작 기준 `540ce05` 이후 변경과 plan 대조, 인접 0019 사슬의 자체 diff 대조: 범위 불일치 없음.
  [독립 검증 보고](reviews/verifier.md).
- root의 최종 산출물 점검: R2 파일 해시 일치, 새 문서의 로컬 링크 확인, `git diff --cached --check`
  통과. 북극성 원문 텍스트 해시와 179개 주석의 ID·순서·등급 클래스가 그대로다.
  [산출물 확인 기록](reviews/artifact-checks.json).

초기 skill validator 실행 환경에는 PyYAML이 없어 임시 venv에만 설치했다. 프로젝트 의존성은
추가하지 않았다. 이어 description 형식 오류를 발견하여 R2에서 수정했고 quick validation은 통과했다.

Root의 이번 범위 통과 판정: **PASS**. 두 설계 리뷰와 기존 소비자 회귀에서 중요한 미해결 문제가
없고, 의도·제안·제약·미확인을 짧은 양식에 보존한다. 추가 필수 구획이나 새 의미 검사기를
도입할 근거는 없다고 판단했다.

문서의 의미를 강제하는 새 검사기는 만들지 않는다. 이 작업은 전체 SDLC 대화 실험, 새 양식의
자연 스킬 호출 성공률, 호스티드 PR·조직 승인·merge, 모든 미래 요청에서의 무오류를 검증하지 않는다.
