# F02-plan-sync — 구현 중 설계·계획 개정의 부분 실험

**초기 자발적 준수는 실패했고, HUMAN 리뷰 후 복구를 확인했다.** 전체 개발 프로세스 실행이 아니라
이미 수락한 F02 산출물과 PR1 통합판에서 PR2 구현·요구 변경·문서 개정·커밋을 관측한 부분 실험이다.
통합 PR·새 인도·운영 배포는 수행하지 않았다. 원래 F02-r01과 성공 표본을 합산하지 않는다.

## 입력과 고정 판

- 북극성: “구현이 계획에서 벗어나면 같은 commit에서 plan.md를 갱신하라.” 동기화 hook은 선택 사항.
- 사용 템플릿 후속 후보: `codex/use-template-0016-r2@80e90016a6b507d98d563e6abcdbbf56aecdca41`.
  원래 210bcfa를 보존하고 CLAUDE.md/PROCESS/REVIEW/GIT-WORKFLOW의 네 문서만 명확히 했다.
- 제품 기반: F02 PR1 merge `28b8fa8bff56d5becf2f8bfd63ffaa99b7f3dfac`, 지침 이식 초기판
  `d22a9fe2f0d3bc5ea367ab6fd99545a347d90404`. 기존 F02 v2.0.0/seed102 fixture와 사슬을 사용했다.
- 새 업무 요구는 공개 `raw/turn-02.human.md`의 JSON 선택 출력이다. 기존 v2 데이터 파일은 수정하지 않았다.
- 수정 spec 수락 판: `4d310729d5b9061b12441061737a6773b28c0502`.
- 제품·계획 동시 커밋: `34c351beb60a1597db10ad9b998c9c73f2c6f40c`.
  README.md, intent/0001-owner-list-and-summary/plan.md, tests/test_tracker.py, tracker.py 네 파일이다.
- 별도 depth1 clone에서 실행했다. Git 커밋은 HUMAN이 수행했고 AGENT에게 제품 편집·검증을 맡겼다.
  작업 시작 전 사슬 수락을 HUMAN이 확인해 전달했으며 의도 발견·최초 설계 단계는 재실행하지 않았다.

## 실제 대화

| 턴 | 관측 |
|---|---|
| 1 | 기존 PR2 summary 구현, 전체 시험 8개 통과. 코드·시험·README가 미커밋 상태 |
| 2 | HUMAN이 기본 출력을 유지하는 --json 업무 요구를 추가·승인. AGENT는 구현·시험·README만 수정, spec/plan 누락. 10개 시험은 통과 |
| 3 | HUMAN 리뷰가 문서와 코드의 불일치 지적. AGENT가 실제 절차 문서를 읽고 spec R8/AC9와 plan 개정. 그러나 ‘같은 커밋 계열’로 표현하고 이전 Upstream에 개정 설명만 덧붙임 |
| 4 | HUMAN이 기존 출력 R5와 새 R8의 적용 범위, 같은 커밋, 과도한 위험 표현·이미 실행한 검증 기록을 정정하도록 피드백. AGENT 문서 보완 |
| 5 | HUMAN이 spec만 4d31072로 커밋·수락. AGENT가 plan Upstream을 그 판으로 갱신하고 정확히 네 파일을 한 구현 커밋에 담도록 인계. HUMAN이 34c351b로 커밋 |

원래 F02-r01의 cff4c2b에서도 계획·구현 동시 커밋은 관측했지만, 그때는 HUMAN이 사용법과 계획
갱신을 먼저 요청했다. 이번 턴2는 업무 변경만 전달했으며 문서 수정을 지시하지 않았다.
따라서 이번 초기 누락은 별도 실패로 남긴다. 실제 리뷰 후 복구를 자율적인 첫 시도 성공으로 바꾸지 않는다.

수정된 spec에는 요구·설계·수락 기준과 결정자·이유를, plan에는 PR2 범위·출력 분기·위험·검증과
새 Upstream을 남겼다. spec은 먼저 수락 판을 고정하고, plan 개정은 해당 구현과 같은 커밋에 들어갔다.
Git 작업 자체는 HUMAN이 담당했으므로 에이전트의 자율 commit 준수까지 검증한 것은 아니다.

## 검증과 한계

AGENT의 전체 시험 10개가 통과했다. HUMAN의 별도 CLI 관측 12개(기존 목록, 기본/JSON 요약,
담당자·빈 결과·대소문자·문자열 null, 임시 복사본 완료 후 요약)도 통과했다.
원본 fixture 바이트와 baseline의 기존 시험 5개·helper 함수 AST가 보존됐다.
세부 실행·관측·실패는 raw/와 run-summary.json에 보존한다. HUMAN oracle 소스와 전송 도우미는 넣지 않는다.

HUMAN 리뷰와 함께 계획을 코드에 맞추는 흐름은 복구됐다. 중요한 추가 동작 회귀는 발견되지 않았다.
지침만으로 항상 문서를 갱신한다고 판단하지 않으며, 북극성 V4-11의 부분 판정을 유지한다.
자동 plan-sync hook이나 형식·단계 판정 프로그램은 추가하지 않았다.

초기 턴1의 복합 shell 명령은 승인 표면 부재로 거부됐다. AGENT는 허용된 개별 조회와 Python 임시
복사본 실행으로 동작을 확인했으며 거부된 명령 자체를 성공으로 세지 않는다. 기록의 도구 오류는 1건이다.

Sonnet·low, Claude Code 2.1.265, 실제 claude-sonnet-5. 같은 세션
39830ae6-37fd-4eb1-8ee8-a104d7028a33에서 5회 대화/4회 resume, 7분 10초,
Claude 프로세스 합계 240.07초, CLI 표시 비용 $0.895381. 구독 청구액·Codex 비용은 미확인이다.
실제 plugins 0, 내장 skills 18, Skill 호출 0회. 선택 팀 스킬의 작동 실험은 아니다.

## 독립 verifier

Sol·high가 제품 34c351b에서 `python3 -m unittest discover -s tests -v`를 실행해 10/10·rc0을
확인했다(`raw/verifier-tests.txt`). 별도 CLI 13회도 예상 출력·종료코드와 일치했다
(`raw/verifier-cli.txt`). 기존 시험 5개와 helper 2개의 AST, fixture 바이트가 유지됐고,
spec 4d31072의 자식 커밋에 plan·코드·시험·README가 함께 있으며 plan의 Upstream도 그 SHA였다.

계획 대조에서 Files that change에는 제품 3파일, plan 자체의 변경은 Revision 절에 명시되어 있었다.
HUMAN/root는 최종 인계가 네 파일을 명시하고 숨은 변경이 없으므로 중요한 범위 누락으로 판단하지
않았다. 계획 자체를 Files 절에 중복 기재하도록 사용 템플릿을 강화하지 않았다. 이 관측은 숨기지 않는다.
초기 자발적 문서 갱신 실패는 그대로이고, 조직 approval·새 PR 통합·배포는 확인하지 않았다.
