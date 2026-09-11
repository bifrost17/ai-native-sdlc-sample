# Root 조사 메모

조사일: 2026-09-11. 이 파일은 탐색·검증 기록이며 최종 선정은 상위 보고서에 있다.

## 경로와 후보

| 후보 | 읽은 원문 | 판정 메모 |
|---|---|---|
| MediaWiki, AOSA Volume 2 | https://aosabook.org/en/v2/mediawiki.html | 교육/사후 아키텍처 해설의 최우선 후보. 전체 웹앱 구조, 저장 변경 이유, 요청 흐름, 캐시를 연결한다. §12.11에 core 개발자의 기여·검토 명시. 현재 아키텍처를 설명한다고 간주하면 안 된다. |
| SocialCalc, AOSA Volume 1 | https://aosabook.org/en/v1/socialcalc.html | 우수한 웹앱 설계 해설. 클라이언트 이동과 가상화/명령 구조의 이유를 설명. 교육 자료의 중복을 줄이기 위해 보조 후보. |
| From SocialCalc to EtherCalc, POSA | https://aosabook.org/en/posa/from-socialcalc-to-ethercalc.html | 우수한 성능·구조 진화 사례. 제약, 프로파일링, 대안의 비용을 연결. 사전 spec이 아니라 2011~2012 개발 회고라는 마지막 절의 설명을 유지. |
| Openverse Ingestion Server Removal | https://docs.openverse.org/projects/proposals/ingestion_server_removal/20240328-implementation_plan_ingestion_server_removal.html | 구현계획 주 후보. 단계별 기존 경로 유지, 로컬/운영 차이, 대안 비교, 환경별 검증과 최종 철거. 실제 검토·계획개정·구현 PR 확인. 전체 프로젝트는 여전히 open. |
| Openverse Dark Mode | https://docs.openverse.org/projects/proposals/dark_mode/20240325-implementation_plan_dark_mode.html | 매우 강한 웹앱 기능 계획. 병렬 work streams, 단계별 가시적 변화, SSR 쿠키/캐시, 시각회귀, 출시·복구. 2024-12-10 공식 출시 공지 확인. Ingestion과 별도 강점. |
| Openverse Fetching, blurring sensitive results | https://docs.openverse.org/projects/proposals/trust_and_safety/detecting_sensitive_textual_content/20230506-implementation_plan_frontend_blurring_sensitive.html | 좋은 경계·기능 플래그·접근성 사례. Step 3 중복 번호와 구체 테스트 명령 부족은 약점. 중복 프로젝트 후보 제한으로 보조. |
| Openverse Popularity calculations decoupling | https://docs.openverse.org/projects/proposals/popularity_optimizations/20230420-implementation_plan_popularity_optimizations.html | 기존 모델과 단계별 데이터 전환이 구체적인 계획. 다른 Openverse 주 후보와 중복되어 이력 정독은 보류. |
| Django DEP 0009 | https://github.com/django/deps/blob/main/accepted/0009-async.rst | 전통 설계/다년 순서 계획 후보. 상세 테스트·실행 계획보다는 설계 사례로 적합. 설계 담당에게 연결. |
| react-grid-layout TypeScript rewrite RFC | https://github.com/react-grid-layout/react-grid-layout/blob/master/rfcs/0001-v2-typescript-rewrite.md | 검색에서 발견. 아직 본문·이력 미검증. 최종 선정에 사용 안 함. |
| OpenTranscribe combined implementation gists | https://gist.github.com/attevon-admin/cc99d266449178649341c2976f9d3f03 | 검색에서 발견. plan only/not implemented 표시. 작성자·실사용 추적성이 더 강한 후보 우선. 본문 심사 안 함. |

## Openverse Ingestion 검증

