# intent.md 레퍼런스 레포 분석 — 7개 후보 실측 비교 (2026-09-08)

검색 레인 1(sonnet · `gh` 인증 · 검색식 28 · raw 356) + 분석 레인 7(A1·A2·A5·A6·A7·A3 opus / A4 sonnet · 각 레포를 스크래치에 클론해 전 파일 읽기 · 검증기/훅/시험 실행 · 뮤테이션 스윕 · sha256 복원) · 부모가 각 레인 raw 를 열어 핵심 수치를 축자 대조. 라벨: 확정(원문·실행 출력 확인) · 추정 · 확인 못 함.

## 0. 한 장 요약

1. **검색.** 플레이북 발표(08-21) 후 2.5주 안에 정확히 `ai-native-sdlc` 라는 이름의 독립 키트가 8개 생겼고(jsnkle · imsungbin · accuser · ihugang · sofus-nl · bashebr · skysthelimitpainting1779-collab · cc4i), 이름만 겹치는 선행 계보(jabrena/plinth 437★ · fabriqaai/specs.md 207★ · agzyamov · Ovid/paad · agent-rigor)는 생성일이 앞서 제외. 공식 예시 레포는 없다(`anthropics/*` 4개 트리 0건).
2. **선정 7.** 검색 상위 jsnkle(26/30) · imsungbin(25) · bashebr(22 · 유일한 채택 신호 42★) + 기지 4(jcuervo · JHashimoto · honghu-ai · intent-md-ko). 보류: cc4i(라이선스 없음) · accuser(매핑표만) · hermes-labs-ai/intent-verify(검증기 설계 시 별도).
3. **결론 — 참고할 「레포」는 없고 참고할 「조각」이 있다.** 7개 중 어느 것도 플레이북 빈틈 ①(intent→spec 파생 검증)·②(첫 아티팩트 준비도 바닥)·⑤(첫 대화 시각)를 닫지 못했다. 코드가 실동하는 건 jsnkle · imsungbin · bashebr 셋이고, 셋 다 **아티팩트 검증기가 0** — intent 를 통째로 비워도 시험이 초록이다. 유일하게 검증기를 가진 jcuervo 는 코드 펜스 안 `Status: accepted` 한 줄에 속는다.
4. **차용 목록(15 조각).** 문서 골격(jsnkle plays 8절 · bashebr playbook 5필드 · 규칙→집행 매트릭스 · artifact-formats 표 · article-map) · spec 템플릿 3종 · incident 변형 · 한국어 절 이름/발주서 표 · 검출기 2종(17/19 시험) · 게이트 안의 양성/음성 대조 쌍 · sync-validator · 설치기 마커 병합 · 원장 레코드 스키마 · 의도적 미구현 원장.
5. **회피 목록(14 패턴).** 자연어 규범으로 `accepted` 강제 · 리터럴/부분 문자열 검사 · 코드 펜스 미처리 · fail-open 훅(jq 부재·깨진 JSON) · 경로 정규화 부재 · exit code 겸용 · 검증 안 된 동봉 예제 · 상태 어휘 다원화(최대 5벌) · 배선 안 된 훅 · 공식보다 약한 자체 스키마 검사 · 번들만 세는 검증 · 인위 커밋 이력 · 생산자 없는 필수 파일 · 계기보다 강한 문서.

## 1. 후보 신원 (부모가 GitHub API raw 로 확인)

