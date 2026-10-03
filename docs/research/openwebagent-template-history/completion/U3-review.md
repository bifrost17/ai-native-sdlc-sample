# U3 적대적 리뷰 — 첫 실제 통합과 병렬 준비

2026-10-03. 현재 안내 전체와 선언된 참조를 함께 읽었을 때, U3를 막는 중요한 결함은 찾지 못했다.
추가 예시나 새 통제 없이 다음 단위로 진행할 수 있다는 검토 의견이다. source 완료·수락 여부는 root가 판단한다.

## Scope and revision

- 작업 위치: `/Users/jake/Projects/ai-native-sdlc-sample`.
- 실제 base와 검토 시 HEAD: `b814ec2379826fcfe98a63c191d6cced48f24051`.
- U3 미커밋 source: `tdd-optional/project/examples/skills/plan/references/execution-depth.md`.
- base 대비 변경은 설정 저장 예시와 준비 작업의 병렬 조건을 더한 7줄이다. 이미 base에 포함된 0.1.9 후보의 초기 통합 안내도 검토했다.
- `CLAUDE.md`, `README.md`, `.gitignore`, 실험/연구 경로 등의 다른 WIP는 U3 diff로 계산하지 않았다. 수정하거나 되돌리지 않았다.
- 소유 파일은 이 보고서뿐이다. source 수정, 제품 코드·브라우저·실험·전역 설치·발행은 수행하지 않았다.

## Criteria and inputs read

`CLAUDE.md`와 `.claude/agents/verifier.md`를 읽었다. 이번 역할은 0028 SP07/T08의 문서·스킬 적용성 검토다.
maker 전체 검사와 최종 verifier의 실행 기준은 U6/T11에 남긴다. U3만으로 chain 완료를 보고하지 않는다.
`sdlc-feedback`의 현재 합의·실제 diff·필수 정본 대조 기준과 `stop-slop-ko`의 보고서 작성 기준을 적용했다.

0028 최신 intent/spec/plan 전체를 읽었다. 적용 요구는 SP06의 실제 경계를 통과하는 작은 경로,
늦는 연결의 가정·시점·위험, SP07의 단위별 검토와 얇은 보완이다. 모든 인터페이스의 선행 확정이나
제품 실험 통과를 이번 검토의 조건으로 만들지 않았다.

북극성은 V4-06/V4-08/V7-05/V8-02의 본문과 주석을 읽었다. 파일·순서·증명 방법을 계획에 담고,
대화를 모르는 실행자가 따라갈 수 있게 하며, 공유 파일·계약의 의존성을 고려하고 작업 중 피드백과
마지막 새 문맥 검토를 구분하는 기준을 사용했다. 주석의 작은 사례 관측·합성 M01·독립 구현 미관측 한계를 유지한다.

활성 source의 `execution-depth.md`, `plan/SKILL.md`, `templates/plan.md`,
`docs/GIT-WORKFLOW.md`, `docs/PR-SIZE.md`, `docs/RELEASE-CONTROL.md`를 읽었다.
구체 인접 사례는 `docs/sdlc-authoring/examples/M01/`의 plan/context/spec와 그 필수
`inputs/current-contract.md`, `design/architecture.md`, `design/storage.md`, `design/operations.md`를 읽었다.
위 경로 중 별도 표시가 없는 제품 파일은 `tdd-optional/project/` 아래다.

## Adversarial checks and findings

### 모듈 완료를 계속 늘려 첫 통합을 무기한 미루는가

`execution-depth.md:36–40`은 위험한 실제 경로를 일찍 배치하도록 하고, 모든 모듈 이후로 미루려면
이유와 조기 대체 검증을 요구한다. 인프라가 늦으면 가상 경계와 실제 연결 작업/시점·잔여 위험을 적어야 한다.
새 예시의 입력→실제 호출→저장→재조회는 결과를 다시 소비하는 경로까지 포함한다.
같은 파일의 “남은 일과 현재 요약”에서는 내부 완료와 선행 조건만 늘어날 때 원래 Done으로 돌아가게 한다.
따라서 “나중에 통합”만 적고 준비 작업을 계속 늘리는 계획은 이 안내를 따른 결과가 아니다.
기간 상한이나 별도 통합 승인 장부를 추가할 이유는 찾지 못했다.

