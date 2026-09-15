# 구현 검토: 요구·설계·계획 추적과 인계

검토한 소스에서 수정이 필요한 중요한 발견은 없었다. Bugs, Security, Compliance의 세 패스로
현재 문서와 실제 변경을 대조했다. 이 결과는 아래 소스 범위의 검토 보고이며 사람의 수락이나
T04 행동 확인·T05 커밋/통합 완료를 뜻하지 않는다.

검토자: 별도 문맥의 Astra/high. 작성 대화 대신 root가 제공한 범위·합의·기준판과 현재 파일을 읽었다.
검토 일자: 2026-09-15. 적용 지침: root `CLAUDE.md`, `REVIEW.md`, `.claude/agents/verifier.md`,
현재 설치된 `sdlc-feedback`, 보고서 작성의 `stop-slop-ko`.

## What I ran

작업 경로는 `/Users/jake/Projects/ai-native-sdlc-sample`, 브랜치는
`codex/traceable-artifact-handoff`, 읽은 HEAD는 `7856e8298cad5828bc7c16ab48eca846787a30be`다.
기준판 `00fd7334`부터 HEAD·현재 작업 트리까지를 읽었다. 미추적 두 판의
`project/docs/sdlc-authoring/traceability.md`를 포함했다. 기존 미추적
`docs/research/003-execution-plan-audit/`와 `docs/research/plan-skill-design/`은 보존 대상 입력이다.

주요 읽기 명령과 결과:

| 명령 | 종료 코드·관찰 |
|---|---|
| `git status --short --branch` | 0. 대상 브랜치와 수정·미추적 범위를 확인 |
| `git log -5 --oneline` | 0. intent `5385148` → spec `57c7721` → plan `7856e82` 순서 |
| `git diff --stat 00fd7334` | 0. 기존 추적 파일의 변경 범위 확인 |
| `git diff 00fd7334 -- tdd-first/project/templates tdd-first/project/examples/skills` | 0. 양식·작성 지침의 실제 변경 검토 |
| `git diff --name-only 00fd7334 -- tdd-first/project/templates/intent.md tdd-optional/project/templates/intent.md docs/verification docs/research` | 0, 출력 없음. 해당 추적 원본 변경 없음 |
| `diff -u tdd-first/project/templates/plan.md tdd-optional/project/templates/plan.md` | 1. 의도된 두 판의 검증 전략 차이를 읽음 |
| `diff -u tdd-first/project/examples/skills/plan/SKILL.md tdd-optional/project/examples/skills/plan/SKILL.md` | 1. test-first와 선택형·탐색 경로의 차이를 읽음 |

나머지 제품 정책·F01/M01·패키지·runtime 사본과 patch도 범위를 나누어 `git diff 00fd7334 -- …`,
`cat`, `nl -ba`로 읽었다. 큰 출력에서 잘린 부분은 좁힌 범위로 다시 읽었다. Python 표준 라이브러리의
읽기 전용 비교로 두 intent 양식의 기준판 바이트 보존, 두 traceability 원본의 일치, 기존 F01/M01
제목의 보존, manifest 판과 verifier 기준 사본을 확인했다. 비교 명령의 종료 코드는 0이었다.
Codex 기준 비교에서 최초 추출기가 TOML의 닫는 작은따옴표 세 개를 본문으로 포함했으나,
diff를 읽어 추출을 바로잡은 뒤 플랫폼의 `AGENTS.md` 추가 외에 기준이 같음을 확인했다.

제품 범위는 기준판 대비 변경한 `.claude-plugin`, `tdd-first`, `tdd-optional`의 추적 파일과
미추적 traceability 두 파일을 합한 60개다. 경로 정렬 후 각 `UTF-8 경로 + NUL + 파일 바이트 + NUL`을
연결한 SHA-256은 `f68443b3c5e6b661c30ba5d892bf37ee1a896e025bf25f98fcaba4b3f36cd65a`다.
이 식별자는 리뷰/실행 기록을 제외한 읽은 제품 소스 상태를 가리킨다.

## What I saw

**Bugs:** 현재 변경으로 생긴 중요한 계약·참조 결함은 발견하지 못했다.

`tdd-first/project/docs/sdlc-authoring/traceability.md:18-39`와 선택형의 동일 문면은
개발건 안의 ID 범위, 동일 항목 개정·이동 시 유지, 분할·대체 관계, 폐기 ID 재사용 금지,
단일 정본과 실제 anchor를 구분한다. spec의 요구와 설계, plan의 실행 방법을 서로 다른 역할로
정의하고 모든 메서드의 번호화나 쌍방 관계표 복제를 요구하지 않는다.