| 후보 | 형태 | 라이선스 | 생성→push · 커밋 | 규모 | ★/포크 | 검색 점수 | 판정 |
|---|---|---|---|---|---|---|---|
| `jsnkle/ai-native-sdlc` | 플러그인 + 프로젝트 템플릿 | MIT | 09-02→09-04 · 25(실제 시간축) | 87파일 3,872줄 | 0/0 | 26 | 개작 |
| `imsungbin/ai-native-sdlc-playbook` | 플러그인 + 멱등 설치기 + 도그푸드 intent 8건 | MIT | 09-03 · main 2(+history 13) | 80파일 | 0/0 | 25 | 개작 |
| `bashebr/ai-native-sdlc` | 단일 스킬 + 스크립트 7 + org 자산 | MIT | 08-23→08-29 · 27 | 75파일 | 42/9(포크 커밋 0) | 22 | 개작 |
| `jcuervo/authoring-ai-sdlc` | 스킬 3 + 템플릿 + 검증기 키트 | MIT | 09-07 · 12(48분) | 39파일 4,033줄 | 0/0 | 18 | 개작 |
| `honghu-ai/sdlc-governance-kit` | 거버넌스 킷(스킬 6 · 스캐폴드) · 중국어 | **없음** | 08-28 · 3(5시간) | 38파일 | 2/1 | 15 | 아이디어만 |
| `JHashimoto0518/ai-native-sdlc-playbook-sample` | 샘플(사슬 1본 시연) · 일본어 | **없음** | 09-06 · 9(타임스탬프 동일) | 24파일 678줄 | 0/0 | 12 | 아이디어만 |
| `simonsez9510/intent-md-ko` | 한국어 템플릿 + 규칙 | CC BY 4.0 | 09-06 · 1 | 4파일 150줄 | 1/0 | 7 | 차용(절 이름·표) |

## 2. 실측 매트릭스 (✅ 성립 · ⚠️ 부분/조건부 · ❌ 없음/뚫림)

| 축 | jsnkle | imsungbin | bashebr | jcuervo | honghu | JHashimoto | intent-md-ko |
|---|---|---|---|---|---|---|---|
| 아티팩트(intent/spec/plan) 검증기 | ❌ 0 | ❌ 0(M2~M6 전부 초록) | ❌ 0(뮤테이션 7 전부 80/0) | ⚠️ 있음 — 절/빈 절/enum 잡음, 펜스 상태 위조·해법 제목·본문 `x`·무관 상류 놓침 | ❌ 스캐폴드 구조만(TODO 치환 시 빈 스캐폴드 OK) | ❌ 0 | ❌ 0 |
| 상류 `accepted` 강제 | ❌ 산문("Refuse politely") | ❌ 산문 | ❌ | ⚠️ 상류 존재+accepted 검사 — 코드 펜스로 위조 가능 | ❌(승인 위조 통과) | ❌ | ❌(파일 말미 판정) |
| 훅 exit 계약 | ✅ 5개 exit 2 | ✅ 4개 exit 2 | ✅ exit 2 | ❌ warn-only exit 0(무효) | — 훅 0 | ✅ exit 2 | — |
| 훅 fail-open(jq/파서 부재·깨진 JSON) | ❌ 4개 전부 | ❌ 4개 전부 | ❌ | — | — | ❌(python3 부재) | — |
| 경로 우회(`../` `./` `//`) | ❌ 4종 | ❌ 3종 | n/a | — | — | ❌ `../` | — |
| 명령 문자열 우회 | ❌ `prod`/대문자/변수/공백 승인 | ❌ `git  commit`/`git -C .` | ❌ `--dry-run=false`·`tools.yaml`·`&& echo` 8건 · 자기 승인 | — | — | ❌ `jsonify({**record})`·app.py 라우트 | — |
| 시험 실동 | ✅ 17 passed · 뮤테이션 7/7 | ✅ 기계 5/5 잡음 | ✅ 80 + 25 + 25(bash 5 필요) | ✅ check-all 26 | ⚠️ 감사기만(뚫림 7) | ✅ 11 passed(동어반복 1) | — |
| CI 실적 | ⚠️ 6 워크플로 · run 0 · 전부 비차단 | ✅ Test 2/2 · bands 5/5 라이브 · ruleset protect-main | ⚠️ self-check 1 | ❌ 없음 | ❌ 없음 | ❌ 없음 | ❌ |
| 원문 충실(축자 검증) | ✅ intent/plan 예시 축자(회고 정직) | ✅ **13/13 바이트 동일** | ✅ playbook.md 190줄 재현 | — | ⚠️ 블로그 전문 무단 번역 | ✅ 7필드/plan 4절 | ✅ 5절 |
| 동봉 예제의 자기 템플릿 준수 | ❌ spec 3절·plan 2절 누락 · draft→accepted 파생 | ⚠️ 8건 전부 accepted(승인 시점 없음) | ❌ expense-tracker plan 파일 5개 부재 | ⚠️ 자기 plan 이 없는 파일 지명 | ❌ self-audit ERROR 5 | ⚠️ R1·R2·CONCERN 하류 참조 0 | ✅ |
| 상태 어휘(벌 수) | 3 | 1(산문) | **5** | 1(enum 3) | **4** | 3(파일마다) | 1(「승인 대기」만) |
| spec 템플릿 | ✅ 34줄 7절 | ✅ 14줄 6요소 | ✅ 36줄 7절(스캐폴드 안 만듦) | ✅ 필수4+확장3 | ✅ 84줄 11절 | 인스턴스 1 | ❌ |
| 공식 검증기 대조 | ✅ frontmatter 공식 필드(argument-hint 는 claude.ai 불가) | ❌ `claude plugin validate` rc=1(`agents` 디렉터리) | ⚠️ frontmatter `version` 비공식 | ⚠️ conformance 가 임의 필드 허용 | ❌ evals 필드명 `expectations`(공식 `assertions`) · `agents/openai.yaml` 소비자 없음 | ✅ | — |
| 라이선스 | MIT | MIT | MIT | MIT | 없음 | 없음 | CC BY 4.0 |

