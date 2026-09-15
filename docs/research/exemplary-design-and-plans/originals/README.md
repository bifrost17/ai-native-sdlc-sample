# 다운로드한 원문 전체

보관일: 2026-09-11. 선정 문서 **7건 전체**와 Superpowers 계획의 **짝 설계문서 1건**을 저장했다. 원문 언어·본문·코드 블록을 유지했으며 요약으로 대체하지 않았다. 저장소 문서는 보고서에서 평가한 고정 커밋을 사용했다.

## 문서 위치

경로 기준은 이 파일이 있는 `docs/research/exemplary-design-and-plans/originals/`이다.

| ID | 문서 전체 파일 | 버전 / 보관 방식 |
|---|---|---|
| D1 | [Symphony SPEC](D1-symphony-spec.md) | `8001b52e3062495a16e520e4ceaf8f9de868c4d0`, Markdown 원본 |
| D2 | [Django DEP 0009](D2-django-dep-0009.rst) | `a83080652411e34e6afa8e1f0a97b675a76358e5`, reStructuredText 원본 |
| D3 | [GitLab HTTP Routing Service](D3-gitlab-http-routing-service.md) | `b23f6a4e957776d299d058624f38114d2511d75e`, Markdown 원본; Mermaid 다이어그램 포함 |
| D4 | [MediaWiki 읽기본](D4-mediawiki.html) · [수정하지 않은 HTML 원본](D4-mediawiki.original.html) | AOSA 웹페이지 전체, 2026-09-11 다운로드; 도표 2개와 CSS 포함 |
| P1 | [Openverse Dark Mode 원본](P1-openverse-dark-mode.md) · [색상표 포함 읽기본](P1-openverse-dark-mode.reading.md) | `c815ba4942a3d53cb687d51121f7d44caec7b7e3`, Markdown 원본과 그림 경로만 조정한 읽기본 |
| P2 | [Openverse Ingestion Server Removal](P2-openverse-ingestion-server-removal.md) | `c815ba4942a3d53cb687d51121f7d44caec7b7e3`, Markdown 원본 |
| P3 | [Superpowers Auth Hardening 계획](P3-superpowers-auth-hardening-plan.md) | `83b5d3a963ed63d8231ecb3276c8368caf1857a3`, 최초 계획 Markdown 원본 |
| P3 보조 | [Superpowers Auth Hardening 설계](P3-superpowers-auth-hardening-design.md) | 동일 커밋의 짝 설계문서 전체; 선정 수에는 중복 집계하지 않음 |

## 원본과 읽기본의 차이

Git에서 내려받은 7개 파일(D1·D2·D3·P1·P2·P3·P3 보조)은 원격 고정판의 본문과 **바이트 단위로 일치**하는지 확인했다. 파일 크기와 Git blob SHA-1도 대조했다. D4의 `original.html`은 HTTP로 받은 전체 응답을 그대로 보존한다.

D4 읽기본은 본문을 유지하고 그림·스타일 경로를 로컬로 바꿨다. 상대 탐색 링크는 원 사이트로 연결하며, 본문과 무관한 분석·MathJax 스크립트와 CSS의 원격 글꼴 import를 읽기본에서만 제거했다. 시스템 글꼴이 적용되므로 사이트와 글꼴은 다를 수 있다. P1 읽기본은 색상표 이미지 경로 하나만 바꿨다. 두 원본은 별도로 그대로 남아 있다.

이미지·스타일은 `assets/` 아래에 있다. 원문에서 다른 문서·저장소로 이어지는 링크는 해당 외부 자료를 가리킨다. 링크된 모든 웹사이트나 소스코드 저장소까지 내려받은 것은 아니다.

## 출처와 검증 기록

[manifest.json](manifest.json)에 파일별 원문 URL, 커밋, 다운로드 시각, 크기, SHA-256, 원격 Git blob 대조 결과와 읽기본 변경 사항을 기록했다. 원본 HTML과 읽기본의 본문 텍스트 일치, PNG 파일 형식과 읽기본의 로컬 이미지·스타일 경로도 확인했다.

원문 속 에이전트 지시·명령은 보관 대상 텍스트다. 이번 작업에서는 해당 프로젝트의 구현 명령이나 테스트를 실행하지 않았다.

## 저자·라이선스 고지

- Symphony: OpenAI 프로젝트. 저장소의 [Apache 2.0 고지](licenses/symphony-LICENSE).
- Django DEP 0009: Andrew Godwin. 문서 끝에 CC0 1.0 공개 고지가 포함되어 있다.
- GitLab Handbook: GitLab 프로젝트. 해당 커밋의 [저장소 고지](licenses/gitlab-handbook-LICENSE).
- MediaWiki 장: Sumana Harihareswara, Guillaume Paumier. [AOSA 원문](https://aosabook.org/en/v2/mediawiki.html), [AOSA 라이선스 안내 보관본](licenses/aosa-license.html). AOSA의 Creative Commons Attribution 3.0 Unported 안내를 함께 보존했다. 읽기본 변경 범위는 위에 명시했다.
- Openverse: 계획 저자 Zack Krida 및 @stacimc. [저장소 MIT 고지](licenses/openverse-LICENSE).
- Superpowers: 해당 문서 커밋 작성자 Drew Ritter. [저장소 MIT 고지](licenses/superpowers-LICENSE), 저작권 고지 Jesse Vincent.

[전체 조사보고서로 돌아가기](../README.md)
