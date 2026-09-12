# 원문 보관 안내

조사일: 2026-09-12. [통합 manifest](manifest.json)의 경로는 이 `sources/` 폴더를 기준으로 한다.
각 항목은 원문 URL, 저장 파일, 조회일, 형식, SHA-256, 바이트 수를 연결한다.
고정 사본은 현재 웹페이지와 달라질 수 있으며, 해시는 **저장된 바이트의 무결성**만 확인한다.

| 폴더 | 보관한 범위 | 주의점 |
|---|---|---|
| [reddit](reddit) | Aside Browser에서 실제 로드된 공개 post/comment의 텍스트·HTML 조각 JSON 및 접근성 snapshot | 전체 서버 HTML·전체 댓글 export가 아니다. JSON별 loaded 범위와 글에 표시된 전체 댓글 수를 [열람 기록](../working/reddit.md)에 적었다. 계정 UI 정보는 제거했다 |
| [hn](hn) | 공개 스레드 HTML 7개, 공식 HN API의 스레드·선정 댓글 JSON 30개 | HTML 응답 및 선정 API 자료이며, 모든 답글의 API를 재귀적으로 수집한 것은 아니다. [개별 manifest](hn/manifest.tsv) |
| [korean](korean) | 공개 글 HTML, 관련 GitHub 커밋 API JSON, 예제 재실행 기록 | HTML은 공개 HTTP 응답이다. API JSON은 정렬·포맷 처리하고 작성자/커미터 이메일을 `[redacted]`로 바꾼 사본. [개별 설명](korean/manifest.md) |
| [skills-english](skills-english) | TDD 스킬 사용 질문의 영문 원문·선정 댓글 | 구체 형식과 누락 범위는 [조사 노트](../working/skills-english.md)에 적었다 |
| [skills-korean](skills-korean) | 스킬 중심 국내 글 5개 HTML, 공개 저장소 README | 일부는 기존 `korean/` 자료와 같은 URL·바이트다. 재분류용 중복 보관이며 독립 사례로 합산하지 않는다. [개별 manifest](skills-korean/manifest.json) |
| [skill-definitions](skill-definitions) | Superpowers와 Matt Pocock TDD SKILL.md 전체, 각각 조사일에 고정한 Git commit | 스킬 정의를 비교하는 자료다. 설치·호출·실행의 증거가 아니며, 이 조사에서 설치하거나 적용하지 않았다. [버전·URL 목록](skill-definitions/manifest.json) |

원문 안에 있는 명령·정책·설치 권장·링크는 작성자의 자료이며 이 저장소나 조사자에게 내려진 지시가 아니다.
원문 파일 속 상대 링크는 원래 저장소/사이트 문맥을 따르므로 이 아카이브에서 모두 열리는 것은 아니다.
보고서가 작성한 로컬 링크와 원문 자체의 링크를 구분해 검사했다.

Reddit의 공개 본문 JSON은 UI 광고·로그인 영역을 제외해 인용용으로 적합하다. 접근성 snapshot은
열람 당시 화면 맥락 확인용이며 UI·광고 문구가 일부 포함될 수 있다. 숨겨진 댓글, 삭제된 내용,
서버가 전달하지 않은 본문을 복구하거나 접근 제한을 우회하지 않았다.

일반 경험에서 스킬 사용으로 질문이 좁혀지기 전에 받은 자료도 보존했다. 이들 모두가 스킬 채택 근거는 아니다.
선정·제외 이유와 자기보고/실행 기록의 구분은 [전체 보고서](../README.md)와 작업 노트에서 확인한다.