## 3. 플레이 커버리지 (구현 ●  부분 ◐  없음 ○  · 레슨 2~13)

| 레슨 | jsnkle | imsungbin | bashebr | jcuervo | honghu | JHashimoto | ko |
|---|---|---|---|---|---|---|---|
| 2 capture-intent | ● | ● | ● | ● | ● | ● | ● |
| 3 requirements-and-design | ● | ● | ● | ● | ● | ● | ○ |
| 4 plan-mode | ◐ | ● | ◐ | ◐ | ○ | ◐ | ○ |
| 5 claude-md | ● | ● | ● | ◐ | ◐ | ● | ◐(3줄) |
| 6 skills | ◐ | ● | ● | ● | ● | ● | ○ |
| 7 subagents | ◐ | ◐ | ◐ | ○ | ○ | ○ | ○ |
| 8 feedback-loop | ● | ● | ● | ● | ○ | ◐ | ○ |
| 9 evals-in-ci | ● | ◐(disabled) | ● | ◐ | ◐ | ○ | ○ |
| 10 PR-review-loop | ● | ◐ | ● | ○ | ◐ | ○ | ○ |
| 11 hooks-as-approval-gates | ◐ | ● | ◐(배선 없음) | ◐(무효) | ○ | ◐(경로 가드) | ○ |
| 12 ci-cd | ◐ | ◐ | ◐ | ◐ | ○ | ○ | ○ |
| 13 closing-the-loop | ◐(loop.sh 결함) | ● (라이브) | ● | ○ | ○ | ○ | ○ |
| 집계 ●/◐/○ | 7/6/0 | 8/4/0 | 8/5/0 | 4/5/3 | 3/4/5 | 4/3/5 | 1/1/10 |

## 4. 플레이북 빈틈 ①~⑥ 대응

| 빈틈 | jsnkle | imsungbin | bashebr | jcuervo | honghu | JHashimoto | ko |
|---|---|---|---|---|---|---|---|
| ① intent→spec 파생 검증 | ○ | ○(규율만) | ○ | ◐(위조 가능) | ◐(산문) | ○ | ○ |
| ② 준비도 바닥 | ◐(인터뷰 6문항 · 모델 준수) | ○ | ○ | ◐(구조만) | ◐(산문) | ○ | ◐(규칙만) |
| ③ 스키마·ID·상태·폐기·충돌 | ○(slug) | ◐(NNNN-slug · draft/accepted) | ◐(그래프 YAML 8종 + 원장 스키마 · 집행 0) | ◐(enum 3 · NNNN-slug) | ◐ 설계만(9필드 · 4치 · 미구현) | ◐(R/C ID 파일 로컬) | ○ |
| ④ 비엔지니어 커밋 | ○(문서) | ○ | ◐(org/intake 도구 · forms/email 빈) | ○(zip 만) | ○(번역) | ○ | 미정 |
| ⑤ 첫 대화 시각 | ○ | ○ | ○ | ○(Date 안 잼) | ○(记录时间 날짜) | ○(시간축 파괴) | ○(작성일) |
| ⑥ spec 템플릿 | ● | ● | ● | ● | ● | 인스턴스 | ○ |

**7개 전부 ①·⑤ 는 0, ② 는 산문/모델 준수뿐.** 이것이 「우리 레포」가 설 자리다.