F01은 기존 R1–R3/AC1–AC4와 전체 계약을 유지하고 spec의 SP01에서 정확 비교·무쓰기·출력 경계를
소유한다. plan의 T01은 옵션 파싱과 출력 전 순회를 연결하며 P1–P3로 기능·인접 회귀·통합을
구분한다. 한 파일의 작은 설계에 M01과 같은 문서 분할을 강제하지 않았다.

M01은 `spec.md:15-25`에서 정본을 지정하고 architecture의 SP01–SP03, storage의 SP04–SP06,
operations의 SP07에서 요구 관계를 소유한다. T01의 보고서 API 전환, T02의 저장·동시성,
T03/T04의 import/export, T05의 시작 검증·API 연결, T06의 운영 문서, T07의 실제 리허설·전환으로
중요 설계가 이어진다. B2/B3 등의 기존 제목과 Upstream은 보존했다. `Current change`와
현재 본문 안내로 SP/T를 추가한 판을 과거 입력 SHA에 잘못 귀속하지 않는다.

두 판의 M01 T06은 Q4의 실제 명령·경로와 확인된 문서 인도를 완료 조건으로 삼는다.
T07은 그 문서와 통합 검증 판을 입력으로 받아 사본 리허설을 먼저 실행한다. 코드 PR의 JSON 기본
배포 가능성, SQLite 코드 통합, 운영 전환의 준비·성공은 별도로 남는다. P-C에서 운영 AC7을
제외하고 T07의 운영 증거에 연결한 변경도 이 범위와 맞는다.

**Security:** 추가된 자동 실행 코드·외부 endpoint·자격 정보·로그 수집 변경은 없었다.
소스 diff에 새 비밀 값이나 권한 확대는 발견하지 못했다. 실제 비밀 탐지 도구 실행이나 런타임 권한
집행 시험으로 확대하지 않는다.

**Compliance:** FR01–FR04/NFR01–NFR02와 구현 사이의 중요한 불일치는 발견하지 못했다.

| 계약 | 읽은 구현과 판단 |
|---|---|
| FR01 / SP01 | 두 spec 양식·design-spec과 traceability에서 FR/NFR → 주요 SP의 근거·다대다 관계·정본을 정의. 기존 R/AC 유지 |
| FR02 / SP02 | plan의 T에 설계 의미·실제 연결 방법·검증·Done·PR을 묶음. execution-depth:41-54에서 설계의 작업/보존/후속 범위와 첫 인도 준비를 대조 |
| FR03 / SP03 | 양 판 GIT-WORKFLOW와 feedback에서 실제 diff 및 관련 미포함 변경을 읽고, 영향 문서를 다음 의존 작업 전에 고치며 관련 커밋과 결과 내용을 확인 |
| FR04 / SP03 | PROCESS·feedback·execution-depth:83-86에서 현재 판·미커밋 범위·완료/미검증·의존성·다음 작업을 보존하고 재개 시 실제 Git·근거와 대조 |
| NFR01 / SP04 | intent 양식 바이트 불변. 기본형 test-first와 선택형의 동작별 구현 후 테스트·기존 시험·혼합/탐색 지침을 유지 |
| NFR02 / SP03–SP04 | 새 검사기·장부·커밋 스킬 없음. 기존 계획 수락과 최종 인도 검토를 구분하며 모든 helper/커밋의 새 독립 검토를 요구하지 않음 |

양식/작성 지침뿐 아니라 짧은 프로젝트 정책, feedback과 verifier에도 실제 변경의 의미를 따라
T → SP → 요구/AC·intent 제약을 대조하도록 넣었다. 코드 결함·허용 내부 선택·설계 개정과
spec-only/plan-only 변경을 구분하고, 영향 없는 문서의 동시 편집을 요구하지 않는다.

기본형 Claude/OpenCode의 Review criteria는 같고, 선택형도 Claude/OpenCode가 같다.
선택형 Codex는 프로젝트 진입 파일로 `AGENTS.md`를 추가한 차이 외에 같은 기준을 제공한다.
재생성된 feedback patch는 플랫폼의 검토자 경로·이름·모델 설정 전달만 바꾸며 새 추적·커밋·인계
본문을 지우지 않는다. root/에디션 marketplace와 plugin manifest는 기본형 0.1.11, 선택형 0.1.7이다.
제공되는 Codex adapter는 선택형이고, 개인 설치본과 별도 제품 갱신은 이번 범위에 포함하지 않았다.

