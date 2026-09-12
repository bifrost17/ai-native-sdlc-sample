# 유명 웹 프로젝트의 TDD·구현 후 테스트 정책과 PR 이력

조사 기준일은 2026-09-12, 병합 대상 기간은 UTC `2024-09-12T00:00:00Z`부터 `2026-09-12T23:59:59Z`까지다. 실제 API 관찰은 `2026-09-12T07:48:59Z`까지이므로 그 뒤 같은 날 병합된 변경은 포함할 수 없다. 결론부터 말하면, 다섯 프로젝트는 모두 테스트를 중요한 병합 조건으로 다루지만 **확인한 공식 문서에는 일반적인 TDD(red-green-refactor) 순서 의무가 명시되지 않았다**. Django·Rails·Next.js는 버그 수정에서 “수정이 없으면 실패하는 테스트”를 명시한다. React는 버그 수정과 새 기능에 테스트를 요구하고, GitLab은 적절한 테스트·회귀 테스트·CI 통과를 요구한다. 이 요구는 테스트의 판별력에 관한 것이며 테스트 코드를 먼저 커밋하라는 규칙은 아니다.

실제 표본도 “TDD를 쓴다/구현 후 테스트를 쓴다”는 양자택일 결론을 허용하지 않는다. 45건 중 37건은 첫 관련 커밋에 코드와 테스트가 같이 있어 로컬 작성 순서를 알 수 없었다. 구현 커밋 다음에 테스트 커밋이 보인 사례는 Next.js #98506 한 건이고, 나머지 7건은 관련 테스트 파일을 바꾸지 않았다. 테스트 전용 커밋이 관련 구현보다 먼저 나온 표본은 없었다. 이 수치는 엄밀한 모집단 비율이 아니라 아래에 저장한 검색 후보 안에서 고른 사례의 기술적 요약이다.

## 공식 정책: 테스트 의무, 실패 재현, 일반 TDD를 분리

| 프로젝트 | 테스트 포함·통과 요구 | 수정 전 실패를 확인하라는 요구 | 일반 TDD 순서 의무 |
|---|---|---|---|
| Django | 좋은 수정에는 회귀 테스트가 포함되어야 하고 전체 테스트 스위트가 통과해야 한다. [원문 110–117, 486](../originals/projects-web/django-submitting-patches.txt) | 버그 리뷰 체크리스트가 “수정 적용 전 실패해야 한다”고 명시한다(505–506행). | 저장한 공식 기여·테스트 문서에는 `TDD`, `test-driven`, `red-green` 의무가 없다. |
| Rails | 코드 기여에 테스트를 포함하고 영향받는 컴포넌트 테스트를 통과시키도록 한다. 전체 스위트를 push 전에 돌리는 것은 관례가 아니라고도 명시한다(337–346행). [전체 원문](../originals/projects-web/rails-contributing-guide.md) | 테스트는 코드 없이는 실패하고 코드와 함께 통과해야 한다(281행). 버그 보고용 실행 테스트도 현재 코드에서 실패해야 한다(52행). | 테스트를 먼저 작성·커밋하라는 일반 순서는 없다. |
| React | 버그 수정이나 테스트할 코드에는 테스트를 추가하고(203행), 새 기능 PR에는 단위 테스트가 필요하다(254행). `main`의 테스트 통과와 PR 전 테스트 실행도 요구한다. [공식 기존 가이드](../originals/projects-web/react-legacy-how-to-contribute.html) | 축소 재현 사례를 권하지만, 저장한 공식 문서에는 테스트가 수정 없이 실패해야 한다는 명시적 PR 규칙은 없다. | 일반 TDD 순서 의무가 없다. 현재 [CONTRIBUTING](../originals/projects-web/react-CONTRIBUTING.md)은 이 기존 공식 가이드를 가리킨다. |
| Next.js | 테스트 종류·작성법·CI 동작을 규정한다. 다만 루트 기여 문서는 모든 코드 PR에 새 테스트를 넣으라는 포괄 문구를 두지 않는다. [기여 안내](../originals/projects-web/nextjs-contributing.md), [테스트 가이드](../originals/projects-web/nextjs-testing.md) | “수정을 적용할 때 수정 없이는 테스트가 실패하는지 확인”하라고 명시한다(77–78행). | 일반 TDD 순서 의무가 없다. |
| GitLab | MR은 적절한 테스트를 포함하고 모두 통과해야 하며, 새 클래스에는 단위 테스트가 있어야 한다(167–169행). 버그·회귀는 재발 위험을 낮추는 테스트로 덮는다(269–274행). [MR workflow](../originals/projects-web/gitlab-merge-request-workflow.md) | 현재 버그를 드러내는 테스트만 제출하는 것도 받는다고 하므로 실패 재현을 장려하지만, 모든 수정에 대해 별도의 선행 실패 실행을 기록하라는 문구는 없다. | [testing strategy](../originals/projects-web/gitlab-testing-strategy.md)의 “Shift Left”는 파이프라인에서 더 일찍 실행하라는 뜻이며 red-green 작성 순서 규칙이 아니다. |

