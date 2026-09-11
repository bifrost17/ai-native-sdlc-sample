# Plan: 팀 스킬 배포와 네이티브 Claude Code 대화 검증
Upstream: spec.md@55f6af3 (root가 사용자의 위임으로 기준 인계 단순화를 수락). Status: draft.

## Files that change
- org-skills/skills/sdlc-feedback/{SKILL.md,PROVENANCE.md}(new): 이벤트와 출처. 중간판의 references/review-criteria.md는 제거.
- org-skills/agents/sdlc-verifier.md(new), org-skills/.claude-plugin/plugin.json: 네이티브 검증자와 플러그인 판.
- org-skills/README.md(new), .claude-plugin/marketplace.json: 설치·갱신·역할·범위 안내.
- README.md, CLAUDE.md, docs/BOUNDARY.md, team-harness/README.md: 기본 팀 스킬 경로와 동결한 0018 CLI 경계.
- docs/experiments/datasets/v5/{manifest.json,cases.json}(new): 작은 부분 사례·고정 기준·평가 범위.
- docs/experiments/0019-event-review-skill.md(new), docs/experiments/README.md: 실제 설치/대화/판정/실패·회귀 기록.
- docs/verification/north-star-playbook.html, INDEX.md, CHAPTERS.md: 원문·집계·이전 실패를 보존하고 새 근거 추가.
- intent/0019-event-review-skill/{intent,spec,plan}.md: 이번 변경의 의도·결정·계획.
- 실험 제품·원본 공개 대화·native agent 출력은 별도 clone과 실험 브랜치에만 보존한다.

## Order of work
1. 주 세션의 얇은 sdlc-feedback과 공통 기준을 담은 독립 sdlc-verifier를 구현한다. forked 운영 스킬은
   업무 대화를 잃을 수 있어 쓰지 않는다. 검증자는 Read/Glob/Grep/Bash로 관측만 하고 재귀·편집은 하지 않는다.
2. 플러그인 판을 올려 검사하고 영구 설치를 갱신한다. 새 일반 Claude 세션에서 실제 로드와 출처를 확인한다.
3. F02 PR1과 기존 사용판을 합친 8dbf319를 고정 실험 기준 브랜치로 둔다. 얕은 clone의 작업 브랜치에서
   기존 summary를 구현한 뒤 JSON 요구를 대화로 추가한다. HUMAN은 응답을 읽고 업무 결정과 수락을 한다.
   일반 구현은 Sonnet/medium, 중요한 후속 합의 대조는 Sonnet/high로 실행한다. 여러 문서의
   중요한 독립 검토는 기본 Opus/high 검증자로 제한해 수행한다.
4. native Agent 호출과 현재 파일 읽기·검증 결과를 관측한다. 후속 요구와 수락을 문서 갱신 상기 없이
   전달하고, plan 참조와 관련 구현 동시 커밋을 확인한다. 질문/현황과 작은 문서 정정도 대조한다.
5. 별도 새 세션에 의도적으로 누락된 문서를 가진 작은 변경을 주고 커밋 준비/PR 범위 리뷰를 요청한다.
   자연 사용과 결함 주입을 구분하고 발견·보완·재검증을 기록한다. 중요한 미호출/오판은 숨기지 않고
   근거가 있는 최소 보완 후 새 세션으로 재확인한다.
6. 기존 제품 시험·fixture 보존과 독립 CLI 동작, 전체 인계의 영향받은 부분을 평가한다. 고정 항목은
   원문/참조 불변과 이전 증거로 재사용한다. 미관측 운영·호스티드 PR/CI는 통과로 세지 않는다.
7. 공개 기록을 정제해 실험 브랜치에 보존하고 제작 make check와 독립 verifier를 수행한다.
   주석·색인·설치 문서를 실제 관측에 맞춘 뒤 로컬 main으로 통합한다.

## Risks
스킬을 읽은 것과 실제 독립 Agent 실행을 혼동, current working tree 대신 HEAD만 검토, 일반 대화의
과잉 검토, 설치 캐시/소스 혼동, 능력 선택 고정, 과거 CLI 성공을 새 스킬의 성공으로 재사용하는 위험.
별도 runtime이나 새 의미 검사기는 만들지 않는다. 실험용 기록 수집은 호출과 원문 보존만 담당한다.

실험 중 조정: 첫 Sonnet/medium 구현은 스킬·검증자를 호출하지 않아 실패로 보존한다. 문서 합의
변경은 Sonnet/high로 실행해 자연 Skill/Agent 호출을 관측했다. 설치 0.1.3에는 설계 리뷰에서 발견한
프로젝트 REVIEW.md/정책 읽기 한 문장과, 비동기 검토가 pending일 때 최종 완료로 보고하지 않는
문장을 보완한다. 기존 CLI나 템플릿에 새 강제 규칙을 넣지 않는다. 실험용 셸 허용 목록에는 실제
검증에 필요한 해시·출력·Git 조회 명령을 추가해 불필요한 도구 거부를 줄인다.

E02 첫 실행은 문서 누락을 발견했지만 주 세션이 기준 파일 경로를 검증자에게 인계하지 않아
공통 기준 로드는 실패했다. 0.1.4는 별도 파일을 없애고 기준을 검증자 본문에 함께 둔다.
주 스킬은 그 공통 부분을 읽되 검증자 전용 권한을 개발 세션에 적용하지 않는다. 기존 실패를
보존하고 같은 누락 사례를 새 세션에서 재실행해 발견·수정·수락·동시 커밋까지 확인한다.

## Proof
plugin validate/skill validate, 새 세션 init과 Skill/Agent 도구 기록, 실제 모델과 추론 설정·실행 시간·비용,
업무 대화·수락 SHA·문서/코드 diff와 commit, 기존 시험/fixture 보존·독립 제품 동작, 제작 make check,
  원문/179 IDs 불변 및 verifier 네 부분 보고. 첫 묶음은 소규모 두 세션과 필요한 정상 대조로 시작한다.

## Execution record

- 최종 설치 후보: 893b79e / plugin 0.1.4. strict plugin/marketplace 검사와 skill quick validation 통과.
- E01 5턴, E02a 1턴, E02b 3턴으로 세 실제 세션에서 진행했다. 첫 미호출과 기준 전달 실패를
  보존한 재실험이므로 처음 계획한 두 세션보다 하나 늘었다. 고정 대본이나 별도 자동 검토 도구는 쓰지 않았다.
- E01은 spec f706c6d 수락 뒤 plan·구현·시험·README를 3873db9에 함께 커밋했다. 제목 정정 후
  제품 c547048. E02b는 spec 8b4395f 수락 뒤 동일 네 파일을 f14c811에 함께 커밋했다.
- 두 제품 각각 unittest 12개와 독립 CLI16/원본7AST/fixture 보존 통과. E02b는 native Agent를
  직접 선택했으며 0.1.4 주 Skill의 새 자연 호출로 계산하지 않는다. 최종 커밋을 native가 재승인한
  것으로 쓰지 않고 주 세션 확인·HUMAN/별도 verifier 근거를 구분한다.
- 제작 make check rc0(96 unittest/skip1, hooks28, eval8, managed settings PASS), production hook
  부정 입력 rc2. 검증 원문과 네 부분 보고는 실험 raw에 보존한다. 기록·주석 마감 검사는 별도로 잇는다.
- 주석의 8개 ID에 새 관측만 추가하며 고정 가이드·원문·역사적 실패·139/23/17 집계는 유지한다.
  전체 평가 범위·미관측 운영·모델/비용·제품/보존 핀은 docs/experiments/0019-event-review-skill.md가 정본이다.
