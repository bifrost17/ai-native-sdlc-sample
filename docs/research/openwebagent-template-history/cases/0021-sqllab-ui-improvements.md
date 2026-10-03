# 0021 SQL Lab UI 개선 — 초기 설계와 결합 후 화면의 차이

판정: **범위를 한정한 심층 검토 완료**. 수집 기준은 2026-10-03의 원격 `main@a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e`다. 아래 사건은 수집한 bare Git의 해당 커밋 문서·diff, GitHub PR API 본문과 첫 부모 머지 이력에서 확인했다. PR 본문의 시험 수치와 사람 확인은 **당시 실행자의 기록**이다. 이 조사에서 테스트·브라우저·제품 스택을 다시 실행하거나 원래 사용자 대화 원문을 읽지 않았으므로 독립 재현 통과로 바꾸지 않는다. 원자료는 `.local/research/openwebagent-template-history/20261003/collection/`에 보존한다.

## 북극성과 이 사례의 질문

제작 저장소 [README](../../../../README.md)의 북극성은 AI-Native SDLC Playbook이며, [이 조사 기준](../README.md)의 여섯 축은 의도 보존, 설계 충실성, 계획 실행 가능성, PR/병렬 분할, 변경 피드백, 검증·보고 정확성이다. 플레이북의 요구·설계(241–294), 계획(296–388), 병렬 세션(531–594), 피드백(596–660), PR 검토(742–801)와 연결해 읽되, **제품 결함·플레이북 충실성·현재 템플릿 결함·당시 프로젝트 실행**은 서로 다른 판정이다. 템플릿이 이런 화면을 자동으로 보장했다거나 후속 결함 하나가 곧 템플릿 결함이라는 주장은 하지 않는다.