## 5. 후보별 카드

### jsnkle/ai-native-sdlc — 「코드가 도는 유일한 종합 키트, 그러나 검증기가 없다」
- 실체: `plugin/`(스킬 6 · 에이전트 3 · 훅 5 · references) + `plugin/template/`(프로젝트에 복사되는 26파일: CLAUDE.md · REVIEW.md · 훅 · 워크플로 6 · `ops/{detect.py,loop.sh,bands.yaml}` · evals) + `docs/`(플레이 14 각 8절 · 회고). 25커밋이 3일에 걸친 실제 작업 시간축.
- 값진 것: `detect.py` 17시험 · 뮤테이션 7/7 · 훅 5개 exit 2 · 회고 스코어카드 전수 정직(초안 과장을 커밋으로 자기정정) · `artifact-formats.md`(사슬 6단 1장 표) · `spec-template.md`(7절) · 플레이 문서 8절 골격 · CLAUDE.md 「두 번 틀리면 등재」.
- 뚫린 것: `ops/loop.sh` 가 `tier=$?` 로 검출기 실패 rc(1/2/3)를 정상 tier 로 오독 — rc=1 → 「tier 1 · 성공」, rc=2 → 빈 리포트로 Claude 호출(loop.sh 시험 0) · jq 부재 시 훅 4개 fail-open · 우회 12(`prod`·대문자·변수 조립·공백 승인·`../`·`.path`·URL 자격증명·MultiEdit·Java/RSpec 시험 파일) · 동봉 `_example/` 이 자기 템플릿 위반 + draft intent→accepted spec · `requirements-dev.txt`·Makefile 미동봉(워크플로 4개 죽음) · `claude-mention.yml` 이 PR 작성자 미검사(pwn-request 정적 추론).

### imsungbin/ai-native-sdlc-playbook — 「원문 축자 13/13 · 라이브 Stage 6 · 그러나 플러그인 매니페스트가 공식 검증기에 걸린다」
- 실체: 블로그(코스 아님) 정본 · 4층 라벨(V 축자/C 구현/I 설치/R 기록) · `docs/article-map.md` 37행(정본 문장↔파일) · `verbatim.lock` + `article-blocks.sha256` · 훅 4 · plan-sync 훅 · `detect-band.py` 141줄+19시험 · `adopt.sh` 멱등 설치기(22단정) · 도그푸드 `intent/000{1..8}/{intent,spec,plan}.md` · ruleset protect-main.
- 값진 것: 「verbatim」이 독립 재현으로 13/13 바이트 동일(후보 중 유일) · `bands.yml` 이 5일 연속 실제로 돎(`tier: none`) · `adopt.sh` 마커 병합(`begin vX … end sha256:H` — 손편집·업그레이드·충돌 3분기) · spec 의 `## Open questions from intent.md`(answered/carried forward) · 훅 exit 2 · intent-template description 이 Stage 1 과 Stage 6 진입로를 한 문장에.
- 뚫린 것: 아티팩트 뮤테이션 5/5 놓침(절 삭제 · `Status: bogus` · 한 줄 intent · spec=intent 복사) · `claude plugin validate` rc=1(`agents` 가 디렉터리 — 자체 validate.sh 는 `[ -e ]` 라 초록) · macOS 에서 `make test` rc=2(ruby Psych 가 `runbook:rollback-deploy` 거부) · jq 부재/깨진 JSON fail-open · protected-paths `./`·`../`·`//` · plan-sync `git  commit`/`git -C .` 우회 + 백틱 불릿 거짓 양성 + 최대 번호 plan 만 읽음 · settings.json 이 4훅 중 1개만 배선 · Stage 1 지표 3종 부재 · validate.sh 가 intent 디렉터리 8개 하드코딩.