북극성은 현재 HTML의 해당 원문과 주석을 읽었다. L2/V2-03·08의 요청자 언어와 intent 산문,
L3/V3-04·09·14의 요구·설계와 미결 질문·정책 근거, L4/V4-06–09·11·17의 실행 계획·동시 개정·정본,
L10/V10-05·06의 실제 변경 대조와 발견/승인 구분에 맞춘 소스 변경이다.
FR/NFR/SP/T 표기, 중단·재개 사건, T/PR 구분은 사용자가 요청한 팀 규칙이다.
플레이북의 축자 의무나 과거 부분 판정을 통과로 바꾼 근거로 주장하지 않았다.

## What does not match plan.md

이번 검토 대상으로 선언한 T01–T03의 소스와 현재 설계·계획 사이에 중요한 불일치 없음.
수정 요청 없음. 파일 목록은 실제 변경 범위를 포함하며 새 traceability 원본도 그 범위 안에 있다.
T04의 별도 행동 확인과 T05의 커밋·통합은 root의 진행 중 작업이므로 누락된 완료 항목으로 판정하지 않았다.

## What I could not check

root가 담당하는 `make check`, Claude strict 검증, 임시 patch 적용·설치 검증, 새 에이전트의
커밋·인계 fixture는 이 리뷰에서 중복 실행하지 않았다. 그 결과를 아직 읽지 않았으므로 성공으로
인용하지 않는다. 프로젝트 verifier의 이전 chain/부정 hook 인접 실행도 이 위임 범위에서 수행하지 않았다.

검토한 HEAD에는 소스 변경이 미커밋 상태였다. 최종 staged/commit 내용, 최신 main과의 결합,
통합 후 결과, 원격 PR/게시, 전역 설치는 확인하지 않았다. 제품 전체 SDLC, 두 판의 실제 TDD 개발,
모든 세션의 자발적 스킬 호출·문서 동기화 또는 강제 중단 예방을 입증하는 리뷰도 아니다.
후속 완료 보고는 root의 실제 실행 기록과 최종 Git 상태를 별도로 연결해야 한다.

## 후속 확인 — 실행 근거 인계

2026-09-15. 추가된 `execution/README.md`, `make-check.txt`, `claude-strict.txt`,
`source-static.txt`, `install-source-comparison.json`, `probe-input.json`, `probe-final.json`과
두 `probe-reader` 보고를 읽었다. 첫 요청·반환 응답·HUMAN 보완 요청과 설치 manifest도 대조했다.
위 최초 리뷰의 “아직 읽지 않았다”는 한계는 이 추가 근거에 대해 해소했다. 시험은 재실행하지 않았다.

주장 범위와 읽은 근거 사이에 중요한 불일치 없음. make check는 102개 시험 중 1 skip과 정상 종료,
hook 28개·eval fixture 8개·managed settings 통과를 기록한다. Claude strict의 다섯 manifest 통과와
정적 파싱·임시 설치 비교도 기록과 맞으며, semantic eval·실제 플랫폼 세션 행동으로 확대하지 않는다.
60개 제품 소스의 SHA-256을 다시 계산해 `f68443b3c5e6b661c30ba5d892bf37ee1a896e025bf25f98fcaba4b3f36cd65a`를
확인했다. staged 내용과 작업 트리의 제품 소스 차이도 없다.

fixture의 실제 `git show --format=fuller --stat 53c60dd7a7beb509c27ff1d1f07f9933c009fd47`은
spec·plan·execution·코드·시험의 동일 커밋을, 같은 명령의 `bc80ef851cd082ffa1b4c1e8bbd265503e4b01f3`은
세 문서만의 후속 보완을 확인했다. 두 명령과 `git status --short`는 종료 코드 0이며 scratch만
미추적으로 남았다. 입력/최종 snapshot의 바이트·해시 대조에서도 intent·코드·시험·scratch가 같고
기존 E01/E02 전체를 실행 기록의 앞부분에 보존했다. 이는 root 초안과 E02 근거의 재사용이다.

첫 제출의 Done/PR 소실과 결정 출처 누락, HUMAN 한 차례 피드백 후의 복구를 최초 무오류 성공으로
소급하지 않았다. 최종 plan/spec/E04와 독자 재확인은 그 두 누락의 해소를 뒷받침한다.
명시한 스킬 사용과 제한된 문서·커밋 인계에 대한 관측이며, 자연 스킬 선택·선행 문서 개정·TDD·
전체 제품 SDLC·장시간 재개 성공으로 해석할 근거는 없다. trim 자동 회귀와 제품 검토·통합·배포를
남은 범위로 둔 설명도 맞는다. 수정 요청 없음. 제작용 소스 커밋과 로컬 main 반영은 이 확인 뒤
root가 수행할 예정이므로 이번 부록에서 완료로 판정하지 않는다.
