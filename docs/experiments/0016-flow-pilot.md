# 0016 — PR 크기·GitHub Flow의 실제 개발 실험

2026-09-11, HUMAN(Codex root, simulated)은 **이번 작은 개발 흐름을 통과**로 판단했다.
Claude Code가 사용 템플릿의 정책을 읽고 PR 경계를 계획했으며, 실제 GitHub PR 두 건으로
업무 결과를 순차 통합했다. 전체 회귀·새 복제본 인도·두 번째 변경 되돌리기를 확인했다.
최적 PR 줄 수나 모든 플레이북 항목의 성공률을 측정한 실험은 아니다.

## 바뀐 템플릿과 근거

[조사 보고서](../research/pr-size/README.md)는 연구·공식 운영 사례·공개 PR의 수치와 한계를 구분한다.
확인한 자료로 AI 리뷰 환경의 보편적인 최적 LOC를 정할 수 없었다. 따라서
[PR 크기](../PR-SIZE.md)는 응집된 목적·검증·복구를 기준으로 판단하고,
[GitHub Flow](../GIT-WORKFLOW.md)는 최신 제품 main에서 짧은 작업 브랜치와 PR로 통합하도록 정했다.

사용판의 `templates/plan.md`는 필요한 경우 선행 관계·병렬 작업 경계·PR 묶음·머지 순서·각 통합에서
동작해야 할 범위를 작업 순서에 담는다. 작업과 PR은 일대일이 아니며 LOC 견적을 요구하지 않는다.
단계별 문서 수락은 최종 구현 PR 승인과 구분하고, 같은 Draft PR에서 승인 문서 SHA와 결정을 보존한다.
기본 merge commit은 그 원본 SHA를 유지한다. 다른 머지 방식에는 조회 가능한 원본 또는 검증된 대응을 남긴다.

원래 사용판 a2bbfe1과 0015 후보 15ab8a6은 보존했다. 새 후보는 18개 파일이며 8개 파일을 변경했다.
두 정책 원문은 제작판과 사용판에서 바이트가 같다. 자동 검사·hook·CI·필수 스킬을 추가하지 않았다.
기존 자체 제작 스킬 예시는 선택 사항으로 남고, plan 예시는 변경된 공통 양식을 따른다.

## 고정 판과 보존 위치

| 구분 | 판 |
|---|---|
| 사용 템플릿 | `codex/use-template-0016@210bcfab3063a47abac147f2b19953085cb22c6f` |
| 데이터 | [F02 / v2.0.0 / seed102](datasets/v2/manifest.json), v1 baseline 해시 고정 참조 |
| 실험 초기 제품 | `a1935fabd974f6196248869c09f74578fc6e6fc4` |
| 제품 검증 최종 | `3f342c1d355c6941287127ff8969ec6f37c8943c` |
| 기록 포함 최종 | `codex/experiment-2026-09-11-f02-r01@11cb93cfd320491a8012045a9f001b41f311cdcf` |
| PR2 revert 대조 | `codex/experiment-2026-09-11-f02-r01-revert@cf6379955ed327a5a97874fe8657b867a41556e1` |