정책 원문은 기본 브랜치 커밋에 고정해 [원문 목록과 출처](../originals/projects-web/README.md)에 전체 저장했다. React 기존 웹 가이드만 커밋 고정판을 제공하지 않아 HTTP 헤더와 SHA-256으로 조회 시점을 보존했다.

## 표본과 판정 방법

변경 유형은 제목만으로 기계 분류하지 않았다. 기능은 새 사용자/API/플랫폼 능력, 버그 수정은 관찰된 잘못된 동작의 교정, 리팩터는 의도한 외부 동작을 유지하는 내부 구조 변경으로 읽었다. 성능 개선이 주목적인 변경은 리팩터에서 제외했다. GitLab은 공식 `type::feature`, `type::bug`, `maintenance::refactor` 라벨을 우선했고 본문과 diff로 확인했다. 각 유형에서 **저장한 검색 후보 안에서** 실제 `merged_at` UTC가 최신인 적격 2건을 기본 표본으로 골랐다. 기본 6건 중 순서를 알 수 없는 사례가 네 건 이상이면 유형별 다음 한 건을 더했다. 다섯 프로젝트가 모두 이 조건을 충족해 프로젝트당 9건, 총 45건이다. 후보 API의 첫 100건과 제목 검색 바깥까지 포함한 전체 모집단의 진짜 최신 적격 PR을 보장하지 않는다.

봇 작성, 문서만 변경, 생성물만 변경, backport, 테스트만 변경, CI만 변경한 PR/MR은 제외했다. 저장한 후보 목록은 API의 실제 첫 100건이며 완전한 2년 모집단이라고 주장하지 않는다. Django·Rails·Next.js의 리팩터 후보는 전체 기간에 대한 제목 검색 결과도 따로 저장했다. GitHub Search가 `facebook/react` 날짜 쿼리에 HTTP 422를 반환해 React는 공식 Pulls API 최근 결과를 `merged_at`으로 로컬 정렬했다. [후보·표본 manifest](../data/web-projects/manifest.json)와 [후보 판정 기록](../data/web-projects/candidate-decisions.json)에 쿼리 한계, 분류·제외 이유와 모든 근거 파일 경로가 있다.

순서 판정은 다음처럼 제한했다.

- **same-commit unknown:** 첫 관련 커밋에 구현과 테스트가 함께 있다. 이를 “테스트 후 작성”으로 부르지 않았다.
- **implementation-then-test commits:** 구현만 바꾼 커밋 뒤에 관련 테스트 커밋이 있다. 공개 커밋 순서일 뿐 로컬 편집 순서의 증명은 아니다.
- **test-first visible without failure confirmation:** 관련 테스트 전용 커밋이 해당 구현 커밋보다 앞에 있지만, 그 시점 실패를 확인하는 CI나 작성자 보고가 없다.
- **existing tests only:** 관련 테스트 파일은 바뀌지 않았다. 저장한 CI 상태는 기존 검사를 실행했다는 범위의 근거이며 특정 동작의 충분한 커버리지 증명은 아니다.
- force-push, rebase, squash, amend 및 커밋 전 로컬 작업은 GitHub/GitLab 이력에서 복구할 수 없다.

## Django: 7 same-commit unknown, 2 existing-tests only

