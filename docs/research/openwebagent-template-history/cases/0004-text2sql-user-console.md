# 0004 Text2SQL 사용자 콘솔 — 단위 검증 뒤 실제 경로에서 드러난 결합 결함

판정: **범위를 한정한 심층 검토 완료**. 수집한 bare Git `main@a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e`와 PR API의 당시 문서·diff·본문을 읽었다. 제품 브라우저·엔진을 이 조사에서 다시 실행하지 않았다. 사용자의 대화 원문과 개발자의 실제 모델·OS는 별도 확인하지 않았다.

## 요청·설계·계획의 형성

| 사건 | 근거 | 해석 |
|---|---|---|
| 최초 요청 | 9/20 intent `94d2c050`은 관리자만 쓰던 text2sql을 일반 사용자 화면으로 옮기고 질문→SQL, 최근 질문, gold/설정 팝업을 요구했다. 기존 관리자 화면 제거·일반 사용자 읽기 전용·운영 `:3080` 무접촉이 제약이었다. [최초 intent:4–61](https://github.com/bifrost17/openwebagent/blob/94d2c050fd135e45be9651b833280211503a2632/intent/0004-text2sql-user-console/intent.md#L4-L61) | 최초 목표는 화면이지만, 실제 구현에는 데이터·API 경계가 필요했다. |
| 요청자 결정 확대 | 최종 intent는 데이터 소스별 gold, 별도 콘솔 축, 스키마 지식/선별, 파라미터, 기존 SQL Lab과의 비결합을 구체화했다. `Q16` 설정 팝업은 초기 제외를 뒤집었고, `Q27`에서는 0003과 겹치는 칸을 같이 쓰기로 정했다. [intent@main:34–105,123–154](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0004-text2sql-user-console/intent.md#L34-L105), [spec@main:428–449](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0004-text2sql-user-console/spec.md#L428-L449) | 추가 요구·실물 대조로 인한 정당한 개정과 최초 설계 부족을 구별한다. |
| 최초 spec | `232dbf75`는 엔진·실행기·CLI 세 코드베이스를 읽고 최초 조사 서술 셋이 틀렸음을 표기했다. SP01 화면, SP02 콘솔 API, SP03 이력, SP04 gold, SP05 지식을 나눴고 신규 표면 스켈레톤·설계 문서 집합을 정본으로 선언했다. [spec@232dbf75:1–30,182–315](https://github.com/bifrost17/openwebagent/blob/232dbf7544a4c0f01473996c60ad3da558ec0dae/intent/0004-text2sql-user-console/spec.md#L1-L30), [spec@main:220–230](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0004-text2sql-user-console/spec.md#L220-L230) | 최종 spec만 읽으면 탐색·정정 비용이 사라진다. |
| 목업의 지위 | 요청자는 목업을 **시안**으로 두고 실제 컴포넌트에 맞춰 만들도록 했다. spec은 구현 시 기존 레일·팝업·화면 말과 대조할 것을 요구했다. [spec@main:253–292](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0004-text2sql-user-console/spec.md#L253-L292) | 목업을 수락된 제품 화면이나 심미성 증명으로 세지 않는다. |
| 최초 plan | `c3aa20b1`은 T01 착수 실측, T02–04 저장소, T05–07 콘솔, T08–11 관리자/엔진, T12–14 프런트, T15–16 진입/배포의 논리 PR-A~E를 정했다. 검증 방식과 T→SP→FR/AC 추적, 구체화 전 착수 금지를 명시했다. [plan@c3aa20b1:1–18,41–90](https://github.com/bifrost17/openwebagent/blob/c3aa20b146d8dd4748b22a9bdf75288fa910e426/intent/0004-text2sql-user-console/plan.md#L1-L90), [plan@main:43–90](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0004-text2sql-user-console/plan.md#L43-L90) | 실행 방법·선행 경계가 있었다. 실제 GitHub 인도는 다섯 PR이 아니다. |

## 구현·브라우저 검증·후속

| 시점 | 확인한 사건 | 의미 |
|---|---|---|
| [#317](https://github.com/bifrost17/openwebagent/pull/317), `53560f0d` 머지 | T01–T16을 한 PR에서 인도했다. 저장소 정본→콘솔 라우터→관리자/번들→프런트 컴포넌트→레일 마운트의 코드 순서는 커밋과 plan T 블록에 남았다. PR 생성 당시 브라우저 golden path는 미실행이라고 체크했다. [plan@main:21–41,73–91](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0004-text2sql-user-console/plan.md#L21-L41) | 모듈·마크업 시험을 통합 UI 수락으로 바꾸지 않았다. |
| [#319](https://github.com/bifrost17/openwebagent/pull/319), `9959aa3a` 머지 | 격리 스택+Playwright 다크 화면에서 질문→SQL·최근 이력·gold·스키마·파라미터를 관찰했다. 여기서 읽기 호출이 생성 요청율을 소모해 429, 수식 없는 gold SQL 전부 거절, 다크 팝업 선택 탭 식별 불가를 찾아 고쳤다. [plan@main:424–446](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0004-text2sql-user-console/plan.md#L424-L446) | 세 결함은 이미 있던 AC/화면 기대를 실제 경로에 연결할 때 드러났다. |
| #319의 한계 | 엔진은 스텁이어서 `examples_used`가 고정 0이었다. disabled 배포의 빈 레일, admin 404, 못 닿는 DB, 공백 열, 좁은 SQL 화면 중 일부는 미검증/미처분이라고 명시했다. 백엔드 `--frozen` 수집 실패는 잠금 파일의 선재 의존 누락을 반대 판에서 대조했다고 주장한다. [#319](https://github.com/bifrost17/openwebagent/pull/319) | 스텁 화면 통과를 실엔진 품질·전체 배포로 확대할 수 없다. |
| [#321](https://github.com/bifrost17/openwebagent/pull/321), `9dfb8d4a` 머지 | 실 deepeye 엔진에서 gold `등록 2·쓰인 0`을 확인해 `_prune_examples`의 수식 없는 표 이름 대조를 고쳤고 `2·2`로 재관찰했다. 못 닿는 DB는 500 대신 콘솔 봉투 403으로, disabled 레일은 미마운트로 확인했다. 공백 열은 번들 규약 변경이 필요해 범위 밖, 좁은 SQL 가로 스크롤은 기존 CodeEditor 보존으로 정했다. [plan@main:448–476](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0004-text2sql-user-console/plan.md#L448-L476) | #319에서 연 정상 gold 등록이 실엔진 소비에서 다시 깨진 **연속 통합 사건**이다. |
| 인접 제품 결합 | #320의 `uv.lock` 누락은 SQL Lab 의존이지만 0004 검증 스택에도 영향을 주었다. 0003과 공유 칸·리비전·라우트는 plan의 선행 재동기·소유자 결정 대상이었다. [#320](https://github.com/bifrost17/openwebagent/pull/320), [plan@main:491–496](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0004-text2sql-user-console/plan.md#L491-L496) | 환경/의존 잠금과 이 사례의 UI 결함을 같은 원인으로 묶지 않는다. |

## 여섯 평가축과 가설

| 축 | 판정 |
|---|---|
| 의도 보존 | **대체로 확인.** 관리자 전용→일반 사용자 콘솔, 관리자 편집/사용자 읽기, 기존 화면 제거와 SQL Lab 비결합이 유지됐다. 스키마 지식/공유 칸 확대는 요청자 결정으로 기록됐다. [intent@main:123–154](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0004-text2sql-user-console/intent.md#L123-L154) |
| 설계 충실성 | **부분 확인.** 콘솔·관리자·에이전트 축, 공유 스키마 칸, 오류 봉투, gold 검증/소비 계약을 다뤘다. 읽기 요청율과 수식 없는 gold의 두 단계 불일치는 코드·시험·실화면에서 뒤늦게 드러났다. [spec@main:220–252,438–448](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0004-text2sql-user-console/spec.md#L220-L252), [#319](https://github.com/bifrost17/openwebagent/pull/319), [#321](https://github.com/bifrost17/openwebagent/pull/321) |
| 계획 실행성 | **강점, 인도 압축.** 각 T의 파일·방법·기대·검증과 소유자 확인을 세웠다. 그러나 PR-A~E는 실제 한 #317에 압축되어 단계별 main 노출·재검증 증거는 없다. 브라우저 검증 빚을 후속 두 PR에서 상환했다. [plan@main:43–91,478–495](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0004-text2sql-user-console/plan.md#L43-L91) |
| PR·병렬 분할 | **실제 세 번의 인도**(#317 구현, #319 스텁 UI 통합, #321 실엔진 최종). 0003과 병행한 공유 파일·리비전 사슬은 plan이 위험으로 적고 재동기했다. [#317](https://github.com/bifrost17/openwebagent/pull/317), [plan@main:491–496](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0004-text2sql-user-console/plan.md#L491-L496) |
| 변경 피드백 | **확인.** 탐색에서 최초 서술 정정, 17회 계획 리뷰의 의미 불일치 조정, 브라우저 3결함·실엔진 2결함을 기존 AC에 연결했다. #321은 요구 추가가 아니라 누락된 구현 연결의 수정으로 기록했다. [plan@main:1–19,424–476](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0004-text2sql-user-console/plan.md#L1-L19) |
| 검증·보고 | **범위 구분이 강점.** #317은 브라우저 미실행, #319는 스텁 한계, #321은 실엔진 관측·선재 실패를 적었다. 이번 조사의 실행 통과는 0건이다. [#317](https://github.com/bifrost17/openwebagent/pull/317), [#319](https://github.com/bifrost17/openwebagent/pull/319), [#321](https://github.com/bifrost17/openwebagent/pull/321) |

H1은 **부분 지지**: 디자인 문서는 풍부했으나 실제 API·엔진 계약의 표 이름 비교가 어긋났다. Q16·Q27 등은 새 결정/실물 정정이라 최초 설계 결함으로 합산하지 않는다. H2는 **부분 지지**: 시안이 제품 수락은 아니었고 다크 선택 탭의 식별 실패가 실제 브라우저에서 나왔다. 그 한 건으로 전체 심미성·통일성은 판정 불가다. H3는 **지지**: 저장소→콘솔→프런트→실엔진 순서에서 분리 시험이 놓친 요청율·gold 소비 결합이 나타났다. H4는 **부분 지지**: AC·검증 명령은 상세했으나 #317 당시 실화면·실엔진 절차 실행이 빠졌다. 후속 PR이 그 공백을 좁혔다.

현 0.1.8 정본에는 공유 계약·실제 UI 관측·독립 기대·미실행 구분이 이미 있다([기준 비교](../baseline.md)). 잔여 개선 질문은 **계획한 논리 PR 경계를 실제 머지/브라우저/실엔진 검증 시점과 맞춰 첫 제품 인도에서 최소 대표 흐름을 언제 볼지**다. 귀속은 템플릿 부재보다 프로젝트 인도 압축·실행 환경·구현의 경계 불일치에 가깝다. CodeRabbit 생성 요약과 GitHub formal review API 빈 배열은 사람 리뷰의 유무를 증명하지 않는다.