### 미래 인터페이스까지 모두 동결하게 만드는가

`execution-depth.md:36`은 이번 인도에 참여하는 경계로 한정하고 `:40`은 모든 미래 인터페이스의
선확정을 명시적으로 배제한다. `:33`에는 공유 계약 변경 시 spec 집합과 영향을 조정하는 절차가 있다.
plan skill도 중요한 미정 계약을 구현 작업 속에 숨기지 말라고 하면서, 확인되지 않은 함수·이름은 제안으로 표시한다.
plan 양식은 모든 클래스·메서드의 선행 식별을 요구하지 않는다. 현재 인도의 입력·오류 의미를 정하는 것과
미래 설계를 고정하는 것을 구별할 수 있다. 중요한 결함 없음.

### 첫 경로 우선이 독립 작업·PR·배포 가능성과 충돌하는가

`execution-depth.md:44–46`은 준비 PR의 보존/시험 범위와 첫 실제 연결을 구분하고,
첫 경로와 독립된 준비 작업의 병렬 실행을 허용한다. 같은 파일 `:25–34`는 main 기준, 종속 PR의 base,
파일 소유와 계약 판, 결합한 결과의 검증을 유지한다. `:51–53`은 일반 OFF에서도 배포 가능해야 한다고 한다.
Git/PR/공개 정책 또한 각 준비 PR의 기존 동작, 실제 효과 경계, 통합과 공개의 구분을 요구한다.
작은 경로를 만들었다고 공개하거나, 독립 작업을 무조건 첫 통합 뒤에만 시작하도록 해석할 필요가 없다.

### health check·mock을 사용자 흐름 증거로 올리는가

`execution-depth.md:40`은 타입 일치/health check의 증명 범위를 제한하고 `:48–49`는 제공자와 달라질 수 있는
중요 동작을 실제 제공자 또는 대표 제품 경로로 대조하게 한다. 빠진 앱 상태·권한·경합도 남긴다.
plan skill의 “mocked flow”와 제품 완료 구분, 양식의 예정 증명과 실제 명령·판·출력 구분도 일치한다.
이 문구는 mock을 금지하지 않으면서 가상 경계가 실제 연결로 확인됐다고 바꾸는 오판을 막는다.
이번 리뷰에서는 실제 제품 경로를 실행하지 않았다.

### M01과 충돌해 잘못된 순서를 지시하는가

M01은 이미 있는 API와 계정을 재사용하는 보고서 PR-A, 비활성 SQLite·이행/복구 도구 PR-B를
고정 공유 계약 아래 병렬 준비한다. B1은 실제 SQLite 연결·동시 완료·rollback을 확인하도록 계획하고,
그 성공을 API 연결 완료로 세지 않는다. B2/B3의 import/export는 데이터 보존과 최신 쓰기 복구를 준비한다.
PR-C/T05에서 실제 선택·API·보고서 결합을 다루며, Q4 운영 입력과 T07 사본 리허설은 별도로 남는다.
첫 SQLite API 연결이 B의 도구 준비 이후라는 잔여 통합 위험은 읽을 수 있고, 그 연결 작업·검증 위치도 정해져 있다.
현재 안내가 요구하는 조기 대체 검증과 늦는 연결의 명시를 적용할 수 있는 사례다.

M01에서 읽기 보고서 전환과 비활성 도구를 독립적으로 준비하는 대신 모든 작업을 하나의 수직 PR로
다시 짜도록 요구하면, 기존 계약과 실질 의존성에 따른 분할을 좁힌다. 새 예시는 순서가 예시임을 밝히고
독립 준비의 병렬을 허용하므로 M01을 잘못된 사례로 만들 정도의 모순은 없다.
M01 자체는 합성 계획이며 여기서 그 제품 구현이나 독립 실행 성공을 확인한 것은 아니다.

### 오류 계약을 첫 경로 뒤에 정해도 된다는 해석