| 유형 | PR과 병합 시각 UTC | 관찰된 순서 근거 |
|---|---|---|
| 기능 | [#20842](https://github.com/django/django/pull/20842), `2026-09-08T19:01:03Z` | 관리자 아이콘·문서 이미지만 한 커밋에서 변경. 테스트 파일 없음 → existing tests only. [JSON](../data/web-projects/django/pr-20842.json) |
| 기능 | [#21875](https://github.com/django/django/pull/21875), `2026-09-04T19:43:51Z` | `qualname` 구현과 단위 테스트가 커밋 `e715dcb`에 함께 있음 → same-commit unknown. [JSON](../data/web-projects/django/pr-21875.json) |
| 기능·확장 | [#21886](https://github.com/django/django/pull/21886), `2026-09-04T18:19:15Z` | 대상 calendar-version 코드와 테스트가 `566a88c`에 함께 있음. 앞선 middleware 커밋은 별도 이슈 → same-commit unknown. [JSON](../data/web-projects/django/pr-21886.json) |
| 버그 | [#21881](https://github.com/django/django/pull/21881), `2026-09-08T16:45:55Z` | raster 수정과 회귀 테스트가 `f862a42`에 함께 있고 사전 실패 실행 보고는 없음 → same-commit unknown. [JSON](../data/web-projects/django/pr-21881.json) |
| 버그 | [#21482](https://github.com/django/django/pull/21482), `2026-09-07T15:02:23Z` | ModelFormSet 수정과 테스트가 `1ce3f82`에 함께 있음 → same-commit unknown. [JSON](../data/web-projects/django/pr-21482.json) |
| 버그·확장 | [#21064](https://github.com/django/django/pull/21064), `2026-09-04T21:24:26Z` | deconstruction 동작과 테스트가 `1fe04df`에 함께 있음 → same-commit unknown. [JSON](../data/web-projects/django/pr-21064.json) |
| 리팩터 | [#21696](https://github.com/django/django/pull/21696), `2026-08-03T14:27:35Z` | fetch-mode rename과 영향 테스트가 `5873f9e`에 함께 있음 → same-commit unknown. [JSON](../data/web-projects/django/pr-21696.json) |
| 리팩터 | [#21519](https://github.com/django/django/pull/21519), `2026-07-13T19:01:16Z` | MiddlewareMixin 이동과 테스트가 `e3a0042`에 함께 있음 → same-commit unknown. [JSON](../data/web-projects/django/pr-21519.json) |
| 리팩터·확장 | [#21507](https://github.com/django/django/pull/21507), `2026-06-17T17:44:38Z` | 내부 helper rename만 `5da2f8b`에서 변경, 테스트 파일 없음 → existing tests only. [JSON](../data/web-projects/django/pr-21507.json) |

대표 제외는 테스트만 고친 #21900, 문서만으로 GEOS 지원을 확인한 #21897, 지원 제거 유지보수 #21929, CI 통합 #21597이다. 선택 표본의 헤드 check-runs 응답은 저장했으며 조회된 check run은 success/skipped였지만 #21875·#21886의 combined status는 조회 당시 pending이었다. 과거 병합 게이트 전체가 성공했다고 확대 해석하지 않았다.

## Rails: 7 same-commit unknown, 2 existing-tests only

| 유형 | PR과 병합 시각 UTC | 관찰된 순서 근거 |
|---|---|---|
| 기능 | [#58710](https://github.com/rails/rails/pull/58710), `2026-09-11T18:40:23Z` | Ractor time-zone 기능과 테스트가 `bc4924a`에 함께 있음 → same-commit unknown. [JSON](../data/web-projects/rails/pr-58710.json) |
| 기능 | [#58668](https://github.com/rails/rails/pull/58668), `2026-09-10T21:23:22Z` | reflection CoW 지원과 테스트가 `a791f84`에 함께 있음 → same-commit unknown. [JSON](../data/web-projects/rails/pr-58668.json) |
| 기능·확장 | [#58695](https://github.com/rails/rails/pull/58695), `2026-09-08T22:35:15Z` | 다섯 capability 커밋이 각각 코드와 테스트를 함께 가짐 → same-commit unknown. [JSON](../data/web-projects/rails/pr-58695.json) |
| 버그 | [#58747](https://github.com/rails/rails/pull/58747), `2026-09-11T23:20:55Z` | Ractor safety 수정과 테스트가 `0b733df`에 함께 있음 → same-commit unknown. [JSON](../data/web-projects/rails/pr-58747.json) |
| 버그 | [#53403](https://github.com/rails/rails/pull/53403), `2026-09-11T20:52:46Z` | 최초 관련 커밋 `e1d2f20`에 수정과 테스트가 함께 있고 이후 test-only 보정이 있음 → same-commit unknown. [JSON](../data/web-projects/rails/pr-53403.json) |
| 버그·확장 | [#58711](https://github.com/rails/rails/pull/58711), `2026-09-10T21:18:17Z` | reloader write 수정과 테스트가 `b68b28f`에 함께 있음 → same-commit unknown. [JSON](../data/web-projects/rails/pr-58711.json) |
| 리팩터 | [#58735](https://github.com/rails/rails/pull/58735), `2026-09-11T05:28:42Z` | method move 구현 파일만 변경 → existing tests only. [JSON](../data/web-projects/rails/pr-58735.json) |
| 리팩터 | [#58673](https://github.com/rails/rails/pull/58673), `2026-09-05T01:32:39Z` | 여섯 리팩터 커밋마다 코드와 관련 테스트가 함께 있음 → same-commit unknown. [JSON](../data/web-projects/rails/pr-58673.json) |
| 리팩터·확장 | [#58497](https://github.com/rails/rails/pull/58497), `2026-08-17T00:18:16Z` | constructor 단순화 구현 파일 하나만 변경 → existing tests only. [JSON](../data/web-projects/rails/pr-58497.json) |

문서 전용, dependency bump, dead-task 제거, test-only 정리와 성능 개선이 주목적인 #58719는 제외했다. 아홉 PR의 저장된 헤드 check runs는 각각 세 건이 모두 success였다. 이는 PR 내 각 커밋에서 red-green을 실행했다는 증거가 아니다.

## React: 8 same-commit unknown, 1 existing-tests only

| 유형 | PR과 병합 시각 UTC | 관찰된 순서 근거 |
|---|---|---|
| 기능 | [#37513](https://github.com/facebook/react/pull/37513), `2026-09-11T09:22:40Z` | compiler 기능과 fixtures/tests가 첫 관련 커밋 `686c4ce`에 함께 있음 → same-commit unknown. [JSON](../data/web-projects/react/pr-37513.json) |
| 기능 | [#37339](https://github.com/facebook/react/pull/37339), `2026-09-02T15:58:53Z` | nonce 코드와 첫 테스트가 `dfc86f3`에 함께 있고 이후 test-only 사례가 추가됨 → same-commit unknown. [JSON](../data/web-projects/react/pr-37339.json) |
| 기능·확장 | [#37491](https://github.com/facebook/react/pull/37491), `2026-09-02T15:47:17Z` | Canary flag 구현 파일만 변경 → existing tests only. [JSON](../data/web-projects/react/pr-37491.json) |
| 버그 | [#37579](https://github.com/facebook/react/pull/37579), `2026-09-11T13:24:42Z` | 첫 커밋에 DOM 수정과 회귀 테스트가 함께 있고 후속은 구현 정리 → same-commit unknown. [JSON](../data/web-projects/react/pr-37579.json) |
| 버그 | [#37539](https://github.com/facebook/react/pull/37539), `2026-09-09T12:06:01Z` | 두 Rust 커밋 모두 구현과 fixture test가 함께 있음 → same-commit unknown. [JSON](../data/web-projects/react/pr-37539.json) |
| 버그·확장 | [#37545](https://github.com/facebook/react/pull/37545), `2026-09-08T22:40:40Z` | 정수 변환 수정과 테스트가 `f851a61`에 함께 있음 → same-commit unknown. [JSON](../data/web-projects/react/pr-37545.json) |
| 리팩터 | [#37574](https://github.com/facebook/react/pull/37574), `2026-09-11T10:07:17Z` | feature flag 정리와 영향 테스트가 `470697d`에 함께 있음 → same-commit unknown. [JSON](../data/web-projects/react/pr-37574.json) |
| 리팩터 | [#37573](https://github.com/facebook/react/pull/37573), `2026-09-10T17:24:22Z` | 첫 cleanup 커밋에 코드와 테스트가 함께 있고 이후 test gate 보정 → same-commit unknown. [JSON](../data/web-projects/react/pr-37573.json) |
| 리팩터·확장 | [#37550](https://github.com/facebook/react/pull/37550), `2026-09-09T13:21:54Z` | RN global 이동과 test update가 `ed5b897`에 함께 있음 → same-commit unknown. [JSON](../data/web-projects/react/pr-37550.json) |

changelog/release 준비, 문서, CI·publish workflow, test-only #37213은 제외했다. Search API 422 때문에 저장한 Pulls API 100건보다 오래된 같은 시각대 후보를 완전히 열거했다고 주장하지 않는다. 작은 PR은 전체 check runs가 success/skipped였고 큰 PR은 API 첫 100개가 success였지만 `total_count`가 240대인 사례가 있어 남은 run의 상태를 추정하지 않았다.

## Next.js: 7 same-commit unknown, 1 implementation-then-test, 1 existing-tests only

| 유형 | PR과 병합 시각 UTC | 관찰된 순서 근거 |
|---|---|---|
| 기능 | [#98532](https://github.com/vercel/next.js/pull/98532), `2026-09-11T19:05:04Z` | loader mode와 테스트가 첫 커밋 `639e22a`에 함께 있고 후속은 테스트 재구성 → same-commit unknown. [JSON](../data/web-projects/nextjs/pr-98532.json) |
| 기능 | [#98571](https://github.com/vercel/next.js/pull/98571), `2026-09-11T17:58:23Z` | image optimizer 설정과 테스트가 `67adc98`에 함께 있음 → same-commit unknown. [JSON](../data/web-projects/nextjs/pr-98571.json) |
| 기능·확장 | [#97203](https://github.com/vercel/next.js/pull/97203), `2026-09-11T14:29:44Z` | 기능 시작 커밋 `963fc3d`부터 코드와 테스트가 함께 있음 → same-commit unknown. [JSON](../data/web-projects/nextjs/pr-97203.json) |
| 버그 | [#98506](https://github.com/vercel/next.js/pull/98506), `2026-09-11T14:01:15Z` | 구현-only `254faa2` 뒤 test-only `ac34a62`, 이어 rename → implementation-then-test commits. PR 본문의 수동 before/after는 있으나 로컬 편집 순서는 모름. [JSON](../data/web-projects/nextjs/pr-98506.json) |
| 버그 | [#98252](https://github.com/vercel/next.js/pull/98252), `2026-09-11T11:44:24Z` | typegen 수정과 테스트가 첫 커밋 `2196b65`에 함께 있고 이후 tsconfig 보정 → same-commit unknown. [JSON](../data/web-projects/nextjs/pr-98252.json) |
| 버그·확장 | [#98512](https://github.com/vercel/next.js/pull/98512), `2026-09-11T08:46:56Z` | fallback staging 코드와 많은 관련 테스트가 `0556fc6`에 함께 있음 → same-commit unknown. [JSON](../data/web-projects/nextjs/pr-98512.json) |
| 리팩터 | [#98575](https://github.com/vercel/next.js/pull/98575), `2026-09-11T23:25:09Z` | 초기 타입 리팩터와 테스트가 함께 있고 마지막 구현-only follow-up은 초기 순서를 밝히지 못함 → same-commit unknown. [JSON](../data/web-projects/nextjs/pr-98575.json) |
| 리팩터 | [#98347](https://github.com/vercel/next.js/pull/98347), `2026-09-10T11:50:40Z` | scripts/bench dependency migration에 테스트 파일 없음 → existing tests only. [JSON](../data/web-projects/nextjs/pr-98347.json) |
| 리팩터·확장 | [#97988](https://github.com/vercel/next.js/pull/97988), `2026-08-28T15:52:51Z` | PR이 “strictly a refactor, no logic should change”라고 범위를 밝히며, 추출과 관련 단위 테스트가 첫 커밋 `ca52aa6`에 함께 있음 → same-commit unknown. [JSON](../data/web-projects/nextjs/pr-97988.json) |

React sync bot, CI·docs·test-only, backport, dependency bump와 성능 최적화가 주목적인 #98504를 제외했다. 헤드 check-runs는 total 117–169인 반면 저장된 첫 100개만 success/skipped로 관찰되어, 전체 CI 성공을 주장하지 않는다. #98506의 중간 커밋에는 실패 check run도 있지만 테스트 누락 때문인지 확인되지 않아 순서 판정의 실패 확인으로 쓰지 않았다.

## GitLab: 8 same-commit unknown, 1 existing-tests only

| 유형 | MR과 병합 시각 UTC | 관찰된 순서 근거 |
|---|---|---|
| 기능 | [!254453](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/254453), `2026-09-11T22:36:41.627Z` | grouping 기능과 Jest 테스트가 `1d67f8f`에 함께 있음 → same-commit unknown. [JSON](../data/web-projects/gitlab/mr-254453.json) |
| 기능 | [!254982](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/254982), `2026-09-11T22:21:10.670Z` | filter 동작과 테스트가 `ef89f86`에 함께 있음 → same-commit unknown. [JSON](../data/web-projects/gitlab/mr-254982.json) |
| 기능·확장 | [!255081](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/255081), `2026-09-11T19:11:35.282Z` | 두 커밋 모두 UI 동작과 테스트를 같이 변경 → same-commit unknown. [JSON](../data/web-projects/gitlab/mr-255081.json) |
| 버그 | [!254560](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/254560), `2026-09-11T18:42:33.212Z` | navigation metadata 수정과 specs가 `8ec65a0`에 함께 있음 → same-commit unknown. [JSON](../data/web-projects/gitlab/mr-254560.json) |
| 버그 | [!254677](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/254677), `2026-09-11T18:39:48.670Z` | 첫 커밋에 수정과 테스트가 함께 있고 후속은 test stub 조정 → same-commit unknown. [JSON](../data/web-projects/gitlab/mr-254677.json) |
| 버그·확장 | [!254620](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/254620), `2026-09-11T18:36:20.959Z` | 두 커밋 모두 구현과 tests/specs를 같이 변경 → same-commit unknown. [JSON](../data/web-projects/gitlab/mr-254620.json) |
| 리팩터 | [!254298](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/254298), `2026-09-12T02:35:52.182Z` | 첫 tool-catalog 변경과 tests가 같은 커밋이고 이후 test/rule 변경 → same-commit unknown. [JSON](../data/web-projects/gitlab/mr-254298.json) |
| 리팩터 | [!252442](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/252442), `2026-09-11T19:33:18.072Z` | state 리팩터와 Jest 변경 14개가 `0ff342d`에 함께 있음 → same-commit unknown. [JSON](../data/web-projects/gitlab/mr-252442.json) |
| 리팩터·확장 | [!253525](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/253525), `2026-09-11T16:00:48.040Z` | feature-flag lifecycle 코드/config/docs만 변경 → existing tests only. [JSON](../data/web-projects/gitlab/mr-253525.json) |

bot-authored, docs-only, stable backport !255118, spec-only !255060·!247832는 제외했다. 모든 표본에서 조회 시 가장 최신 pipeline은 success였고 일부 MR에는 그 전 failed/canceled pipeline도 있다. 이 상태 이력은 최종 검증이 반복되었다는 근거일 뿐, 개별 테스트를 구현보다 먼저 썼다는 근거가 아니다.

## 에이전트 개발에 적용할 수 있는 범위

이 근거는 모든 작업에 엄격한 TDD를 강제하기보다, **행동을 판별할 수 있는 테스트 증거를 강제**하는 쪽을 지지한다. 버그 수정 에이전트에는 기준 커밋에서 실패하고 수정 커밋에서 통과하는 같은 테스트 명령과 결과를 남기게 하는 것이 Django·Rails·Next.js 정책에 가장 가깝다. 기능은 명시된 수용 동작을 자동화하고, 리팩터는 기존 테스트가 충분한지 먼저 확인한 뒤 필요한 경우에만 새 회귀 테스트를 추가하도록 할 수 있다.

에이전트 실행 계약은 다음 정도가 실용적이다.

1. 버그 수정: 가능한 최소 재현 테스트를 먼저 만들거나 찾고, 기준판 실패와 수정판 통과를 둘 다 기록한다. 실패 재현이 불가능하면 이유와 대체 검증을 명시한다.
2. 기능: 요구사항별 테스트를 구현과 함께 제출하고 영향 범위의 테스트를 통과시킨다. 테스트가 구현보다 먼저 커밋되어야 한다는 형식 규칙은 두지 않는다.
3. 리팩터: 관찰 동작을 유지하는 기존 테스트를 먼저 식별한다. 테스트를 추가하지 않았다면 어느 기존 검사가 보호하는지 기록한다.
4. 감사 증거: 커밋 순서 대신 실행한 명령, 기준판·수정판 결과, 변경된 test path, CI 링크를 보존한다. same-commit은 순서 불명으로 남긴다.
5. 탐색적 작업: 짧은 spike 후 테스트를 보강하는 예외를 허용하되, 병합 전에는 같은 판별력 기준을 충족시킨다.

프로젝트 인지도, 정책 채택, 이 표본의 병합은 어느 개발 순서가 생산성·품질을 인과적으로 높였다는 증거가 아니다. 이 조사가 지지하는 것은 “TDD라는 이름”보다 수정 전 실패 가능성, 수정 후 통과, 회귀 방지와 증거 보존을 에이전트 계약의 핵심으로 삼으라는 조건부 권고다.
