# U7 — 문서 동기화 훅 설계 제안

Status: draft

2026-10-03, Asia/Seoul. 제작 source 기준은 `df3ae99c3ba9bab5b656a0761aa52ba7a733bb79`다.
이 보고서는 후속 설계 제안이며 source 구현·설치·실제 모델 실행·독립 검토 완료 기록이 아니다.
같은 checkout의 다른 WIP는 읽기 대상으로만 취급했다. 작성 소유 범위는 이 파일 하나다.

## Recommendation

팀이 선택해서 설치하는 Git `pre-commit` 예시를 권한다. 현재 개발 세션이 기존
`sdlc-feedback`으로 문서 영향을 판단하고, 훅은 **그 판단에서 필요하다고 선언한 문서 변경이
검토한 staged 범위에 함께 있는지** 확인한다. 확인 신호가 없으면 커밋을 멈추고 현재 세션의
검토·보완 후 재시도를 안내한다. 별도 모델 프로그램이나 영구 검토 장부를 만들지 않는다.

이는 누락을 한 번 더 드러내는 장치다. 문서 개정 필요 여부, 개정 내용의 정확성, 실제 스킬 수행을
훅이 증명하지 않는다. 검토자가 필요한 문서를 잘못 제외하거나 형식 수정만 올리면 기계 검사는
통과할 수 있다. 이 한계를 숨기고 “spec·plan 동기화 보장”이라고 부르지 않는다.

## Basis