### bashebr/ai-native-sdlc — 「플레이북 재현 충실도 최고 + 도구 최다, 그러나 산출물은 무계측이고 훅은 배선되지 않는다」
- 실체: `SKILL.md` 145줄(하드룰 8 + **규칙→집행 매트릭스** + 페이즈 6행) → `references/playbook.md` 190줄(14레슨 5필드 축자) · 스크립트 7(init_workflow · init_org · quick_validate · run_evals · detect_bands 330줄 · gate_ledger · sync_issues) · 시험 7(50 검사) · org 자산 15 · Codex 겸용(산문 치환 + `--framework`) · 저자 자기 결함 이슈 #4.
- 값진 것: 규칙→집행 매트릭스 4열(하드룰|권고층|결정론층|어디서 검사) · playbook.md 5필드 서식 · SKILL(얇게)/references(두껍게) 분할 · `workflow-graph.yaml`(상태 8종 · 엣지 6) · `gate_ledger` 레코드 스키마 11필드 · Western Electric 밴드 검출기 · PR #3 에서 봇 리뷰 루프를 실제로 돌린 흔적.
- 뚫린 것: 산출물 뮤테이션 7건 전부 80/0(quick_validate 는 번들 파일만 센다) · production-gate: read-only 허용목록이 앵커 없는 부분 문자열이고 배포 판정보다 먼저 돎 → `--dry-run=false`(`ls`)·`tools.yaml`·`catalog`·`controls/`·`echo … && kubectl apply -n prod` 8건 무승인 통과 · 스캐폴드가 훅을 배선하지 않음(settings 부재 · 참조 0) · 원장 해시체인 전체 재체인 위조 rc=0 · `gates/` 가 .gitignore 면 미커밋 승인 통과 · 상태 어휘 5벌 · 전이 집행 0 · 대표 예제 expense-tracker 의 plan 파일 5개 부재 · 42★는 북마크(포크 9 전부 커밋 0).

### jcuervo/authoring-ai-sdlc — 「유일하게 아티팩트 검증기를 가졌고, 그래서 검증기의 함정이 가장 잘 보인다」
- 값진 것: `check-all.sh` 의 **템플릿은 반드시 rc=1 · 예시는 반드시 rc=0** 상주 대조 쌍 · 정본 1 + 사본 N + `sync-validator.sh --check` · `--format json` + `schema_version` + rc 0/1/2(2 = 판정 불가) · description 「Does not write spec.md or plan.md」 배타절 · spec 「Not applicable, because…」 강제 · incident 변형 템플릿(「완화는 맥락이지 결과가 아니다」).
- 뚫린 것: `read_status()` 가 파일 전체 첫 매치 — 코드 펜스 안 `Status: accepted` 로 상류 위조(X2 rc=0) · 에이전트 자기 `accepted` OK · 정상 대괄호 산문 6건 error(거짓 양성) · 무관 상류·축자 복사 spec·요구 0건 plan 통과 · warn-only PreToolUse 훅 무효 · conformance 가 임의 frontmatter 필드 허용 · 「Only a human sets it to accepted」 문서 4곳 + 코드 0.

### honghu-ai/sdlc-governance-kit — 「설계 문서는 가장 야심차고, 코드는 그 설계를 모른다」
- 값진 것(아이디어만 — 라이선스 없음): `规范目录设计.md` 의 change-ID 규약(외부 기록 ID 재사용 → `CHG-YYYYMMDD-NNN-slug` · `INC-…`) · 디렉터리 개명 금지 · YAML frontmatter 9필드 · `draft|approved|rejected|superseded` · 2단 인덱스 · 사고↔의도 양방향 · `spec.md.tpl` 84줄 11절(FR/AC 대응 · 정책 약속 5열 표 · 승인 기록 3행) · 정책 스킬 3종 동형 4절(권위 자료 없으면 사칭 금지 · 적용/비적용/미확인 · 부재 PASS 금지) · 「Skill 로 만들지 말 것」 판정.
- 뚫린 것: 훅·CI 0(README 「确定性关卡」 문면과 불일치) · 감사기: 플레이스홀더를 영문 `TODO` 로 바꾸면 빈 스캐폴드 OK rc=0 · 승인 위조 + 무추적 spec 통과 · 절대경로 링크를 FS 루트로 · 비UTF-8 크래시 · 자기 레포 self-audit ERROR 5 · 상태 어휘 4벌(정본 4치가 템플릿에 없음) · 검사가 요구하는 `00_Index.md` 의 생산자 없음 · evals 필드명 `expectations` · 존재하지 않는 `secure-api-review` 로 라우팅 · 블로그 전문 무단 번역 동봉.

