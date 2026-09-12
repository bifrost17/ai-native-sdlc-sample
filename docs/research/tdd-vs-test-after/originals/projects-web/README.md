# 웹 프로젝트 테스트 정책 원문

조사 시각은 `2026-09-12T07:48:59Z`이다. Git 저장소 문서는 당시 기본 브랜치의 커밋으로 고정해 전체 원문을 저장했다. `manifest.json`에는 고정 커밋과 파일별 SHA-256이 있다. React의 현재 `CONTRIBUTING.md`는 기존 공식 사이트의 가이드를 가리키므로, 짧은 저장소 파일과 HTTP 응답 전체를 함께 저장했다. 이 웹 문서는 커밋 고정 URL이 없어서 응답 헤더와 해시로만 시점을 보존했다.

| 프로젝트 | 정책 원문 | 고정 원출처 |
|---|---|---|
| Django | [패치 제출](django-submitting-patches.txt), [단위 테스트](django-unit-tests.txt) | [submitting-patches.txt](https://github.com/django/django/blob/2b30f6255b5ef84afbd827993643d52ef2c0963a/docs/internals/contributing/writing-code/submitting-patches.txt), [unit-tests.txt](https://github.com/django/django/blob/2b30f6255b5ef84afbd827993643d52ef2c0963a/docs/internals/contributing/writing-code/unit-tests.txt) |
| Rails | [CONTRIBUTING.md](rails-CONTRIBUTING.md), [기여 가이드](rails-contributing-guide.md) | [CONTRIBUTING.md](https://github.com/rails/rails/blob/5d0f2ef19ac387022c2ec6ad6efe442c2b9d79a2/CONTRIBUTING.md), [contributing guide](https://github.com/rails/rails/blob/5d0f2ef19ac387022c2ec6ad6efe442c2b9d79a2/guides/source/contributing_to_ruby_on_rails.md) |
| React | [현재 저장소 안내](react-CONTRIBUTING.md), [공식 기존 가이드 HTML](react-legacy-how-to-contribute.html), [HTTP 헤더](react-legacy-how-to-contribute.headers.txt) | [CONTRIBUTING.md](https://github.com/facebook/react/blob/019019be403c3269e15b8d7ebefb57d30f84086b/CONTRIBUTING.md), [legacy guide](https://legacy.reactjs.org/docs/how-to-contribute.html) |
| Next.js | [기여 안내](nextjs-contributing.md), [테스트 가이드](nextjs-testing.md) | [contributing.md](https://github.com/vercel/next.js/blob/d5276f04a1406b131a98efb77866a256fb68178f/contributing.md), [testing.md](https://github.com/vercel/next.js/blob/d5276f04a1406b131a98efb77866a256fb68178f/contributing/core/testing.md) |
| GitLab | [MR workflow](gitlab-merge-request-workflow.md), [testing strategy](gitlab-testing-strategy.md), [code review](gitlab-code-review.md) | [MR workflow](https://gitlab.com/gitlab-org/gitlab/-/blob/d1fc75b481ab131d96e4ea91140bbdd2a7e3a67b/doc/development/contributing/merge_request_workflow.md), [testing strategy](https://gitlab.com/gitlab-org/gitlab/-/blob/d1fc75b481ab131d96e4ea91140bbdd2a7e3a67b/doc/development/testing_guide/testing_strategy.md), [code review](https://gitlab.com/gitlab-org/gitlab/-/blob/d1fc75b481ab131d96e4ea91140bbdd2a7e3a67b/doc/development/code_review.md) |

저장한 원문 전체에서 `TDD`, `test-driven`, `red-green`이라는 일반 개발 방식의 의무 문구는 발견되지 않았다. 이는 선택한 공식 문서에 대한 문자열 확인이며, 프로젝트 구성원 누구도 TDD를 쓰지 않는다는 뜻은 아니다.