[실험 브랜치의 EXPERIMENT.md](https://github.com/bifrost17/ai-native-sdlc-sample/blob/11cb93cfd320491a8012045a9f001b41f311cdcf/EXPERIMENT.md)에
8회 대화 요약·챕터 2~13의 흐름 회귀·한계를 보존했다. 같은 판의 `raw/`에는 공개 대화·도구 결과·
PR 기록·실제 시험 출력이, `run-summary.json`에는 환경·세션·제품 핀과 공개 파일 54개의 SHA256이 있다.
[기록 전용 PR #73](https://github.com/bifrost17/ai-native-sdlc-sample/pull/73)은 종료 후 증거만 보관하며 제품 코드를 바꾸지 않았다.

HUMAN 비공개 결정·oracle 원본·전송 도우미는 로컬
`/Users/jake/Projects/ai-native-sdlc-experiments/human-f02-r01`에 두고 AGENT 복제본에 전달하지 않았다.
공개 입력·응답만 보존하며 숨겨진 추론과 계정 이메일은 제외했다. 최초 clone은 depth1/single-branch로
만들어 제작 부모 조회가 rc128임을 확인했다. 로컬 제품 main은 전용 원격 실험 브랜치에 대응하며,
제작 원격 main@37c596d는 실험에서 변경하지 않았다. 끝난 원격 작업 브랜치를 정리하고 로컬 refs는 남겼다.

## 실제 대화와 PR

Claude Code 2.1.265, 요청 sonnet·low, 실제 모델 claude-sonnet-5.
동일 세션 `ab3c2b91-54ad-44bc-9a68-5f3bb7975683`에서 8회 대화(7회 resume)했다.
AGENT가 필요한 동작을 질문하고 HUMAN이 목록을 먼저 사용할 업무 사정·정확한 출력과 예외를 공개했다.
intent 17bf490 → spec 892d6a5 → plan 0b8aff6을 수락한 후 구현했다.

턴4에서 두 정책과 plan 양식을 실제 읽고, 같은 파일과 선택 의미를 공유하므로 순차 PR로 제안했다.
HUMAN은 명세 참조·사용 설명·계획 갱신·출처와 마지막 위험 표현을 실제 응답에 따라 피드백했다.
턴5 cff4c2b에 README 사용법과 plan 갱신이 구현·시험과 함께 들어갔다. 고정 대본을 재생하지 않았다.
Git/PR 조작은 HUMAN이 맡았다. 첫 Draft PR도 조기 인도 요구에 따라 HUMAN이 열었으므로
에이전트가 최적 PR 개수를 독립 발견했거나 자율 GitHub 운영을 완수했다고 주장하지 않는다.

| 개발 단위 | 실제 PR · merge | 크기 | 검증 |
|---|---|---|---|
| 담당자 목록 | [#71](https://github.com/bifrost17/ai-native-sdlc-sample/pull/71) · 28b8fa8 | 6파일 +241/−1, 공통 사슬 문서 포함. 제품 코드 +4/−1 | 시험 5/5·독립 동작 3/3, 통합 후 재확인 |
| 상태 요약 | [#72](https://github.com/bifrost17/ai-native-sdlc-sample/pull/72) · 3f342c1 | 3파일 +53/−3 | 전체 시험 8/8·독립 동작 7/7, 기존 시험 AST·fixture 보존 |
| 새 복제본 인도 | 제품 최종 3f342c1 | 통합 결과 그대로 | 8/8·7/7, 독립 verifier도 별도 확인 |
| PR2 코드 되돌리기 | cf63799 | merge를 `git revert -m 1` | tree가 PR1 통합판과 같음, 5/5·3/3, summary 미존재 rc2 |

PR의 댓글에 단계 수락·피드백·최종 수락을 남겼고 승인된 문서 SHA가 최종 제품 이력에서 조회된다.
같은 계정의 HUMAN 댓글과 merge이며 정식 동료 계정의 approval은 없다. 호스티드 CI check도 없다.

## 회귀 판정·비용·한계

의도와 질문 → 명세·정책 → 계획 → 구현·시험·리뷰 → 통합·인도·유지보수 인계를 전체 흐름으로 확인했다.
특히 문서마다 PR 강제, 승인 SHA 유실, 임의 병렬화, 작은 PR에서 통합 회귀 누락이 없는지 보았다.
변하지 않은 설명·역할 원칙은 0015의 고정 근거를 재사용했고, 바뀐 지침과 연결 단계는 재평가했다.
역사적 실패와 제작판 179개 주석의 집계(139/23/17)는 유지한다. 이번 근거는
V4-06·09·11, V7-05·06, V10-05·07에 사용판 범위를 구분해 기록한다.

선택된 팀 스킬·플러그인은 없었다. 실제 init은 plugins 0, 내장 skills 18이며 Skill 호출 0회다.
스킬 적용·병렬 Claude 세션·자동 PR 리뷰·실제 조직 권한 분리·호스티드 CI·운영 배포와 사고 대응은 미관측이다.
새 복제본은 로컬 인도, revert는 코드 복구 확인이며 데이터·외부 효과 복구까지 증명하지 않는다.

도구 오류 3건을 숨기지 않았다. 턴5 복합 명령은 승인 표면 부재로 실행 거부되어 개별 재실행했고,
턴6·7의 echo 구분자가 든 명령은 일부 실행 후 rc1로 멈췄다. 턴6 나머지는 개별 재실행,
턴7 summary는 별도 실행했다. 실패한 묶음을 통과로 바꾸지 않았으며 최종 동작 판정은 성공한
unittest와 HUMAN의 새 복제본 독립 관측에 근거한다. 제품 시험 자체의 실패는 없었다.

실제 대화는 UTC 2026-09-10 15:18:14~15:34:22(한국 9월 11일), 약 16분 8초다.
Claude 프로세스 합계 280.09초, CLI 표시 비용 합계 $1.035306이며 구독 청구액이나 Codex 비용은 아니다.
작은 합성 사례 1건이므로 대형 프로젝트·대형 PR 성능이나 통계적 최적 크기로 일반화하지 않는다.

## 독립 verifier

Sol·high가 `.claude/agents/verifier.md`의 읽기 전용 검증을 수행했다. 전체 출력은 실험 판의
`raw/maker-make-check.txt`, 1차 요약은 `raw/independent-verifier.md`에 보존했다.

- **실행:** 제작 `make check` rc0, 인도판 `python3 -m unittest discover -s tests -v` rc0,
  독립 CLI 목록/조회/없는 ID/요약/완료 후 요약 관측, 두 정책 `cmp` rc0,
  이전 사슬 0015의 제작·사용판 diff 대조. 임시 복사한 production-gate에 잘못된 JSON을 넣어 rc2 확인.
- **관측:** `Ran 81 tests in 19.591s` / `OK (skipped=1)` / `test_hooks: 28 passed, 0 failed` /
  `8 passed, 0 failed` / `PASS  managed-settings 키·훅 계약`. skip은 macOS 파일시스템의 조건부 대조다.
  의도한 음성 입력은 `[production-gate.sh] BLOCKED: hook input is not valid JSON; refused.`로 차단됐다.
  인도판 8개 시험과 별도 동작이 통과했고 fixture 해시는 전후 같았다.
- **계획 대조:** 1차의 작성 중 문서까지 마무리한 0c8c81e를 재확인했다. 제작 diff 18파일과 사용판
  8파일이 계획과 양방향으로 일치했다. 상대 링크 49개 정상, 공개 기록 54개 해시 일치,
  원문 불변·179 ID·139/23/17 집계 유지, 실제 PR #71~#73의 상태·크기·범위가 기록과 같았다.
  기록 PR 전후 제품 blob도 같았다. 중요한 과장·누락·계획 불일치 없음으로 보고했다.
- **확인 불가:** 실제 동료 승인·호스티드 CI·운영 환경은 없으며 사용판에 제작 hook/스킬의 성공을 승계하지 않는다.
  외부 DOI 1개는 자동 curl 요청에 403을 반환해 그 방식의 도달성만 확인할 수 없었다.

## 후속 요청 — 구현 중 설계·계획 개정의 부분 실험

사용자가 계획 이탈 시 같은 커밋 갱신의 반영·실행을 추가 검증하도록 요청했다. 원문에는 정확히
“구현이 계획에서 벗어나면 같은 commit에서 plan.md를 갱신하라”가 있고 동기화 hook은 선택이다.
제작용 plan 스킬은 명시했지만 사용판 CLAUDE는 ‘같은 변경’이라고 표현해 같은 PR로도 읽힐 여지가 있었다.

후속 사용 후보 `codex/use-template-0016-r2@80e90016a6b507d98d563e6abcdbbf56aecdca41`에서
CLAUDE.md·PROCESS·REVIEW·GIT-WORKFLOW 네 문서(11줄 추가/3줄 삭제)를 명확히 했다.
계획의 파일·순서·PR 경계·검증이 달라지면 이유와 plan.md를 해당 구현과 **같은 커밋**에 담는다.
요구·설계 변경은 spec과 영향받는 결정을 확인하고 수락 판을 먼저 고정한 뒤 plan의 Upstream에 연결한다.
기존 210bcfa와 전체 F02-r01 기록은 유지했다. 후속 후보를 전체 흐름의 새 성공 표본으로 세지 않는다.

부분 실험은 F02 PR1 통합 28b8fa8에서 지침을 반영한 d22a9fe로 시작했다. Sonnet·low의 같은
세션에서 summary를 구현한 후, 미커밋 상태에서 기본 출력은 유지하는 `--json` 요구를 전달했다.
**턴2에서 코드·시험·README만 수정하고 spec/plan은 누락했다.** HUMAN 리뷰 후 턴3에서 문서를
갱신했지만 ‘같은 커밋 계열’과 이전 Upstream 표기를 남겼다. 턴4에서 문서 정합성을 정정하고,
수정 spec을 4d31072로 커밋·수락한 뒤 턴5에서 그 SHA를 plan Upstream으로 연결했다.

HUMAN이 만든 **34c351beb60a1597db10ad9b998c9c73f2c6f40c**에는 코드·시험·README·수정 plan이
정확히 한 커밋으로 들어갔다. AGENT의 전체 시험 10개와 HUMAN의 별도 CLI 관측 12개가 통과했고,
기존 시험 5개·helper AST와 fixture 바이트도 보존됐다. Git 조작은 HUMAN이 수행했다.
**자발적 문서 동기화는 초기 실패, 사람 리뷰를 포함한 복구는 확인**으로 구분한다. V4-11은 부분을 유지한다.

5회 대화/4회 resume, 실제 claude-sonnet-5, 7분 10초, 프로세스 합계 240.07초,
CLI 표시 비용 $0.895381이다. 복합 shell 명령 거부 1건과 그 뒤 성공한 별도 확인을 그대로 기록했다.
팀 스킬 적용·새 통합 PR·배포는 이 부분 실험에서 수행하지 않았다. 고정 입력 v2는 바꾸지 않았고,
새 업무 요구와 실제 리뷰는 부분 실험의 공개 프롬프트에 보존한다.

기록 포함 최종은 `codex/experiment-2026-09-11-plan-sync@5e5b71d0581651ca26afc14367c52a5a69d50607`다.
[EXPERIMENT.md](https://github.com/bifrost17/ai-native-sdlc-sample/blob/5e5b71d0581651ca26afc14367c52a5a69d50607/EXPERIMENT.md),
같은 판의 `raw/`와 `run-summary.json`에 공개 기록 28개의 해시를 보존했다. 종료 후 기록만 추가했으며
제품 검증 핀 34c351b와 구분한다. 중간 미커밋 diff는 공백을 보존하는 JSON 문자열로 저장했다.
비공개 oracle·전송 도우미는 `/Users/jake/Projects/ai-native-sdlc-experiments/human-f02-plan-sync`에 남긴다.

후속 독립 verifier(Sol·high)의 보고:

- **실행:** 제품 34c351b에서 `python3 -m unittest discover -s tests -v` rc0, CLI 13회 관측,
  기존 5개 시험·helper 2개 AST와 fixture 대조, spec→구현 부모 관계·plan Upstream·5회 공개 대화 확인.
- **관측:** `Ran 10 tests in 0.521s` / `OK`. CLI의 예상 출력·종료코드 일치, fixture SHA 전후 동일,
  plan과 구현이 같은 커밋이고 Upstream은 수락된 4d31072였다. 제품 검사에서 예상 밖 실패 줄은 없었다.
- **계획 대조:** Files에는 제품 3파일, plan 자체는 Revision 절에 동시 커밋 대상으로 명시돼 있었다.
  root는 최종 인계의 네 파일과 실제 변경이 일치하고 숨은 범위가 없어 중요한 누락으로 판단하지 않았다.
  이 차이를 기록하되 사용판에 계획 자체의 중복 기재를 강제하지 않았다.
- **확인 불가:** 초기 자발적 동기화는 실패했다. 복구와 커밋 조작에 HUMAN이 개입했고,
  새 PR 통합·실제 조직 승인·배포는 부분 실험 범위 밖이다.

독립 보고 원문은 기록 판의 `raw/verifier-summary.txt`, 실제 출력은 `raw/verifier-tests.txt`와
`raw/verifier-cli.txt`다. 부분 실험 뒤 제작 원문·179개 ID와 집계, 데이터 v1/v2, 배포 정책 동일성,
기록 해시와 제품 불변을 정적으로 재확인했다. 제작 코드·시험은 그대로라 앞선 make check 결과를 재사용했다.