### JHashimoto0518/ai-native-sdlc-playbook-sample — 「사슬의 모양을 가장 빨리 보여주고, 사슬의 강제는 하나도 없다」
- 값진 것(아이디어만 — 라이선스 없음): `docs/phases.md` 의도적 미구현 원장 · spec 의 「intent 에서 상속한 제약 / 설계 중 판명한 제약」 절 분리 + 머리 `適用した Skill:` · 시험 이름에 요건 ID · 커밋 타입 `intent:`/`spec:`/`plan:` · CLAUDE.md 「Claude 가 자주 틀리는 것」(이유 포함) · README 대로 6홉 추적 실재.
- 뚫린 것: 9커밋 author date 초 단위 동일(연출 이력 → 메트릭 3종 원리적 불가) · `check-endpoints.sh` 리터럴 grep — `jsonify({**record})`·별칭·`app.py` 익명 라우트(인증 없이 PII 200)에도 rc=0 + 11 passed · 허용리스트 시험 동어반복(`bank_account` 유출에도 11 passed) · 훅 `../`·Bash·python3 부재 fail-open · 「실패하는 테스트」 커밋의 red 가 `ModuleNotFoundError` · 기계 링크 0(R1·R2·CONCERN 하류 참조 0).

### simonsez9510/intent-md-ko — 「한 장짜리 한국어 템플릿 · 검증 0」
- 값진 것(CC BY 4.0): 절 이름 직역(문제/원하는 결과/영향 범위(사용자·시스템·코드·데이터)/제약/미결) · 「완료 판정 = 숫자 또는 관찰 가능한 사실」 · 발주서 대응표(Problem↔배경 · Proposed outcome↔목표+검수 기준 · Constraints↔제외 항목+기간 · Open questions↔막힌 지점) · CLAUDE.md/AGENTS.md 3줄 드롭인 · 「길어지면 기능이 둘」.
- 갈리는 것: 「미결 0건이어야 착수」(레슨은 spec 으로 answered/carried forward) · 「판정을 파일 말미에」(레슨은 merge/closing review — 타임스탬프 없어 메트릭 불가) · `intent/날짜-이름.md` → 승인분 `docs/plans/` 이동(spec 없는 1산출물 재배치) · 제목 `# Intent —`(엠대시) · 검증기·훅·CI 0.

## 6. 차용 목록 (조각 단위)

| # | 조각 | 출처 · 라이선스 | 형태 |
|---|---|---|---|
| 1 | 플레이 문서 8절 골격(What changes / Who runs it / Prerequisites / Infrastructure / How to execute / What it looks like / Governance / How to measure) | jsnkle `docs/plays/*` · MIT | 그대로 |
| 2 | `references/playbook.md` 5필드 서식 + SKILL(얇게 · 하드룰 + 매트릭스 + 색인)/references(두껍게) 분할 | bashebr · MIT | 그대로 |
| 3 | **규칙→집행 매트릭스**(하드룰 \| 권고층 \| 결정론층 \| 어디서 검사) — 단 각 칸에 실재 증명 게이트를 붙인다 | bashebr SKILL.md · MIT | 개작 |
| 4 | `artifact-formats.md` — 사슬 6단을 「아티팩트·경로·작성자·승인자·승인이 무엇을 발화하는가」 1장 표 | jsnkle · MIT | 그대로 |
| 5 | `docs/article-map.md` — 정본 문장 ↔ 파일 1:1(지면 정정 때 조회) | imsungbin · MIT | 개작(코스 레슨 slug 로) |
| 6 | 의도적 미구현 원장(`docs/phases.md`) — 안 한 것을 이름으로 | JHashimoto · 라이선스 없음 | 아이디어(우리 FINDINGS 형식으로) |
| 7 | spec 템플릿 — jsnkle 7절(Summary·Requirements·Design·Acceptance criteria·Areas of concern·Open questions·Out of scope) · jcuervo 필수 4 + 확장 3 + 「Not applicable, because…」 · imsungbin `## Open questions from intent.md`(answered/carried forward) · honghu 11절(FR/AC 대응 · 정책 약속 표 · 승인 3행 — 아이디어) · JHashimoto 「상속 제약/발견 제약」 분리 + `適用 Skill`(아이디어) | 혼합 | 재작성 |
| 8 | intent 변형 템플릿 incident(「완화는 맥락이지 결과가 아니다」 · 「사고 중 피해자 ≠ 수정 영향자」) · defect · feature | jcuervo · MIT | 개작(한국어) |
| 9 | 한국어 절 이름 · 「완료 판정 = 숫자」 · 발주서 대응표 · CLAUDE.md 3줄 드롭인 | intent-md-ko · CC BY 4.0(출처 표기) | 차용 |
| 10 | intent 인터뷰 6문항 + 「Do not write the file until you can answer each」 · Stage 1/6 두 진입로를 한 문장에 담은 description | jsnkle · imsungbin · MIT | 개작 |
| 11 | 게이트 안 상주 대조 쌍(`expect_exit 1` 템플릿 · `expect_exit 0` 예시) + `sync-validator.sh --check` + `--format json`/`schema_version`/rc 0·1·2 | jcuervo · MIT | 그대로 |
| 12 | 결정론 검출기 + 시험: jsnkle `detect.py`+17시험(loop.sh 제외) 또는 imsungbin `detect-band.py`+19시험(라이브 5일) | MIT | 택1 · 개작(sigma==0 모서리) |
| 13 | `adopt.sh` 마커 블록 병합(`<!-- begin vX -->` … `<!-- end sha256:H -->` · 손편집/업그레이드/충돌 3분기 · 22단정) | imsungbin · MIT | 그대로 |
| 14 | 승인 원장 레코드 스키마(id·gate·decision·artifact·commit·approver·evidence·decided_at·expires_at) — 해시체인은 버리고 git 앵커 · `workflow-graph.yaml`(전진 코드 + 폐기 상태 필수) | bashebr · MIT | 개작 |
| 15 | 훅 exit 2 + stderr 계약 형태 — 구현은 재작성(realpath 정규화 · `command -v jq \|\| exit 2` fail-closed · NotebookEdit matcher · 토큰 단위 앵커) | jsnkle · imsungbin · JHashimoto | 재작성 |

