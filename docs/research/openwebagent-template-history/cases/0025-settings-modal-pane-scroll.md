# 0025 — 설정 팝업의 독립 스크롤과 OWUI 프레임

판정: **검토 완료, 애니메이션 실제 재생은 미확인.** 0023과 [PR #421](https://github.com/bifrost17/openwebagent/pull/421)을 공유한다. 이 문서는 프레임·스크롤 책임과 0023의 화면 내용이 만나는 접점만 평가한다. 수집 원본 main은 `a08295f`.

| 단계 | 근거와 관찰 |
|---|---|
| 요청·설계 | `a08295f:intent/0025-settings-modal-pane-scroll/intent.md:4-15`: 좌측·우측이 함께 스크롤되고 머리 여백·닫기·애니메이션이 OWUI와 맞지 않는다는 요청. 당시 실제 팝업별 닫힘은 미확인이라고 명시한다. `spec.md:5-13,18-23,44-64`는 `SqlLabModalFrame`의 기존 본문 wrapper `overflow-y-auto`를 원인으로 보고 `owuiStyle` 옵트인 + `SettingsPopupLayout/Header`로 책임을 옮긴다. 기존 SQL Lab 소비자 불변 FR05가 경계다. |
| 초기 Git 판·구현 | [`dd25526d2e`](https://github.com/bifrost17/openwebagent/commit/dd25526d2e00904550e3db6d6acca0750712d964)에서 0023과 함께 프레임·공통 컴포넌트·시험이 들어왔고 [`82f1a7aad`](https://github.com/bifrost17/openwebagent/commit/82f1a7aad38eea1ccd4eb6f388f2c3e5f0f99def)에 문서가 기록됐다. `plan.md:25-53`은 T01 프레임, T02 공용 부품, T03 두 소비자 연결을 분리한다. 최초 기록 문서가 이미 완료 수치를 담아 실제 문서 선행/TDD 실행 순서는 별도 로그 없이는 미확인이다. |
| 검토 중 범위 교정 | `plan.md:54-64`: 독립 검토가 md 미만 높이·검색칸 잘림·과도한 Esc 차단을 찾았다. md 미만 전용 코드는 사용자 “모바일 폭 할필요없어” 결정으로 제거했다. 열린 listbox에서 Esc가 팝업까지 닫혀 초안을 잃는 경로와 부모 `{#if}` 전환의 `|global`을 시험에 추가했다. 0023 FR14 body 포털도 프레임 계약에 기록했다. |
| PR 리뷰·통합 | [`d819801`](https://github.com/bifrost17/openwebagent/commit/d819801ae6c5bc7da7eb58eaa6fa4c6703d929cd) 1차는 `owuiStyle=false`의 기존 SQL Lab Esc를 복원했고, [`8a663b7`](https://github.com/bifrost17/openwebagent/commit/8a663b7f1ab72a8bf4870768ec6c2cf509082f48) 2차는 캡처에서 차단만 판정하고 버블에서 `defaultPrevented`/IME를 보고 닫게 했다(`plan.md:66-82`). #421은 [`1c02888`](https://github.com/bifrost17/openwebagent/commit/1c02888e0747691a9823df957144bc24cdb95711)에 머지. 후속 0027에서 실브라우저가 OWUI 앱 전역 Esc `preventDefault`와 충돌해 실제 팝업이 닫히지 않는 결함을 발견해 [`1f8d3a3`](https://github.com/bifrost17/openwebagent/commit/1f8d3a3dcd8e4f35a6b5a466eacd6e29d5a647fd) 이후 프레임을 수정했다(`0027 plan.md:256-260`). 따라서 #421 시점 Esc 전체 성공을 현재 화면으로 소급하지 않는다. |
| 검증 범위 | `0025 plan.md:84-98,107-114`: 수정 전 4파일 48시험, 프레임/레이아웃/소스 계약 RED, 집중 165파일 1769·T05 후 166파일 1924시험을 보고한다. Chromium 1440×900 앱에서 750px 패널, 좌측 1020px 내용을 684px 안에서 스크롤해도 우측 `scrollTop` 불변, overlay 0, Esc·바깥 클릭을 관측했다. 빈 임시 백엔드·라이트 모드·정지 캡처라 애니메이션은 직접 보지 못했다. 전체 프런트 9실패는 수정 전 별도 worktree의 같은 실패로 비교했다고 문서가 밝힌다. |

여섯 축: **의도 보존**은 독립 스크롤·공용 머리·기존 SQL Lab 기본 경계에 연결된다. **설계 충실성**은 현재 `SqlLabModalFrame.svelte:42-66,77-118,157-178`의 옵트인·전환·Esc 경로로 정적 확인된다. **계획 실행 가능성**은 AC01–10의 클래스/브라우저 역할 구분이 좋았으나 처음 앱 전역 Esc 간섭까지 모델링하지 못했다. **PR 경계**는 0023 FR14와 공통 파일 때문에 합친 이유가 문서에 명확하다. **변경 피드백**은 검토 두 회차와 0027 실브라우저 발견을 수용했다. **검증·보고**는 CSS 클래스 시험, 소스 문자열 시험, 브라우저 스크롤 실측, 전환 호출 시험을 각기 한정해 보고한다. 명령 출력 원본은 이번 조사에 없다.

사용자 가설: H1은 **부분 지지**(Esc 우선순위·md 폭을 구현 검토에서 구체화), H2는 **지지**(코드/캡처는 맞아도 실제 앱 전역 핸들러가 Esc 동작을 깨뜨림), H3는 **후속 통합 결함**(0027이 재사용할 때 드러났고 그 PR에서 수정; 계획된 병렬 모듈 충돌 증거는 없음), H4는 **부분 지지**(실브라우저 관찰은 있었으나 전역 앱 간섭을 늦게 발견). 원인은 프레임과 앱 전역 이벤트의 상호작용·검증 환경 차이다. 현재 배포 0.1.8과 WIP plan 양식은 독립 기대와 실제 결과·한계 구분을 이미 요구한다. 이 사례만으로 새 템플릿 규칙을 제안하지 않는다.

근거 부족: 열림 애니메이션 눈 관측, 다크/모바일 폭, 실제 프로세스 rc와 검토 원응답은 없다. 0027의 Sonnet·Opus 표기는 문서/PR의 주장으로 읽고 실행 모델을 브랜치명에서 추정하지 않는다.