새 문구 `:43`의 “그다음 권한 거절/저장 실패의 계약과 나머지 입력을 작은 인도로 확장”만 떼어 읽으면
오류 설계를 나중에 정하는 것으로 읽을 여지가 있다. 그러나 직전 `:36`은 결과/오류·중요 시퀀스를 spec에서
확인하도록 하고, `:45`는 기존 동작·공개 제어를 유지하도록 한다. skill도 중요한 인터페이스를 구현으로 미루지
못하게 한다. 현재 문맥에서는 이미 정한 계약의 구현·검증 범위를 후속 인도로 확장한다는 뜻으로 읽을 수 있다.
이 한 문장의 표현 선호만으로 수정 필수 지적을 만들지 않았다. 기존 권한을 제거한 첫 경로를 허용한다는 결론도 없다.

## Evidence and hashes

조회 명령 `git rev-parse HEAD`, `git status --short`,
`git diff b814ec2379826fcfe98a63c191d6cced48f24051 -- tdd-optional/project/examples/skills/plan/references/execution-depth.md`,
`git diff --check -- tdd-optional/project/examples/skills/plan/references/execution-depth.md`는 모두 exit 0이었다.
마지막 명령 출력은 없었다. 내용은 `cat`, `sed`, `nl -ba`로 읽고 잘린 도구 출력의 필요한 구간은 다시 읽었다.
SHA-256은 `shasum -a 256 <해당 경로>`로 확인했다. diff-check는 공백 검사이며 지침 효과의 증거가 아니다.

| 입력 | SHA-256 |
|---|---|
| execution-depth.md | `36c0407918e534d60c83fbdd7dd7e4883d8c0daeee24fe7dbaa0931caaafc15d` |
| plan/SKILL.md | `08a5e02ffdfc14bfa72b306a256e66fb82ef18012b3f7448d0ff649d49f5abeb` |
| templates/plan.md | `50fd7d6fbff00f2df2b2be030f38b8e8ff950253b8d0ee44f0108f89bf24226a` |
| GIT-WORKFLOW.md | `82831f2d6c03e148a372f917ee74172e2cf5abf53f11b4398945ae4d4b40d93c` |
| PR-SIZE.md | `38e7c1639c678d7114a80258131aa38dea0d97aac32cb651dbac79bd4a9416fe` |
| RELEASE-CONTROL.md | `da97242c7f7140b8c1090c67b0fe5f0ba43eb58063210d82280c27e067044ff8` |
| M01/plan.md | `91b83de62d97d13a8279e11213591b6d83184e5dcacd57a4380928a3d27da88c` |
| M01/spec.md | `b391c6506f73475e4c364b915e0b47f272082b27660087de7e1b75538a035c0c` |
| M01/context.md | `2dabc6b2607527022c6e850cecee390be26033195efe4c6036e83b0530211264` |
| M01/inputs/current-contract.md | `f5d7d83a71b65fc3fe85a74653f0bfee28acbaa52e9c2a144723a6cecb478a13` |
| M01/design/architecture.md | `36cafd2ad89a366868fbe183a3c9ba826f67e86b56ba45b1d53e043379d6a776` |
| M01/design/storage.md | `d7e4f4258a913608a9c9881169715d6fbd91ac7bb57b20c442565fbf33024432` |
| M01/design/operations.md | `0c765c908eb7f228812119c4250f8da80b4e405c91ddf3eb85c1a7581e5da2eb` |
| 0028/intent.md | `56c380d188c3eeff0b6c30951d831159fc32db27f781680caa13200235cd9106` |
| 0028/spec.md | `ff36f8b563e39326cc161fee680b7bbdeb728eb8659cf0943618229209ab0905` |
| 0028/plan.md | `16e20b67481a60eca32061c69bae8a34b4ca166db6267f8c4d684712ae46ac4a` |
| north-star-playbook.html | `e11f73355e5b2ec329f6d485487341ebc6d15aa7a54c4d4a5a7ef4f17329ca50` |

## Limits and handoff

필수 수정 지적은 없다. 위 결론은 이 판의 문서 내용과 인접 계약을 읽은 정적 검토다.
실제 에이전트의 자연스러운 스킬 선택, 첫 통합 시점 개선, 제품 동작, 개발 효과 AC04는 확인하지 않았다.
make check·패키지/adapter strict 검사·전체 diff 검증은 U6/T11 범위로 남긴다.
코드/운영 실험, 전역 설치, 커밋·푸시·병합·배포는 이 리뷰에서 하지 않았다. root가 현재 source 해시와
리뷰 범위가 유지되는지 확인하고 U3 판단 및 다음 단위 진행을 결정한다.
