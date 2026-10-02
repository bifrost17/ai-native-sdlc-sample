# 0017 — SQL Lab 이식본 결함과 의도 불일치

판정: **주요 문서·인도·후속 수정 검토 완료, 실행 로그/시각 품질의 독립 판정은 제한됨.** 가장 큰 다중 PR 사례다. 요청자의 U1~U36과 선행 잔여 R1~R6을 문서 PR로 먼저 고정했지만, 실제 UI 관찰과 통합에서 추가 정정이 여러 번 나왔다. 이것을 전부 초기 설계 결함으로 세면 후속 사용자 결정·실환경 발견·게이트 자체 결함을 혼동한다.

고정 원본은 `.local/research/openwebagent-template-history/20261003/collection/` inventory·API·bare Git, 초기 main `a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e`다. 아래 PR 본문 수치·브라우저 관찰은 원시 로그가 없는 보고자의 진술로 표시한다. PR 리뷰 API의 빈 결과를 리뷰가 없었다는 뜻으로 쓰지 않는다.

## 최초 요구와 문서 인도

[`550435c`](https://github.com/bifrost17/openwebagent/commit/550435c8e01) intent 초안 뒤 U 항목과 R 잔여가 다수의 문서 커밋으로 추가됐다. 예를 들어 [`f251b6e`](https://github.com/bifrost17/openwebagent/commit/f251b6e1e3d)는 탐색기와 편집기 분리, [`937304b`](https://github.com/bifrost17/openwebagent/commit/937304b700f)는 등록된 데이터 소스를 실행기에 즉시 반영하는 U26을 기록했다. [`f965cf5`](https://github.com/bifrost17/openwebagent/commit/f965cf5e7d6)는 자율 진행·GitHub Flow·권장안 선택의 요청자 결정을 남겼다. frozen intent `:15-67,85-102`가 최종 U/R/D 목록이다. 최초 계획의 범위가 처음부터 고정돼 있었다는 뜻은 아니다.

[`352cf98`](https://github.com/bifrost17/openwebagent/commit/352cf98b19c)는 진입 spec과 A1 탐색기·A2 편집기·A3 팝업/관리자·A4 Text2SQL/실행기 설계 네 편을 추가했다. [`51dc5f1`](https://github.com/bifrost17/openwebagent/commit/51dc5f1d192)과 [`9c44023`](https://github.com/bifrost17/openwebagent/commit/9c4402390ac)는 설계 검토 발견과 반영 키·세대 동시성·코어 가드 등 공유 계약을 수정했다. [`135ce38`](https://github.com/bifrost17/openwebagent/commit/135ce389aef)는 PR-0~9·T01~41 계획을, [`0e1cf30`](https://github.com/bifrost17/openwebagent/commit/0e1cf308522)는 인계 검토의 jsdom 장치·36개 Dropdown 소비처·병렬 겹침을 반영했다. [PR #346](https://github.com/bifrost17/openwebagent/pull/346)은 이 문서만 [`589ce74`](https://github.com/bifrost17/openwebagent/commit/589ce7489)로 먼저 머지했다. spec `:88-133`의 AC→설계 색인과 plan `:106-244,1270-1305`의 PR 지도·공통 검증·Proof는 구현자가 나눠 착수할 수 있는 수준이다. 다만 문서 PR 본문의 “리뷰 통과”는 원응답 미수집으로 독립 확인되지 않는다.

## 구현·통합·후속 사건

| 흐름 | 근거와 관측 경계 |
|---|---|
| 공용 UI와 탐색기 | [#348](https://github.com/bifrost17/openwebagent/pull/348) PR-1은 공용 Dropdown 소비처 36개, 팝업 프리셋·우클릭·아이콘과 관련 시험을; [#351](https://github.com/bifrost17/openwebagent/pull/351) PR-2는 스키마 개수 API, 별/아이콘, 우클릭 메뉴·상세 팝업을 착지시켰다. #351 본문은 검증자가 개수 배지 미배선을 찾아 고쳤고 실 SingleStore 라이트/다크 캡처를 보고한다. 프런트 시험·빌드·브라우저 수치는 본문 진술이며 캡처 원본은 미수집이다. |
| 편집기·상세·관리자 | [#354](https://github.com/bifrost17/openwebagent/pull/354) PR-3은 편집기 자체 대상 선택·Ctrl+Enter·한글/커서, [#352](https://github.com/bifrost17/openwebagent/pull/352) PR-4는 상세 스피너·컬럼 표·목록 모달·1792년 표시, [#350](https://github.com/bifrost17/openwebagent/pull/350) PR-5는 관리자 팝업·좌측 탭이다. 숫자 순서와 **실제 머지 순서는 다르다**: #350 [`488decf`](https://github.com/bifrost17/openwebagent/commit/488decf50f) → #352 [`8858e6d`](https://github.com/bifrost17/openwebagent/commit/8858e6dfe5) → #354 [`ce79341`](https://github.com/bifrost17/openwebagent/commit/ce793414d4). #354 본문은 Windows Chrome 한국어 IME와 Ctrl+Enter의 요청자 실환경 판정을 남긴다. |
| 실행기와 Text2SQL | [#349](https://github.com/bifrost17/openwebagent/pull/349) PR-6은 데이터 소스 저장 뒤 실행기 밀기, 세대·영수증·코어 적용 가드와 배포 배선을; [#353](https://github.com/bifrost17/openwebagent/pull/353) PR-7은 스키마별 저장·권한·SQL 한정과 화면 설정을 바꿨다. #349 본문은 라이브 `singlestore-net`을 통한 코어 :9100 우회 가능성과 수정 뒤 실스택 재측정·브라우저 미실행을 명시했다. 후속 [#361](https://github.com/bifrost17/openwebagent/pull/361)이 실제 :3080 경로에서 웹 티어→코어 `/internal/targets` 200 우회를 404로 닫았고, [#362](https://github.com/bifrost17/openwebagent/pull/362)가 일회용 반영 컨테이너의 read-only/no-new-privileges를 보강했다. 이는 공유 망·보안 경계의 늦은 통합 발견이다. |
| 잔여·시각 정정 | [#347](https://github.com/bifrost17/openwebagent/pull/347) PR-8은 쓰기 라우트 이벤트 루프 정지와 `server_cert` 배선, [#356](https://github.com/bifrost17/openwebagent/pull/356) PR-9는 색·좁은 폭·로고·Text2SQL 요청자 정정을 다뤘다. 그 뒤에도 [#357](https://github.com/bifrost17/openwebagent/pull/357) 아이콘 원본, [#358](https://github.com/bifrost17/openwebagent/pull/358) 좁은 편집기 툴바의 글자 세로 깨짐, [#359](https://github.com/bifrost17/openwebagent/pull/359) 720px 아이콘화·560px 탐색기 자동 닫힘이 이어졌다. #358은 실브라우저 좁은 폭 캡처 미실행을 적고 #359는 dev 스택 관찰을 보고한다. PR-9를 “최종 UI 수락”으로 읽으면 안 된다. |
| 게이트 결합 | [#360](https://github.com/bifrost17/openwebagent/pull/360)은 SQL Lab 결함과 함께 게이트의 자원 기동 시점·worker 수·UID·고정 이미지 아키텍처·CSS 토큰 문제를 수정했다. 본문은 dev 프로필 95 gate 첫 회차 93 통과·2 실패와 수정 후 시험 통과를 보고한다. 이것은 관련 PR들이 각각 요청자 지시로 full gate를 생략한 사실을 소급해 지우지 않는다. plan `:1232-1247`의 통합 보완 기록과 본문을 별도 층으로 읽어야 한다. |

## 여섯 축

| 축 | 판정 |
|---|---|
| 의도 보존 | **대체로 충족, 변경 누적.** U/R 목록과 D 결정이 최초 문서 PR에 반영됐고 후속 사용자 결정은 #356·#359 등에 다시 반영됐다. U5의 “탐색기 선택 = 편집기 대상” 과거 0011 계약은 0017에서 **명시적으로 대체**됐다(spec `:23-25`, plan T12~13 `:514-551`). 과거 spec을 현행 정본으로 인용하면 잘못이다. |
| 설계 충실성 | **핵심 계약은 정적 추적 가능, 화면 수락 제한.** spec A1~A4와 plan T별 파일·AC가 각 PR 설명·diff로 이어진다. #361·#362의 보안 보완, #358·#359의 좁은 폭 정정은 최초 설계·검증에서 덜 본 경계다. |
| 계획 실행성 | **착수 가능했으나 현재 기록 낡음.** PR 선행·겹침·핸드오프·관련 시험·브라우저 절차가 plan `:133-244`에 있다. frozen plan 머리 `:11-20`은 아직 “계획 작성 단계, 모든 구현 T 미실행, 다음 T01”이라고 말한다. 후반 T 문단에는 실행 기록이 섞여 있어 **plan 머리나 과거 spec 상태를 현재 요약으로 쓰면 오판**한다. 같은 PR이나 같은 커밋의 문서·코드만으로 선행 갱신은 증명하지 않는다. |
| PR·병렬 분할 | **분할은 구체적, 결합 판은 단계적.** PR-0 선행과 A1~A4·공용 UI·실행기 경계가 제시됐다. 실제 #347~#354는 번호 순이 아닌 겹침 머지였고, #361의 :3080 공유 망 우회는 PR-6의 모듈별 검증만으로 통합 보안을 닫지 못했음을 보여 준다. |
| 변경 피드백 | **풍부함.** 검토 발견, 요청자 수정, 브라우저 좁은 폭, 실운영 망 우회가 후속 PR로 이어졌다. 하지만 PR-9 이후 #357~#362는 “최종”이라는 요약을 무효화했으므로 인계 현행성은 약하다. |
| 검증·보고 | **증거 층이 다양하나 최종 전체 증명은 제한됨.** PR마다 관련 시험·빌드·브라우저를 다르게 수행했고 full gate는 사용자 지시로 다수 생략했다. #360의 게이트 보완 보고는 별도다. 캡처·원시 로그·실환경 IME 입력·실DB TLS·일부 AC는 미수집 또는 미실행으로 남는다. 본문 숫자를 독립 통과로 옮기지 않는다. |

H1: 최초 문서화와 교차 리뷰에도 후속 수정이 있었다. 좁은 폭과 공유 망 가드는 초기에 덜 구체화한 설계/검증 경계로 지지된다. 아이콘·로고·화면 선택의 요청자 재결정은 초기 결함과 구별한다. H2: #358→#359의 실제 분할 폭 문제는 컴포넌트 시험·시안만으로 심미성과 배치 품질이 닫히지 않는다는 강한 사례다. 캡처 원본과 사람의 최종 수락은 미수집이다. H3: PR-6의 코어 가드가 `singlestore-net` 공용 경로를 놓친 것은 전체 배포 네트워크 시퀀스 검증 부족을 지지한다. 반면 PR-7의 스키마 전달·권한은 설계와 리뷰가 fail-open을 찾아 보완했다. H4: 각 T의 시험 방법은 구체적이었지만 실환경·좁은 폭·전체 게이트의 사후 누락이 남았다. “방법 문구 부재”보다 **대표 입력/환경 선택과 실제 실행 범위** 문제로 좁혀야 한다.

당시 지침의 실제 설치·호출은 세션 원문 없이 미확인이다. 현재 0.1.8 원본은 공유 계약·UI 상태·실화면 관찰·통합 검증·갱신 기록을 이미 요구한다([baseline](../baseline.md)). 기존 WIP 5파일은 계획 구체성의 정책 진입점 보강이며 이 사건을 소급해 해결한 판이 아니다. 원인 후보는 제품 설계, 요청자 후속 결정, 모델/레인 실행, 게이트 환경, 증거 범위로 나눠야 한다. 새 일괄 문서·도식 의무의 근거로 삼지 않는다.