해당 주석 중 [V3-03](../../../verification/north-star-playbook.html#V3-03)은 Design 목업→코드 경로를 당시 **팀 몫(미검증)**으로, [V4-11](../../../verification/north-star-playbook.html#V4-11)은 계획 이탈의 같은 변경 내 갱신을 **부분**으로, [V7-01](../../../verification/north-star-playbook.html#V7-01)은 병렬 세션의 독립 작업 공간을 **충실**로 기록한다. 이들은 템플릿의 역사적 주석이며 0021 실행을 자동 판정하지 않는다. 0021에는 실제 레퍼런스 UI 촬영·측정, 선행 PR 경계, 후속 계약 전파 누락이라는 별도 사건이 있다.

0021의 실제 요청은 `:3080` SQL 편집기 **오른쪽**을 실행 중인 Superset SQL Lab과 시각적으로 가깝게 맞추고, **왼쪽**을 DBeaver식 단일 트리로 바꾸는 것이었다. 편집 영역 안 데이터 소스·스키마 선택 구조와 기존 연결·클릭 동작은 유지한다. 처음의 “테이블·뷰만” 결정은 같은 날 “DBeaver 폴더 전체”로 바뀌었고, 새 메타데이터 API는 기존 동작 유지의 명시적 예외가 됐다. [intent@0e01e1c](https://github.com/bifrost17/openwebagent/blob/0e01e1c3a962ce4af8d390272c98ae0943f1861b/intent/0021-sqllab-ui-improvements/intent.md#L1-L45), [수정 intent@b1428ac](https://github.com/bifrost17/openwebagent/blob/b1428acef7df8e03c2dacadebb6a602b5c34958f/intent/0021-sqllab-ui-improvements/intent.md#L47-L79).

## 사건 사슬

| 단계 | 확인한 사건과 근거 | 판정 한계 |
|---|---|---|
| 요청·설계 입력, 9/29 | `0e01e1c`에서 intent가 먼저 생겼다. `b1428ac`는 D25–D28의 요청자 조정을 기록했다. `f3f25dc`에서 spec과 오른쪽·왼쪽·메타데이터 API·검증 설계 4편을 추가했다. `08c9499`, `fc54ecc`, `cd7d7eb`는 설계 검토 지적과 추가 결정을 고쳤다. [PR #403](https://github.com/bifrost17/openwebagent/pull/403), [spec 초기판](https://github.com/bifrost17/openwebagent/blob/f3f25dcb0f7f946f2ddd3107f5de2d827d7f4851/intent/0021-sqllab-ui-improvements/spec.md#L1-L23). | 커밋 순서가 단계 선행을 보여 준다. 대화에 나온 모든 결정의 원문과 당시 사람이 실제 읽은 범위까지 증명하지는 않는다. |
| 계획·수락, 9/29 | `9f3ff37`의 plan 초안 뒤 파트별 보강 `eb2bd4f`, 요청자 결정 반영 `f480911`, 인계 검토 대응 `6bfb004`·`26212ab`·`2da3f6d`, GitHub 조회 실패 처리 `77d7351`, 계획 수락 기록 `703942e`가 순서대로 있다. plan은 Astra medium 검토 네 번의 판정이 조건부·아니오·아니오·조건부였고 마지막 수정본 재검토는 없었다고 **자체 기록**한다. [plan@3084414:16–47](https://github.com/bifrost17/openwebagent/blob/3084414a4c9c370fb48d6e3f2c580a0c244f7cca/intent/0021-sqllab-ui-improvements/plan.md#L16-L47). | 계획 수락은 구현·시각 동등성 통과가 아니다. 모델 이름·검토 결과는 기록에 의존한다. |
| PR-0, 9/30 | [#403](https://github.com/bifrost17/openwebagent/pull/403)은 제품 코드 없이 intent/spec/plan, 측정 기대값, 참고 이미지, 이미지·라이선스 gate를 넣었다. `ae4bdc2`·`db8c070`은 오른쪽 기준값과 왼쪽 구조 기대값을 분리해 넣었다. `431918e`는 49개 참조 이미지에 요청자의 사람 확인을 기록했다. 새 문맥 Opus 검증 2회와 코드 리뷰 뒤 `5775b58`, `f1bc634` 등으로 지적을 고쳤으며 `08bcbc44d`로 머지됐다. [plan@3084414:732–755](https://github.com/bifrost17/openwebagent/blob/3084414a4c9c370fb48d6e3f2c580a0c244f7cca/intent/0021-sqllab-ui-improvements/plan.md#L732-L755). | 49장 확인 기록은 이미지의 출처·마스킹 검토에 해당한다. DBeaver 전사 표본 확인은 #403 본문 당시 **열림**이었고, 이후 요청자가 에이전트에게 위임해 PR-A T11 전 32/32행 불일치 0으로 닫았다고 plan이 기록한다. 사람 본인의 표본 시각 확인은 아니다. [plan@main:59–61,796–798](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0021-sqllab-ui-improvements/plan.md#L796-L798). |
| 선행 기반·API, 9/30 | PR-0 뒤 [#406 PR-E](https://github.com/bifrost17/openwebagent/pull/406)(head `3e74c83b`)와 [#405 PR-A](https://github.com/bifrost17/openwebagent/pull/405)(`fe7862c7`)를 병렬 진행해 E→A 순서로 머지했다. E는 읽기 전용 조회 API·권한/상한과 프런트 클라이언트를 제공하고 화면 소비는 F2로 미뤘다. A는 토큰·표면 컨텍스트·글꼴/아이콘·측정/픽셀 하네스를 제공해 화면 변화 0을 목표로 했다. | E 본문은 Oracle live 미실행과 일부 백엔드 전량 시험 실패를 남긴다. A의 자체 비교는 29개 영역 밖 소비자 중 12개 관찰로 한정됐다. |
| 오른쪽·왼쪽 결합, 9/30–10/1 | [#426 B](https://github.com/bifrost17/openwebagent/pull/426)(`159c2a2c`) 툴바·편집기, [#429 C](https://github.com/bifrost17/openwebagent/pull/429)(`48546260`) 결과·상태, [#430 D](https://github.com/bifrost17/openwebagent/pull/430)(`bcac8a07`) 탭·팝업이 직렬 머지됐다. [#434 R2](https://github.com/bifrost17/openwebagent/pull/434)(`ade06169`)는 B/C 이후 확인된 북쪽 창 3px·모션 차이를 고쳤다. [#424 F1](https://github.com/bifrost17/openwebagent/pull/424)(`1b28e576`) 기본 트리와 [#437 F2](https://github.com/bifrost17/openwebagent/pull/437)(`dcf8ce32`) API 소비는 뒤이어 머지됐다. F1 본문은 부분 구조 10/10, 나머지 54행 미실행; F2는 구조 62/62와 라이브 권한 일부를 기록한다. | B/C/D PR 설명은 하네스·component 결과와 잔여 불일치를 함께 적었다. F1/F2의 Oracle·뷰 일부 라이브는 비어 있었다. 로그·원본 화면을 이 조사에서 재실행·대조하지 않았다. |
| 새 결정·화면 피드백, 10/1–2 | 결합 뒤 [#438](https://github.com/bifrost17/openwebagent/pull/438)(`497db471`)은 실제 SQL 미리보기 모달 가림, 영문 진행 문구, 셀렉트 넘침, 좁은 폭 기록 표를 고쳤다. [#439 D30](https://github.com/bifrost17/openwebagent/pull/439)(`7601f0e3`)은 편집기 우클릭과 ⋮ 메뉴를 하나로, [#441 D31](https://github.com/bifrost17/openwebagent/pull/441)(`79636153`)은 Superset 카드 대신 공용 칩 모양으로 바꿨다. 이후 탭 정렬·여백·실행 단축키, 오류 행과 팝업 가림 관련 PR이 이어졌다(아래 원인별). [plan@main:85–88](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0021-sqllab-ui-improvements/plan.md#L85-L88). | 요청자 결정의 프로젝트 기록은 확인했지만 대화 원문은 별도 확인하지 않았다. “40개 PR=40개 결함”이 아니다. |

PR 번호와 머지 상태는 수집 API의 0021 색인 40개와 bare Git 첫 부모 이력을 함께 확인했다. #403→#406→#405→#426→#429→#430→#434→#424→#437의 **실제 머지 순서**는 [main 첫 부모](https://github.com/bifrost17/openwebagent/commits/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/)에 있다. API의 `reviews: []`는 GitHub review 엔드포인트의 빈 배열일 뿐, 위에 기록된 하위 에이전트·`/code-review`가 없었다는 근거로 쓰지 않는다.

## 제기된 가설의 검토

### UI의 심미성·기존 제품과의 일관성

**부분적으로 맞지만, 초기 요구와 후속 판단을 구분해야 한다.** 9/29 intent의 목표는 오른쪽을 기존 OWUI 색에 맞추는 것이 아니라 Superset SQL Lab에 가깝게 만드는 것이었다. spec은 기존 OWUI 부품·팔레트가 불일치 원인이라고 적고, 오른쪽 표면 컨텍스트를 한정해 공용 부품의 영역 밖 소비자는 보존하도록 설계했다. 동시에 공용 미리보기 탭 줄 자체와 데이터 소스·스키마 선택 구조는 유지한다는 충돌 경계도 적었다. [spec@f3f25dc:8–18,119–142](https://github.com/bifrost17/openwebagent/blob/f3f25dcb0f7f946f2ddd3107f5de2d827d7f4851/intent/0021-sqllab-ui-improvements/spec.md#L119-L142), [intent@b1428ac:35–63](https://github.com/bifrost17/openwebagent/blob/b1428acef7df8e03c2dacadebb6a602b5c34958f/intent/0021-sqllab-ui-improvements/intent.md#L35-L63).

후속 D30·D31은 요청자가 공용 UI와의 일관성을 더 높이도록 기준을 **변경한 사건**이다. D31 구현 #441은 카드용 패리티 짝을 제거하고 공용 칩·탭 줄로 돌아갔음을 설명한다. 10/1 이후 탭 세로 중앙·여백과 오류 카드 모양을 여러 번 조정한 사실은 초기 디자인 선호가 끝까지 고정돼 있지 않았음을 보여 준다. 이를 “초기 설계가 심미성을 전혀 다루지 않았다”로 해석하면 초기의 실측·이미지·색·치수 계약을 지워 버린다. [#441](https://github.com/bifrost17/openwebagent/pull/441), [plan@main:85–88](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0021-sqllab-ui-improvements/plan.md#L85-L88).

**후속 문서 정합성 발견:** [#457](https://github.com/bifrost17/openwebagent/pull/457)(head `fb7476cf2`)은 모든 미리보기 탭의 여백을 바꾸며 plan의 10/1 결정 행에서 D1·D31과 AC03의 공용 탭 줄 불변을 그 범위에 한해 대체한다고 적었다. 그러나 수집된 `main`의 [intent D31](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0021-sqllab-ui-improvements/intent.md#L82)에는 “다른 탭 종류와 탭 줄 자체는 바뀌지 않는다”가, [spec FR04·AC07](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0021-sqllab-ui-improvements/spec.md#L79)에는 탭 줄 유지와 “SQL 탭이 없는 탭 줄의 픽셀 차이 0”이 남아 있다. #457의 변경 파일 목록에도 intent/spec은 없다. 이는 **계획·제품 변경이 상위 계약에 완전히 전파되지 않은 기록 결함**이다. AC03 자체는 영역 밖 소비자 목록을 주로 다루므로 이 행의 실제 충돌은 특히 FR04·AC07·intent D31에 분명하다. [plan@main:88](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0021-sqllab-ui-improvements/plan.md#L88), [PR 파일 목록](https://github.com/bifrost17/openwebagent/pull/457/files).

### HTML 목업과 실제 UI

**0021은 HTML 목업을 정답으로 구현한 사례가 아니다.** PR-0 설계는 Superset 실행 화면을 Playwright로 촬영한 오른쪽 21장, DBeaver 빌드 실행 화면의 왼쪽 28장, 측정 기대값 JSON과 트리 구조 JSON을 사용했다. `design/verification.md`는 0021에 목업 HTML이 없으므로 기존 이미지 gate의 `mockup`을 선택 항목으로 만든다고 명시한다. 이미지 README에는 촬영 경로·상태·크롭/가림·사람 확인을 기록했다. [verification@3084414:50–93,406–455](https://github.com/bifrost17/openwebagent/blob/3084414a4c9c370fb48d6e3f2c580a0c244f7cca/intent/0021-sqllab-ui-improvements/design/verification.md#L406-L455), [images README@3084414:1–34](https://github.com/bifrost17/openwebagent/blob/3084414a4c9c370fb48d6e3f2c580a0c244f7cca/intent/0021-sqllab-ui-improvements/design/images/README.md#L1-L34).

그렇다고 실제 제품 UI가 전부 확인됐다는 뜻은 아니다. A는 비교 하네스 `self`·참조 대조와 방문한 소비자 범위를 분리했고, B는 실행 중 하네스가 실제 Stop 상태를 만들지 못한 한계를 적었다. C는 DB 응답 행 순서가 비결정적이라 self 픽셀 차이가 흔들린다는 원인을 기록했다. R2는 토스트 모션을 **하네스에서** 봤지만 실제 앱 스토어가 그 토스트를 표시하지 않는다는 결함을 발견했고, 별도 [#448](https://github.com/bifrost17/openwebagent/pull/448)로 연결했다. [#405](https://github.com/bifrost17/openwebagent/pull/405), [#426](https://github.com/bifrost17/openwebagent/pull/426), [#429](https://github.com/bifrost17/openwebagent/pull/429), [#434](https://github.com/bifrost17/openwebagent/pull/434). 따라서 “목업 불일치”보다는 **실행 상태·데이터·표면 경계에서 하네스와 실제 제품의 재현 범위가 달랐던 사례**가 더 정확하다.

### 모듈 분할 뒤 늦은 결합, 방법의 선행 정의

**분할과 검증 방법은 대체로 구현 전 정의돼 있었다.** PR-0의 `plan.md`는 A/E 병렬, A→B/C/D 및 E+F1→F2 의존, 오른쪽 {B,C,D}와 왼쪽 {F1,F2}의 보이는 머지 묶음, 레인별 스택·포트·볼륨·자격, 공유 파일 편집 차례, 토큰 파일 b/c/d, 컨텍스트, 하네스의 레인별 시나리오 계약, PR별 최신 main 검증·머지 후 main 재실행을 적었다. 이는 파일 소유 표만 놓은 계획보다 깊다. [plan@3084414:216–269,427–468,567–682](https://github.com/bifrost17/openwebagent/blob/3084414a4c9c370fb48d6e3f2c580a0c244f7cca/intent/0021-sqllab-ui-improvements/plan.md#L567-L682), [verification@3084414:176–260,608–648](https://github.com/bifrost17/openwebagent/blob/3084414a4c9c370fb48d6e3f2c580a0c244f7cca/intent/0021-sqllab-ui-improvements/design/verification.md#L608-L648).

그런데도 결합 후 결함이 나왔다. #438의 가림은 모달이 SQL Lab `z-10` 쌓임 맥락에 갇혀 앱 머리 위로 못 올라온 **전역 화면 계층 경계** 문제였다. #445는 공용 Dropdown의 열림 전환이 `overflow-y`를 지워 목록이 넘치는 **공용 부품 생명주기** 문제였다. #459는 고정 23px 가상 트리에서 긴 오류 행이 다음 행과 겹치는 **동적 콘텐츠와 가상화** 문제였다. #473은 기존 팝업 16곳이 여전히 같은 쌓임 맥락에 갇혀 마스크 이음새가 보인 **소비자 전수 확인 누락**이었다. [#438](https://github.com/bifrost17/openwebagent/pull/438), [#445](https://github.com/bifrost17/openwebagent/pull/445), [#459](https://github.com/bifrost17/openwebagent/pull/459), [#473](https://github.com/bifrost17/openwebagent/pull/473). 이 사건은 계획 부재의 증거라기보다 계획된 비교가 모든 실제 조합·표면 소비자를 덮지는 못했다는 피드백이다.

## 후속 PR을 원인별로 묶은 결과

수집 색인의 0021 PR은 40개이고 이 40개의 API 상태는 모두 `merged`다. 아래 묶음은 같은 증상·원인을 중복 결함으로 세지 않기 위한 것이며, 새로운 요청자 결정은 결함 수정과 분리한다.

| 원인·결정 | 연결 PR과 관측 | 처음 계획에서의 위치/해석 |
|---|---|---|
| 기준·결정 변경 | [#419](https://github.com/bifrost17/openwebagent/pull/419) 모션 D29, [#439](https://github.com/bifrost17/openwebagent/pull/439) 메뉴 D30, [#441](https://github.com/bifrost17/openwebagent/pull/441) 칩 D31, [#457](https://github.com/bifrost17/openwebagent/pull/457) 모든 탭 여백, [#456](https://github.com/bifrost17/openwebagent/pull/456) Alt+Enter | 원래 요구와 다르게 선택한 **후속 결정**이다. 변경 당시 spec/plan·검증을 바꿔야 하는 범위와 단순 버그 수정을 가른다. |
| 제품 표면·공용 소비자 결합 | [#438](https://github.com/bifrost17/openwebagent/pull/438) 모달·셀렉트·기록 표, [#445](https://github.com/bifrost17/openwebagent/pull/445) Dropdown 전환, [#449](https://github.com/bifrost17/openwebagent/pull/449)·[#450](https://github.com/bifrost17/openwebagent/pull/450) 편집기 호스트 여백, [#473](https://github.com/bifrost17/openwebagent/pull/473) 남은 오버레이 16곳 | 선행 설계에 표면 컨텍스트와 영역 밖 보존이 있었으나 실제 포털·호스트·전환·전수 소비자에서 추가 결함이 드러났다. #438과 #473은 같은 계열이지만 #473은 #438이 고치지 않은 소비자 범위를 닫는다. |
| 상태·데이터 재현 충실도 | [#447](https://github.com/bifrost17/openwebagent/pull/447) 샘플 응답 고정, [#448](https://github.com/bifrost17/openwebagent/pull/448) store toast 연결, [#458](https://github.com/bifrost17/openwebagent/pull/458) 실행 중 상태를 실제로 재현하는 하네스, [#454](https://github.com/bifrost17/openwebagent/pull/454)·[#455](https://github.com/bifrost17/openwebagent/pull/455) 단축키 실행 중 가드·번역 JSON | 처음의 “하네스 결과”와 실제 사용자 상태를 같은 것으로 보지 않아야 한다. #455는 번역 원본 갱신 뒤 런타임 JSON 재생성을 빠뜨린 한 건이다. |
| 탭·라벨 시각 조정 | [#442](https://github.com/bifrost17/openwebagent/pull/442)·[#443](https://github.com/bifrost17/openwebagent/pull/443) 제목/진행 단계 세로 정렬, [#444](https://github.com/bifrost17/openwebagent/pull/444) 라벨 폭, [#457](https://github.com/bifrost17/openwebagent/pull/457) 전체 여백 | D30/D31 뒤 공용 탭과 진행 줄을 실제 화면에서 조정한 하나의 디자인 피드백 흐름이다. |
| 트리 오류 행 내용·디자인 | [#453](https://github.com/bifrost17/openwebagent/pull/453) 폭, [#459](https://github.com/bifrost17/openwebagent/pull/459) 가변 높이, [#460](https://github.com/bifrost17/openwebagent/pull/460) 기본 접힘, [#461](https://github.com/bifrost17/openwebagent/pull/461) 테두리, [#462](https://github.com/bifrost17/openwebagent/pull/462) 버튼 위치, [#463](https://github.com/bifrost17/openwebagent/pull/463) 토글 디자인, [#464](https://github.com/bifrost17/openwebagent/pull/464) 다크/링크 색, [#465](https://github.com/bifrost17/openwebagent/pull/465) 기록 | 같은 오류 행을 긴 메시지·가상화·접힘·시각 상태로 반복 다듬은 연속 사건이다. 각 PR을 별개 설계 실패로 세면 원인을 부풀린다. |

## 여섯 축 판정과 템플릿에 돌릴 내용

| 축 | 0021 판정 |
|---|---|
| 의도 보존 | **부분 확인.** 최초 Superset/DBeaver 목표와 보존 제약이 intent에 있고 D17→D20, D1의 탭 카드→D30/D31 공용 메뉴·칩 같은 번복을 기록했다. 다만 #457의 모든 탭 여백 결정은 plan과 제품에 반영됐으나 intent D31·spec FR04/AC07의 이전 불변 문구가 남았다. |
| 설계 충실성 | **부분 확인.** 네 설계 정본·실측·경계와 AC는 구체적이다. PR별 구현 설명과 일부 비교 결과는 정본을 참조한다. 실제 전체 화면·모든 상태의 동등성은 후속 결함 때문에 통과 판정할 수 없다. |
| 계획 실행 가능성 | **강점.** PR-0 이전의 세부 plan, 선행/병렬 계약, 하네스·레인·공유 파일/머지 규칙은 실행 가능한 수준이다. 계획 검토가 조건부였고 미해결 표본 확인도 남겼다는 한계가 있다. |
| PR·병렬 분할 | **실행 확인.** PR-0, A/E 병렬, B/C/D와 F1/F2 선후, 머지 순서가 Git에서 확인된다. 분할 자체가 모달 포털·가변 오류 행 같은 화면 결합 결함을 제거하지는 못했다. |
| 변경 피드백 | **활발하나 비용 큼.** 독립 검토·코드 리뷰, 요청자 화면 피드백, 원인 파악과 시험 보강이 반복됐다. 같은 오류 카드와 탭 줄에 여러 PR이 들었다. 제품의 실제 통합 화면을 보는 간격과 재현 시나리오가 더 중요해 보인다. |
| 검증·보고 정확성 | **범위 구분을 잘한 기록이 많음.** PR 본문은 호스트 시험/CI, mock/live, 실행/미실행, 기존 red/신규 red를 구분한다. 다만 이 조사에서 로그·스크린샷·독립 실행을 재검증하지 않았고 하네스가 실제 Run→Stop·store toast를 놓쳤던 것은 확인된 한계다. |

현재 배포 정본 `tdd-optional/project/`의 [plan 양식](../../../../tdd-optional/project/templates/plan.md), [PROCESS](../../../../tdd-optional/project/docs/PROCESS.md), [검증 방식 가이드](../../../../tdd-optional/project/docs/TESTING-STRATEGY.md), [REVIEW](../../../../tdd-optional/project/REVIEW.md)는 이미 선행 계약·실제 경계·독립 기대·UI 실제 관찰·통합판 검증·미실행 구분을 요구한다. 0021만으로 “템플릿에 병렬 계약/조기 검증 방법이 없다”는 결함을 새로 만들 근거는 없다. **#457의 문서 전파 누락은 당시 프로젝트 실행 결함**으로 볼 수 있으나 현재 템플릿 REVIEW는 후속 결정의 spec·plan 반영을 이미 요구한다. 개선 후보는 프로젝트 실행 기록에서 비교 하네스가 재현한 상태와 실제 제품에서 관찰한 상태, 공용/포털 소비자 전수, 사람의 화면 선호 변경을 PR마다 좁고 명확하게 표시하는 것이다. 반복되는 다른 사례에서도 같은 공백이 확인되면 그때 템플릿 예시나 리뷰 질문의 결함인지 재평가할 수 있다. 새 gate나 PR마다 별도 문서를 늘리는 제안은 이 사례의 근거를 넘는다.

당시 제품 저장소 규칙도 이미 같은 경계를 가리켰다. frozen `main`의 [CLAUDE.md:35–50](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/CLAUDE.md#L35-L50)는 실제 diff에서 T→SP→요구/AC/intent를 의미로 대조하고 수락 기준 변경을 요청자와 조정하라 한다. [GIT-WORKFLOW:28–37](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/docs/GIT-WORKFLOW.md#L28-L37)는 조정 뒤 영향받는 intent/spec/plan 갱신과 커밋 전 대조를, [REVIEW:15–19](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/REVIEW.md#L15-L19)는 코드·시험이 맞아도 필요한 문서 갱신 누락을 발견으로 남기라고 한다. #457의 문제를 “이 지침이 없어서”라고 볼 수 없다. 어떤 검토가 이 diff의 상위 계약까지 실제로 읽었는지는 수집 기록만으로 확인되지 않는다.

모델·검토자 경로도 원인으로 단정하지 않는다. 9/29 plan/spec 검토는 기록상 Codex Astra medium, 9/30 이후는 요청자 지시로 새 문맥 Claude 하위 에이전트(난도별 최대 Opus)와 코드 리뷰를 썼다([plan@3084414:46–48,658–679](https://github.com/bifrost17/openwebagent/blob/3084414a4c9c370fb48d6e3f2c580a0c244f7cca/intent/0021-sqllab-ui-improvements/plan.md#L46-L48)). 어느 모델이 실제 어떤 정본·실제 화면을 읽고 어떤 장애 시나리오를 검토했는지가 미래 평가의 입력이다. 모델 이름이나 “독립 검토 횟수”만으로 UI 결함의 발생·예방을 설명하지 못한다.

## 미확인·제외

- 9/29–10/2의 원래 사용자 대화 transcript, 브라우저 원본 화면/실행 로그의 독립 재생, 배포 뒤 `:3080` 전체 수용 결과는 이 조사에서 확인하지 않았다. plan과 PR 본문이 인용한 요청·결정은 프로젝트 기록의 주장으로 사용했다. `plan.md`가 제공한 Windows에서 여는 **WSL 경로**는 검토 자료 접근 경로일 뿐 개발자 OS를 증명하지 않는다.
- #403 당시 참조 이미지 49장 확인과 DBeaver 전사 62행 검증은 별개의 일이다. 새 문맥 검증자의 62/62행 전사 대조와 요청자 위임 뒤 에이전트가 수행한 32/32행 표본 시각 대조는 plan에 기록됐다. 이는 요청자 본인이 32행을 눈으로 확인했다는 뜻이 아니고, 실제 제품 동등성 검사도 아니다. 이미지 gate의 파일/마스킹 형식 검사와도 구분한다. [#403](https://github.com/bifrost17/openwebagent/pull/403), [plan@main:796–798](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0021-sqllab-ui-improvements/plan.md#L796-L798).
- API 리뷰 목록은 빈 배열이고, 로컬 하위 에이전트·`/code-review`의 원문 로그는 PR·plan 요약을 넘어서 독립 확인하지 않았다. 일부 PR의 테스트 통과/기존 red/미실행은 진술을 인용한 것이며 현행 `main` 전체 품질 승인으로 환산하지 않는다.
- 0021과 무관한 후속 제품 결함, 현재 템플릿의 변경 효과, 실제 사용자 만족도/심미성 최종 수락은 **미검토 또는 증거 부족**이다.