## 7. 회피 목록 (공통 실패 패턴 · 근거 후보)

1. 자연어 규범으로 `accepted` 강제 — jcuervo(문서 4곳 · 코드 0) · jsnkle("Refuse politely") · imsungbin(SKILL 산문) · honghu(批准状态只能由…). 
2. 리터럴/부분 문자열 검사 — jcuervo `[…]` 플레이스홀더(정상 산문 거짓 양성) · honghu `待团队填写`(TODO 로 바꾸면 통과) · JHashimoto `jsonify(record)` · bashebr `ls`/`cat`/`more` 허용목록 · jsnkle `production` 철자.
3. 코드 펜스 미처리 — jcuervo `read_status` · honghu 링크 검사.
4. fail-open 훅(jq/파서 부재 · 깨진 JSON · 빈 stdin) — jsnkle 4 · imsungbin 4 · bashebr · JHashimoto(python3).
5. 경로 정규화 부재(`../` `./` `//` `.path` 키) — JHashimoto · jsnkle · imsungbin.
6. exit code 를 의미값과 실패에 겸용 — jsnkle `loop.sh`.
7. 검증 안 된 동봉 예제 — jsnkle `_example`(자기 템플릿 위반) · bashebr expense-tracker(다른 제품) · jcuervo(없는 파일 지명) · JHashimoto(고아 ID).
8. 상태 어휘 다원화 — bashebr 5벌 · honghu 4 · jsnkle 3 · JHashimoto 파일마다.
9. 배선 안 된 훅 — bashebr 스캐폴드 참조 0 · imsungbin settings 1/4.
10. 공식보다 약한 자체 스키마 검사 — imsungbin `[ -e ]` vs `claude plugin validate` · jcuervo 열린 frontmatter · honghu evals 필드명.
11. 번들만 세는 검증 — bashebr quick_validate 80 · imsungbin validate.sh(파일 존재 · 8 디렉터리 하드코딩).
12. 인위 커밋 이력 — JHashimoto 동일 타임스탬프 · bashebr 9초 간격 한 줄 커밋 8건.
13. 검사가 요구하나 생산자 없는 파일 · 동봉 결손 — honghu `00_Index.md` · jsnkle `requirements-dev.txt`/Makefile.
14. 계기보다 강한 문서 — JHashimoto 「빌드를 떨어뜨린다」 · honghu 「确定性关卡」 · imsungbin 「frozen」 · bashebr 「결정론 열」의 미출하 훅.