- [북극성 V4-11](../../../verification/north-star-playbook.html#V4-11) 본문은 구현이 계획에서
  벗어나면 같은 commit에서 plan을 갱신하고, 동기화 hook 도입을 고려하라고 한다. hook은 선택이다.
  주석은 같은 커밋 갱신 관측과 누락 사례, 0018 하네스의 false pass, 0019 스킬의 복구를 구분하며
  `부분`을 유지한다. 이번 제안만으로 그 판정을 올리지 않는다.
- [V8-02](../../../verification/north-star-playbook.html#V8-02)는 작업 중 feedback loop와 완료 시
  새 문맥의 최종 검토를 구분한다. 커밋 직전 주 세션의 확인을 매번 fresh verifier로 바꾸지 않는다.
- [제품 Git 정책](../../../../tdd-optional/project/docs/GIT-WORKFLOW.md)은 실제 staged 범위와
  관련 unstaged·untracked 작업을 대조하되 무관한 WIP를 포함하지 않게 한다. 계약·계획의 의미가
  달라진 문서만 갱신하며, 커밋 뒤 실제 내용을 다시 확인한다.
- [제품 절차](../../../../tdd-optional/project/docs/PROCESS.md)는 작은 변경의 짧은 문서와
  기존 plan·실행 기록을 허용한다. [전달 정책](../../../../tdd-optional/project/docs/CHANGE-DELIVERY.md)은
  같은 커밋이라는 사실로 작성 순서나 시험 성공을 증명하지 못한다고 명시한다.
- [공통 feedback](../../../../tdd-optional/org-skills/skills/sdlc-feedback/SKILL.md)의
  `Change or acceptance`, `Implementation and commit`이 의미 판단을 이미 맡는다.
  [검토 기준](../../../../tdd-optional/org-skills/agents/sdlc-verifier.md)은 파일 변경 여부가 아닌
  합의·diff·증거의 의미를 읽고, 영향 없는 문서 수정과 새 승인 단계를 요구하지 않는다.
- [maker CLAUDE.md](../../../../CLAUDE.md)의 제작용 `.claude/hooks/`와
  [0018 team-harness](../../../../team-harness/README.md)는 제품 기본 설치가 아니다.
  하네스는 역사적 선택 실험으로 남아 있으며 현재 팀 기본 경로는 스킬과 native verifier다.

spec 개정을 관련 구현과 연결하는 정책은 제품의 선택이다. 북극성 V4-11의 직접 요구를 모든
spec 변경으로 확대하지 않는다. 특히 제품 Git 정책상 새 상위 수락판을 먼저 기록한 경우에는
이미 커밋한 spec을 형식적으로 다시 수정하지 않는다. 이번 구현에 필요한 plan의 참조·이유·개정이
같이 들어가는지 판단한다. 초기 intent→spec→plan의 단계별 커밋도 계속 허용한다.

## Boundary

Git 훅의 입력·종료 코드와 에이전트 native 도구 호출은 서로 다른 실행 경로다. 현재 저장소에는
Git 프로세스가 진행 중인 Codex·Claude 세션에 공통으로 native skill 호출을 시키는 연결이 없다.
훅에서 스킬 이름을 출력하는 것은 안내이며 호출 성공의 증거가 아니다. 별도 `claude -p` 또는
`codex exec`를 띄우면 다른 실행·문맥·비용·권한 관리가 필요하므로 이번 안에서 제외한다.

흐름은 다음과 같다.

1. 커밋할 staged 변경을 준비하고 현재 개발 세션에서 관련 합의·문서·diff를 읽는다.
2. 기존 feedback 기준으로 이번 커밋에 함께 있어야 하는 문서 개정 목록을 정한다. 필요한 개정을
   작성하고 관련 부분만 stage한다. 영향이 없으면 목록은 빈 배열이다.
3. 최종 staged 내용을 확인한 뒤 그 범위의 지문과 문서 목록을 커밋 명령 한 번에 전달한다.
4. 훅이 지문과 포함 조건을 확인한다. 신호 누락·불일치·필수 문서 미포함이면 non-zero로 끝난다.
   현재 세션이 오류를 읽고 필요한 확인·보완 후 다시 시도한다. 훅은 자동 resume이나 재시도 루프를 돌리지 않는다.
5. 커밋이 만들어지면 기존 Git 정책대로 실제 내용을 확인한다. 인도 완료라면 기존 완료 검토를
   별도로 적용하며 이 훅의 통과로 대체하지 않는다.

## Minimal interface

이름은 구현 제안이며 현재 존재하는 명령이 아니다. 공통 Python 표준 라이브러리 스크립트 하나에
읽기 전용 `snapshot`과 `check` 동작을 두고, 작은 `pre-commit` 진입점은 `check`만 호출한다.
shell 명령문을 파싱해 `git commit`을 찾아내는 Claude 전용 PreToolUse 탐지기는 추가하지 않는다.

커밋 명령에만 전달하는 `SDLC_DOC_SYNC` 환경변수는 다음 JSON을 받는다.

```json
{
  "snapshot": "<검토한 HEAD와 staged diff의 지문>",
  "documents": ["changes/0002-example/plan.md"]
}
```

- `snapshot`: `HEAD`의 실제 object ID(첫 커밋은 명시한 unborn 값)와 canonical staged diff의
  바이트를 구분 가능한 형식으로 묶은 SHA-256. diff는 binary·full-index를 포함하며 external diff,
  textconv, rename 추정을 끄는 고정 옵션을 쓴다. 구현에서는 현재 디렉터리와 display 설정에
  영향을 받지 않도록 저장소 루트와 diff 옵션을 고정한다. unresolved index는 오류다.
  지문은 현재 index가 검토 대상과 같은지 비교하는 값이며 검토자의 서명이나 인증서가 아니다.
- `documents`: 의미 판단으로 이번 커밋에 필요하다고 결정한 저장소 상대 경로의 정확한 목록.
  `spec.md`·`plan.md`라는 파일명이나 `changes/` 경로를 하드코딩하지 않는다. 기존 `intent/`,
  여러 설계 정본, 새 문서·의도된 삭제/이동도 실제 staged 경로로 전달한다.
  경로 escape·glob·중복·잘못된 타입은 오류이며, 공백과 한글 경로는 그대로 취급한다.
  NUL 구분 Git 출력으로 경로를 읽고 JSON 목록의 각 경로가 staged 변경 집합에 있는지 비교한다.
- 빈 `documents`는 “이번 커밋에 동반해야 할 문서 개정 없음”이라는 자가선언이다. 작은 오탈자,
  기존 계약 그대로의 버그 수정, 이미 수락·커밋한 문서를 사용하는 작업 등에 사용할 수 있다.
  변경이 없다는 판단의 이유는 필요할 때 기존 대화·커밋 본문에 남긴다. 별도 양식을 만들지 않는다.

신호를 `export`하거나 셸 초기화 파일에 저장하지 않는다. 명령 한 번의 환경으로만 전달한다.
이는 관행상 일회성이며 소비 여부를 저장하는 토큰은 아니다. 같은 HEAD·같은 staged 범위에
값을 다시 쓰는 것을 암호학적으로 막지는 않는다. 지속 장부 없이 이보다 강한 재사용 방지를
약속하지 않는다. `snapshot` 생성기가 의미 검토를 대신한 것으로 표현해서도 안 된다.

검사 결과는 세 가지 사실만 구별한다. 신호가 유효한지, 검토 대상으로 선언한 지문과 현재
Git 커밋 대상이 같은지, 선언한 문서가 실제 staged 변경에 있는지다. 새 상태 vocabulary나
테스트·수락·배포 판정을 추가하지 않는다. 오류 안내에는 빠진 경로 또는 지문 불일치와 다음
행동을 쓰고, 스킬 수행을 인증했다는 문구는 쓰지 않는다.

## Staging and limits

훅은 `git add`, reset, stash, checkout, 자동 문서 편집을 하지 않는다. 부분 stage는 유지한다.
작업 트리의 plan이 완성돼 있어도 그 개정이 staged에 없으면, 해당 경로를 필수로 선언한 커밋은
막는다. 문서 일부만 stage한 경우 그 부분이 의미상 충분한지는 개발 세션이 staged blob/diff를
읽고 판단한다. 훅이 파일 경로만 확인하는 점은 남는 한계다.

관련 unstaged·untracked 내용은 기존 feedback에서 읽는다. 모든 WIP를 지문에 묶어 무관한 편집으로
커밋을 막지 않는다. 따라서 검토 뒤 작업 트리만 바뀐 상황의 의미 영향은 훅이 감지하지 않는다.
동일 index를 동시에 수정하지 않는 협업 전제와 커밋 후 확인을 유지한다. Git이 훅에 넘긴
`GIT_INDEX_FILE`을 존중해 path-limited commit의 실제 대상 index와 비교하며, 그 범위가 앞서
검토한 staged 대상과 다르면 새 범위를 확인하기 전까지 차단한다. 별도 staging 우회 경로를 만들지 않는다.

`--no-verify`, 훅 미설치·제거, 설정 우회, 거짓 빈 목록, 지문만 다시 계산하는 행위는 막지 못한다.
이는 협조적인 개발자·에이전트가 지침을 대체로 따르는 현재 신뢰 전제에 맞춘 로컬 보조 장치다.
조직 승인·보안 경계·원격 merge 강제로 설명하지 않는다. 기계 검사와 판단을 더 강하게 묶겠다는
이유로 서명 서버·receipt ledger·상시 모델 감독을 추가하지 않는다.

## Adoption and adapters

배포 위치는 `tdd-optional/org-skills/examples/` 아래 선택 예시가 적합하다. 제품 기본
`project/`와 maker `.claude/settings.json`에 활성 훅을 넣지 않는다. 팀 스킬 설치만으로 채택하거나
Git 훅을 활성화하지 않는다. 공통 feedback 본문에는 채택한 경우의 커밋 확인 연결만 짧게 추가하고,
설치·입력 상세는 예시에 둔다. 설치 대상에는 companion 예시도 접근 가능하게 전달해야 한다.

Claude는 현재 플러그인의 feedback, Codex는 현재 프로젝트에 설치한 같은 스킬과 adapter를 읽는다.
양쪽 모두 같은 Git hook과 JSON 계약을 사용한다. native verifier 전달 차이는 기존 adapter가
맡으며 이 훅을 위한 Codex runtime API나 Claude 전용 모델 프로세스를 만들지 않는다.
Claude/Codex의 채택 안내에는 관련 커밋 직전 feedback을 확인하는 사건을 명시한다.
스킬 이름·파일이 보이는 것, 본문을 읽은 것, 실제 검토한 것은 별도 근거로 유지한다.

첫 버전은 새 범용 installer 대신 예시와 명시적인 저장소별 설치 절차로 충분하다. 대상 repo와
실제 hooks 경로·`core.hooksPath`·기존 hook 유무를 읽은 뒤 비어 있는 저장소 로컬 경로에만
설치한다. 기존 hook/관리자 설정/사용자 전역 경로가 있으면 덮어쓰거나 몰래 우선순위를 바꾸지 않고
그 팀의 기존 설치 방식으로 합친다. linked worktree의 공통 hooks 디렉터리는 다른 worktree에도
영향을 줄 수 있으므로 설치 범위를 repo 전체로 명시한다. 도구별 skill installer에 자동 활성화를
끼워 넣지 않는다. 향후 installer를 만들더라도 명시 선택 옵션과 실제 대상에만 한정한다.

변경하지 않을 설정은 사용자 전역 Git·Claude·Codex 설정, shell PATH, parent model, reasoning,
approval, sandbox, MCP, 기존 plugin·검증자 선택이다. 플러그인의 프로젝트 설치가 사용자 cache에
파일을 둘 수 있다는 기존 안내는 유지한다. 설치 완료는 스킬 수행·모델 행동 통과가 아니다.

## Scope decisions and cost

| 선택 | 이유와 tradeoff |
|---|---|
| 주 세션 self-review + 지문/필수 경로 확인 | 기존 의미 판단을 재사용한다. 수행의 진위·목록의 완전성은 인증하지 못한다. |
| 모든 활성 pre-commit에 같은 간단한 신호, 빈 목록 허용 | 코드 확장자·커밋 제목으로 문서 영향을 추측하지 않는다. 작은 커밋도 짧은 확인 부담은 생긴다. |
| 인도 완료의 fresh review는 기존 규칙 유지 | 매 커밋의 모델 비용을 늘리지 않는다. hook 통과가 완료 검토를 대신하지 않는다. |
| 로컬 opt-in, 기본 제품 설치에서 비활성 | 팀 선택을 지킨다. 미설치·우회 경로는 통제하지 않는다. |

훅 자체의 모델 호출 예산은 0회, 네트워크 호출도 0회다. self-review는 이미 필요한 커밋 전
영향 확인에 통합한다. 작은 개발건에 새 문서·새 review 파일·새 승인 질문을 요구하지 않는다.
문제 해결이 반복되면 같은 근거를 다시 읽어 기계 오류인지 의미상 미결정인지 구분하고 인계한다.
자동 모델 보완 루프·승격·N회 재시도 예산은 추가하지 않는다. 중요한 의미 판단의 모델/추론은
기존 난도·영향·불확실성 기준으로 고른다.

## Required follow-up before implementation

0028 [spec](../../../../intent/0028-openwebagent-history-feedback/spec.md) SP05의 “새 자동 검사기”
금지와 FR08의 여섯 단위는 이번 후속 사용자 선택을 반영해야 한다. U1–U6의 이전 범위를 소급해
고치지 말고, opt-in 문서 포함 확인이라는 U7의 좁은 추가 범위를 기록한다. 기존
CHANGE-DELIVERY의 “commitlint·새 hook” 금지는 메시지 형식 검사와 이번 선택 예시의 범위를
명확히 구분한다. 새로운 사람 승인을 요구하는 충돌이 아니라 이미 주어진 후속 결정의 문서 반영이다.

구현 전에는 root가 위 설계를 현재 spec/plan의 책임 단위로 연결한다. 구현·검토 시 확인할 핵심은
다음과 같으며, 지금 실행했다는 뜻은 아니다.

- 신호 누락/잘못된 JSON, 지문 불일치, 선언 문서 누락을 차단하고 정상 빈 목록·동반 개정은 허용한다.
- 문서의 unstaged 개정만 있는 경우, 부분 stage, 관련 없는 WIP, 첫 커밋, amend, 삭제/이동,
  공백·한글 경로, 다른 index를 쓰는 commit에서 실제 대상과 보존 범위를 확인한다.
- 기존 hook이 있는 설치 대상과 공유 worktree, hooksPath 설정 대상에 예기치 않은 덮어쓰기나
  전역 변경이 없는지 확인한다. 설치 미채택 제품의 기본 동작은 유지한다.
- 같은 공통 source의 Claude/Codex 전달 예시·adapter·companion 설치 참조를 확인한다.
  실제 native 세션의 의미 판단·hook 실패 후 보완 행동은 별도 실행 증거 없이는 미검증이다.
- 거짓 빈 목록이나 의미 없는 문서 수정이 기계 검사만 통과할 수 있음을 숨기지 않는다. 이것을
  막기 위해 매 커밋 LLM 심판을 덧붙이지 말고 기존 의미 검토의 한계로 남긴다.

## Review and provenance

이 작성자의 설계 검토는 V4-11/V8-02, 제품 정책, 공통 feedback/검토 기준, Claude/Codex 전달
경로, 기존 maker hook·team-harness의 경계를 읽은 self-review다. 별도 fresh 검토·구현 검증·
사용자의 최종 수락을 주장하지 않는다. 중요한 남은 검토점은 지문 canonicalization과 실제 Git
index 경로의 구현 정확성, 예시 companion의 도구별 전달 누락이다. 의미 판단을 기계적으로
입증하지 못하는 한계는 설계에서 의도적으로 수용한다.

적용한 세션 스킬은 `/Users/jake/.agents/skills/sdlc-feedback/SKILL.md` (설치 표기 0.1.7),
`spec-policy-pass`, `brand`, `stop-slop-ko` (각 `/Users/jake/.agents/skills/<name>/SKILL.md`,
설치 표기 0.1.6)다. 설치 manifest 자체의 hash 일치는 이번에 검사하지 않았다. 프로젝트 기준은
위 현재 source를 우선했다. 제품 PROJECT-POLICY의 빈 이름/시간대 슬롯은 채택 팀이 정할 값이며
maker 보고서의 새 승인 공백으로 간주하지 않는다. 외부 API·민감 응답·새 로그 저장소는 설계하지
않으므로 secure-api-review/data-compliance 범위의 새 정책 계약은 추가하지 않았다.

기존 기억은 북극성 우선·실험 유예·원문 보존의 탐색 방향에만 사용했고 위 파일 내용을 현재
checkout에서 읽었다. 이 보고서 전문을 보존하며, root가 후속 단위 검토와 source 반영 여부를 정한다.