- 고정 스냅샷: `WordPress/openverse@c815ba4942a3d53cb687d51121f7d44caec7b7e3`, 문서 blob `09eeba0a2a94f8666c33b5822dda5d2d3cd5ab29`.
- 계획 PR: https://github.com/WordPress/openverse/pull/4026 — 2024-04-03 생성, 2024-04-17 병합, merge `797b32c8e76a72a123a1338e6c8768d57f6ed885`. 문서에 적힌 2024-03-28과 공개 PR 시각을 구분한다.
- 최초 추가된 문서판: https://github.com/WordPress/openverse/blob/26480d47f7afd01d4a66b41d3d81f5ec5922aa8f/documentation/projects/proposals/ingestion_server_removal/20240328-implementation_plan_ingestion_server_removal.md
- 검토: https://github.com/WordPress/openverse/pull/4026#pullrequestreview-1981621777 에서 AetherUnbound가 계획의 상세함을 구체적으로 평가하고 확인 질문 제시. https://github.com/WordPress/openverse/pull/4026#pullrequestreview-1998688566 (2024-04-12), https://github.com/WordPress/openverse/pull/4026#pullrequestreview-2002490278 (2024-04-16)에서 APPROVED 확인.
- 계획 수정: https://github.com/WordPress/openverse/pull/4615 — 2024-07-19 병합. ASG에서 직접 EC2 관리로 바뀐 이유를 이슈 토론에 연결.
- 구현 수정: https://github.com/WordPress/openverse/pull/4684 — 2024-08-20 병합. 기존 multiprocessing 복제가 Airflow에서 막혀 mapped tasks로 전환했고, 오디오까지 필터링하는 차이를 명시. 환경변수·관찰 결과를 포함한 테스트 지침이 있다. 테스트를 우리가 재실행한 것은 아니다.
- 전체 프로젝트 https://github.com/WordPress/openverse/issues/3925 는 조회 시 open, 미완료 항목 존재. 완성/운영 성공 사례라고 쓰지 않는다.
- 공식 진행 기록: https://make.wordpress.org/openverse/2024/11/06/openverse-monthly-priorities-meeting-2024-11-06/ 는 당시 오디오 staging 성공과 이미지 단계의 미완료를 구분한다.
- 주요 API 사실은 `openverse-evidence.json`에 저장. 전체 PR 본문이나 원문은 복제하지 않았다.

## Openverse Dark Mode 보강 출처

- 출시 공지: https://make.wordpress.org/openverse/?p=2216 — Olga Bulat, 2024-12-10. 공개 계획·진행과 최종 기능 제공을 설명한다.
- 주간 기록: https://make.wordpress.org/openverse/2024/10/21/last-week-openverse-2024-10-14-2024-10-21/ — #5051, #5052, #5053 시각회귀 스냅샷 PR 및 #4305 완료 연결.
- 본문 Expected Outcomes, Step-by-step implementation plan, Launch plan, Rollback 정독. 특정 색 이름·UI가 TBD인 부분은 설계 승인 선행 조건으로 명시되어 있어 완전히 독립적인 구현 지시서라고 부르지 않는다.

## 검색 기록

1. AOSA SocialCalc / 웹 시스템 장 → MediaWiki·EtherCalc 원문 및 목차 역추적.
2. GitHub implementation plan + Django/React → DEP 0009와 기타 후보.
3. docs.openverse.org implementation plan → 프로젝트 색인 → 실제 계획 4건 비교.
4. GitHub PR 검색 ingestion server removal → #4026 → reviews → #4615 → #4684 → project #3925.
5. WordPress 공식 dark mode 공지·주간 개발 기록 → 출시 증거 확보.

검색엔진은 Openverse preview 복제본을 많이 반환했다. 최종 링크는 정식 문서 경로와 고정 GitHub 판으로 정규화했다. GitHub REST 조회는 connector를 사용했으며, 프로젝트 트리의 `truncated:false`를 확인했다.

## Aside 초기 시도

- `aside guide` 및 `aside guide repl` 확인. CLI 1.26.906.1630.
- sandbox 안에서는 daemon auth fetch 오류/실행 안 됨처럼 보였으나, 승인된 sandbox 밖 실행에서 실제 세션 생성됨.
- `openai/gpt-5.6-sol` 모델은 Aside 계정에서 unavailable. 이를 성공한 브라우저 조사로 집계하지 않는다.
- 이후 커뮤니티 담당은 Aside REPL 직접 제어로 전환하도록 위임했다. 실제 결과는 `community-research.md`에 기록한다.