## 8. 「우리 레포」 설계 판단 지점 (사용자 결정 · 이 보고서는 답하지 않는다)

1. **형태** — 키트(스킬·템플릿·검증기) / 샘플(사슬 1본 시연) / 플러그인+설치기. 셋을 한 레포에 두면 jsnkle 의 `plugin/`·`template/` 분리와 imsungbin 의 도그푸드 `intent/NNNN` 이 선례. 샘플은 N=1 이라 규칙과 우연을 못 가른다(JHashimoto).
2. **정본** — Academy 14레슨(slug 가 안정 좌표 · DOCS.md 3조와 정합) vs 블로그(imsungbin 은 자체 Play 번호를 발명해야 했다).
3. **언어** — 한국어 템플릿이면 마커·상태 어휘를 검사기 리터럴로 쓰지 않는다(honghu TODO 교훈 · jcuervo 영문 반례 문장의 번역 손실).
4. **intent 스키마** — `# Intent:` 접두 유지 여부(bashebr 는 버림 → 파일 내용만으로 종류 판별 불가) · 7필드 + 추가 후보(Date/Created · Source · Out of scope · Record) · 머리 줄 vs YAML frontmatter(honghu 설계 9필드).
5. **상태 어휘·전이** — 한 곳에서 정의(`draft|accepted|rejected|superseded`?) · 누가 옮기나 · 옮긴 증거는 무엇인가(merge 커밋? 원장? 파일 말미?) · 폐기·충돌·재개정.
6. **승인 기록** — 레슨(merge/closing review) · bashebr(원장 파일) · intent-md-ko(파일 말미 판정) 중 무엇을, 그리고 survival rate 를 계산할 수 있는 형태인가.
7. **아티팩트 검증기** — 만들 것인가(7개 중 실효 0) · 축의 어휘 소유(절 이름 = 닫힘 · 해법 제목/산문 품질 = 열림) · 코드 펜스 처리 · 상류 accepted 강제 + 위조 방지 · 동봉 예제 = 첫 픽스처 · 뮤테이션 스윕(M2~M6 · X1/X2)을 게이트에.
8. **강제층** — 훅(exit 2 · realpath · fail-closed · NotebookEdit) / CI 차단 / branch protection+CODEOWNERS — 「배선됐는가」를 스캐폴드 시험에 넣는다(bashebr·imsungbin 교훈).
9. **메트릭** — 첫 대화 시각 필드(자기 신고) 또는 인테이크 레코드 `received_at` · survival rate 계산 경로 · 첫 spec 이후 intent 변경 수는 위상(`git rev-list`)으로.
10. **비엔지니어 경로** — 이슈 템플릿/폼 · Claude Tag · 아니면 명시적 미구현 등재(7개 중 실효 0).
11. **라이선스·표기** — MIT 차용 표기 위치(NOTICE/파일 헤더) · 라이선스 없는 레포(honghu·JHashimoto)는 아이디어만 · 우리 레포의 라이선스.
12. **셀프 도그푸딩** — 레포 자신을 자기 워크플로로 운영할 것인가(imsungbin·jcuervo). 표방하면 그것을 재는 게이트가 따라와야 한다(bashebr·jsnkle 이 대표 예제에서 깨졌다).

## 9. 방법 · 확인 못 함

- 레인: S(sonnet) · A1/A2/A3/A5/A6/A7(opus) · A4(sonnet). 각 레인은 `$SCRATCH/repo` 에 클론, 전 파일 읽기, 검증기/훅/시험 실행, 뮤테이션(양성 대조 → 변조 → sha256 복원), raw 전량 저장. 부모는 레인마다 핵심 수치 6~14개를 raw 에서 grep 으로 재확인했다. 대상 레포에 이슈·PR 은 내지 않았다.
- 확인 못 함(공통): 스킬·에이전트의 실대화 발화(`claude -p` 미실행) · 워크플로 실행(`act` 없음 · imsungbin 만 Actions 실적 확인) · 플러그인 실제 설치 동작 · Linux 재현(macOS 결과가 1차) · 레인별 목록은 각 보고에.
- 검색 한계: `filename:intent.md` 16,512건 중 상위 100 · gh code search legacy 엔진 · 트리 지표는 정규식.
