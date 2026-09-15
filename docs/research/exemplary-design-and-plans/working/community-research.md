# 공개 개발자 커뮤니티 조사 기록

조사 시각: 2026-09-11 (Asia/Seoul)

## 조사 방법과 접속 결과

`aside-browser`의 `SKILL.md`, `aside guide`, `aside guide repl`을 읽고, 연결 복구 후 Aside REPL의 `openTab()`과 `snapshot()`으로 지정된 공개 페이지를 직접 열람했다. 사이트 쓰기, 댓글, DM, 가입, 로그인, 사용자 계정 토큰 및 개인 파일 탐색은 하지 않았다.

| 대상 | 실제 결과 |
|---|---|
| [Design Docs at Google, Hacker News](https://news.ycombinator.com/item?id=23915521) | 성공. 제목, 원문 링크, 459 points, 187 comments 및 댓글 트리를 snapshot으로 확인했다. 출력량이 약 30K tokens여서 CLI 출력 중간은 잘렸지만 아래에 인용한 댓글과 링크는 출력 또는 별도 DOM `href` 조회로 확인했다. |
| [Ask HN: Examples of good technical design docs](https://news.ycombinator.com/item?id=24184906) | 성공. 질문 본문, 5개 댓글 및 추천 링크를 snapshot으로 확인했다. |
| [r/ExperiencedDevs 스레드](https://www.reddit.com/r/ExperiencedDevs/comments/1awsqtv) | 실패. Reddit이 challenge query가 붙은 URL로 이동한 뒤 `You've been blocked by network security.`만 표시했다. 제목, 본문, 댓글은 읽지 못했다. 관찰하지 않은 `old.reddit.com` 주소를 추측해 열지 않았다. |

초기에는 `aside skills list`가 `Failed to request daemon auth challenge: fetch failed`와 `Aside isn't running on this machine.`으로 실패했지만, 연결 원인 해결 후 상위 작업자가 sandbox 밖에서 목록을 확인했다. HN/Reddit 전용 built-in skill은 없었고, 승인된 `aside repl` 경로로 위 페이지를 열람했다.

## 검토할 만한 구체 사례 후보

아래 항목은 이 두 HN 스레드에서 실제 참가자가 구체 자료로 제시한 후보이다. 두 스레드만으로 광범위한 커뮤니티 합의라고 볼 수는 없다.

### 1. Chromium Design Documents

- 후보: [Chromium Design Documents](https://www.chromium.org/developers/design-documents)
- 추천 맥락: 한 참가자가 “실제 문서가 없는 요약 글보다 구체 예시가 필요하다”고 지적하자, 다른 참가자가 Chromium의 설계문서 모음을 직접 제시했다. 시스템 설계문서의 공개 표본을 여러 개 비교할 수 있다는 점에서 가장 직접적인 사례 후보다.
- 추천 댓글: [floil의 답변](https://news.ycombinator.com/item?id=23922187)
- 요청 배경: [choppaface의 구체 예시·사후분석 요구](https://news.ycombinator.com/item?id=23921004)
- 설계/agent 구현계획에 적용할 점: 섹션 템플릿만 복사하기보다 실제 시스템 문서에서 동기, 제약, 대안, 선택, 구현 경계를 어떻게 연결하는지 표본 단위로 비교한다.
- 한계: 추천 댓글은 링크만 제공하며 개별 Chromium 문서의 품질을 검토하거나 공통 우수성을 입증하지 않는다. 이번 분담에서도 링크된 모음 내부 문서까지 열람하지 않았다.

### 2. Ganeti Implemented Designs

- 후보: [Ganeti implemented designs](http://docs.ganeti.org/ganeti/master/html/#implemented-designs)
- 추천 맥락: `mbakke`는 Google 내부에서 개발돼 오픈소스로 공개된 Ganeti에 이런 설계문서가 많이 있으며, 외부 사용자로서 읽는 것을 즐겼다고 설명했다. 작성 조직의 자기소개가 아니라 실제 외부 사용자의 경험이 붙은 후보라는 점이 유용하다.
- 추천 댓글: [mbakke의 답변](https://news.ycombinator.com/item?id=23922021)
- 설계/agent 구현계획에 적용할 점: “implemented” 문서 모음은 제안과 실제 구현 사이를 비교할 후보군이다. agent 계획에서도 목표, 선택한 접근, 구현 단위, 완료 상태가 어떻게 이어지는지 검토할 수 있다.
- 한계: 한 명의 긍정적 경험이며, 문서별 최신성·성공 여부·사후 변경은 이 댓글만으로 알 수 없다.

### 3. Uber RFC 경험과 쓰기로 확장한 엔지니어링 문화

- 후보: [Scaling Engineering Teams via Writing Things Down: RFCs](https://blog.pragmaticengineer.com/scaling-engineering-teams-via-writing-things-down-rfcs/)
- 추천 맥락: `gregdoesit`은 Uber에서 모든 프로젝트에 RFC를 일찍 도입했고, 전 엔지니어링 조직에 배포하는 방식이 천 명이 넘는 규모까지 잘 작동했다고 자신의 경험을 설명했다. 문서 한 장의 서식보다 리뷰·배포·조직 확장 과정까지 다루는 사례로 가치가 있다.
- 추천 댓글: [gregdoesit의 경험](https://news.ycombinator.com/item?id=23919520)
- 설계/agent 구현계획에 적용할 점: agent 계획을 작성자 개인의 TODO가 아니라 관련 주체가 비동기 검토하고 의존성과 반대 의견을 드러내는 RFC로 운용하는 사례를 검토한다.
- 한계: 작성자 자신의 회고이므로 독립 평가가 아니다. 또한 댓글 자체가 “천 명이 넘은 뒤” 같은 규모 한계를 시사한다.

## 스레드에서 확인된 설계문서의 실무 원칙

- 사전 합의와 병렬화: [cameronbrown](https://news.ycombinator.com/item?id=23916134)은 코드 리뷰와 다른 종류의 피드백을 얻고 여러 팀·기술 사이 합의를 코드 작성 전에 형성한다고 평가했다. [jakevoytko](https://news.ycombinator.com/item?id=23916466)는 blocker, known unknowns, 구현 작업을 일찍 나누면 여러 엔지니어의 작업 중단 위험을 줄인다고 보탰다.
- 대안을 명시하는 효과: [nkingsy](https://news.ycombinator.com/item?id=23917631)는 trade-off를 쓰는 과정이 대안 탐색을 공식화하며, 자신도 대안이 더 설득력 있어 본안과 바꾸는 일이 많다고 설명했다.
- 크기에 맞춘 문서화: [theptip](https://news.ycombinator.com/item?id=23918461)은 agile을 무설계가 아니라 just-in-time design으로 보고, sprint가 아니라 story/epic에 문서를 연결하며 복잡도와 변경 비용에 비례해 사전 설계를 늘리자고 제안했다.
- 제안과 현재 문서의 구분: [jkaptur](https://news.ycombinator.com/item?id=23919292)는 설계문서를 결정을 돕는 “ought” 문서로, 운영 문서를 현재 상태인 “is” 문서로 구분했다. 구현계획과 유지보수 문서의 수명주기를 분리할 근거가 된다.

## 반론과 실패 패턴

- 문서가 실행 가능한 blueprint는 아니다: [sarchertech](https://news.ycombinator.com/item?id=23917227)는 설계문서가 세 구현팀에 동일 결과를 낼 정도로 구체적이지 않으며, 이를 완전한 blueprint로 취급하면 위험하다고 반박했다. 계획에는 구현 중 발견과 변경을 반영할 여지를 남겨야 한다.
- 불확실한 제품 문제에는 큰 선행 설계가 맞지 않을 수 있다: [Areibman](https://news.ycombinator.com/item?id=23917154)은 많은 프로젝트가 문제 자체를 아직 모른다고 지적했다. 이에 대한 실용적 절충이 story/epic 단위의 짧은 설계와 복잡도 기반 깊이 조절이다.
- 관료화와 지연: [blululu](https://news.ycombinator.com/item?id=23923854)는 bikeshedding과 실제 소프트웨어 대신 slideware를 만드는 행정 부하를 경고했다. `choppaface`도 피드백 주기가 수 주 걸릴 수 있다고 했다.
- 동기와 사용 사례가 빠진 구현 세부는 좋은 설계문서가 아니다: [jeffbee](https://news.ycombinator.com/item?id=23918428)는 댓글에 제시된 event trace 문서가 motivation과 use case 없이 구현 세부로 바로 들어가므로 설계문서보다 형식 명세에 가깝다고 비판했다.
- “좋은 실제 사례” 요청에 메타 자료가 답으로 섞인다: [Ask HN 질문](https://news.ycombinator.com/item?id=24184906)은 실제 설계문서를 요구했지만, 첫 답변은 다시 “Design Docs at Google” 방법론 글이었다. 질문자는 [후속 댓글](https://news.ycombinator.com/item?id=24188700)에서 실제 문서가 필요하다고 재차 구분했다. 사례집에는 작성법 글과 실제 산출물을 별도 분류해야 한다.

## Ask HN에서 추가로 나온 자료와 신뢰도

- [National Academies PDF](https://sites.nationalacademies.org/cs/groups/pgasite/documents/webpage/pga_179129.pdf): [추천자](https://news.ycombinator.com/item?id=24197878)가 자신의 업무 템플릿과 어느 정도 비슷하다고 했지만, “golden sample”인지 확신하지 못한다고 명시했다. 참고 후보로만 둔다.
- [awesome-writing](https://github.com/jenniferlynparsons/awesome-writing): [추천 댓글](https://news.ycombinator.com/item?id=24186395)에 포함됐지만 실제 시스템 설계문서 하나를 지목한 것은 아니다.
- [USAF SMC-S-012](http://everyspec.com/USAF/USAF-SMC/SMC-S-012_16JAN2015_52130/): [추천 댓글](https://news.ycombinator.com/item?id=24185047)은 유용한 자료라고만 했고 이유를 제시하지 않았다. 소프트웨어 agent 구현계획과의 직접 관련성은 별도 검토가 필요하다.

## 통합 시 사용할 결론

이 커뮤니티 근거가 지지하는 방향은 긴 단일 템플릿이 아니다. 좋은 후보는 실제 구현 문서 모음을 제공하고, 동기·사용 사례·제약·대안·trade-off·구현 단위를 연결하며, story/epic의 복잡도에 맞춰 깊이를 조절하고, 리뷰가 blocker를 조기에 드러내도록 한다. 동시에 문서가 구현을 완전히 결정한다는 가정, 리뷰 지연, bikeshedding, [사후 승진 자료화](https://news.ycombinator.com/item?id=23920545)는 명시적 실패 모드로 다뤄야 한다.