## 후속 확인

- MediaWiki 공식 작성 프로젝트 https://www.mediawiki.org/wiki/MediaWiki_architecture_document 를 직접 읽었다. 2011년 8월 편집자의 제안, 공동체·편집자·기술 검토 절차, 2012년 2월 출판 일정이 기록되어 있다. AOSA 본문이 사전 설계가 아닌 개발자 입문용 구조 해설이라는 분류를 보강한다.
- Openverse 다크 모드 공지는 https://make.wordpress.org/openverse/2024/12/10/introducing-dark-mode/ 날짜 경로에서 직접 열기 성공. 짧은 ?p=2216 주소의 cache miss를 해소했다.
- 다크 모드 계획 PR #3963은 2024-05-01 두 승인 뒤 merge. 구현 #4810은 2024-08-30 merge. changed-files에서 use-dark-mode, UI store, cookies, tailwind 및 대응 단위 테스트 수정 확인. metadata는 openverse-dark-evidence.json.
- 보충 agent 검색: https://github.com/obra/superpowers/blob/main/docs/plans/2026-01-17-visual-brainstorming.md — agent plan 담당에게 이력 검증 위임. 관련 issues #649/#565/#87은 작성도구의 한계·운영 논쟁이므로 실제 우수 계획으로 집계하지 않는다.

## 최종 보강 조사

- Symphony `SPEC.md`는 2026-03-04 최초 공개, 2026-08-12 파일 최종 변경 이력 확인. README가 에이전트에게 이 명세를 주어 구현하는 용도를 명시한다. PR #102의 명세·코드·테스트 변경 확인. 자동 테스트 수치는 작성자 보고로 구분. `symphony-evidence.json` 참조.
- Django DEP 0009는 Andrew Godwin의 2019-05-06 문서, Accepted 상태와 2019-07-21 수락 경로 이동 커밋을 확인. 공식 3.1 릴리스 노트로 비동기 뷰·미들웨어·테스트의 출시를 확인. 당시 모든 목표가 실현됐다고 주장하지 않음.
- GitLab HTTP Routing Service 원문 Goals/Requirements/Low Latency/Routing rules/Classification/Deployment/Alternatives 정독. `Non-Goals` 미정, FAQ 미정, 예시 JSON의 설명용 성격을 한계로 추가했다. 공식 runbook이 설계문서를 직접 인용하며 운영 역할과 장애·복구를 설명하는 것 확인. root의 MR369 열기는 cache miss였으므로 최종 주요 근거는 직접 읽은 원문+runbook으로 제한했다.
- Superpowers 원문 3건을 비교했다: 초기 visual brainstorming, zero-dep server, auth hardening. 마지막 사례가 실패 재현·예상 결과·실제 브라우저 검증에서 가장 강했다. 계획83b5d3a → 직접자식 구현b17d54f를 확인하고 주요 코드·테스트 패치를 대조했다. releasePR1769 연결. `superpowers-auth-evidence.json` 참조.
- EveryInc unified plan은 긴 구체 내용에도 본문 제외 산출물과 Global DoD 사이 충돌이 있어 제외. Rhapsody xfail과 BanyanDB replication 계획은 검색 캐시의 실제 본문을 확인했지만 검증 명령·정확성 우려로 보류/제외. 이 원문들에 적힌 명령은 실행하지 않음.
- Aside 최초 실패는 sandbox 안의 daemon 인증이었다. sandbox 밖 `aside skills list`, `aside repl`이 성공했고, 커뮤니티 담당이 HN 두 페이지 실제 snapshot과 댓글 permalink를 확보했다. Reddit은 사이트 네트워크 보안 차단. 업데이트 실패를 실제 브라우저 미지원으로 오인하지 않도록 최종 기록 보정.
