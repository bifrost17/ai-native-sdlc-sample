# 스킬 전달 설계

2026-09-12 · 제안이며 설치 파일을 생성하거나 활성화하지 않았다.
원칙은 **같은 업무 지식, 얇은 플랫폼 변환, 필요한 본문만 읽기**다.
아래 16개는 제공 범위이며 호출 의무나 통과 개수가 아니다.

## 조건 A — 최대한 native로 제공

| 자료 | 수 | 제공 방식 | 필요한 조정 |
|---|---:|---|---|
| brand, data-compliance, secure-api-review, spec-policy-pass, tdd, stop-slop-ko | 6 | `.opencode/skills/<name>/` | 전체 폴더·참조·라이선스·출처 보존 |
| accessibility, secrets-scan, grilling | 3 | 같은 native 경로 | 필요한 로컬 참조 보존. 미포함 선택 자료는 알려진 제한으로 기록; grilling의 위임은 실제 실행 별도 관측 |
| sdlc-feedback | 1 | 같은 native 경로 + `.opencode/agents/sdlc-verifier.md` | 상대 기준 경로 보존, agent 이름과 설정·모델 계약 변환 |
| ux-copy | 1 | 같은 native 경로 | 인자를 현재 요청에서 읽는 지침으로 바꾸고 CONNECTORS 링크를 실제 동반 파일로 연결 |
| capture-intent, design-spec, plan | 3 | 사용판 `examples/skills/` → 제품 `.claude/skills/` | 프로젝트 상대 경로 유지. 이번 실행에서 명시 채택한 자동 선택 가능 스킬로 기록 |
| to-questionnaire | 1 | `team-resources/skills/to-questionnaire/` | 명시 요청 때 참고하는 파일. 자동 호출 금지 옵션이 지원된다고 주장하지 않음 |
| pr-loop | 1 | `team-resources/skills/pr-loop/` | 원문 보존. 이번에는 hosted PR이 없으므로 외부 PR loop는 미관측 |

**native 14개 + 파일 참조 2개 = 총 16개**다.
이전 검토의 최소 핵심 세트보다 이번 사용자의 “최대한 설치/참고” 목적에 맞게 제공 범위를 넓혔다.
F04에 서버 API·웹 UI가 없다고 API/접근성 스킬을 억지로 실행하지 않는다.
UX 원칙은 CLI 오류 안내에도 관련될 수 있다. 매번 긴 UX 보고서를 별도 생성할 필요는 없다.

OpenCode는 프로젝트 `.opencode/skills`와 `.claude/skills`를 발견하고 native skill 도구로 본문을 읽는다.
지원하지 않는 frontmatter는 무시한다. 세 작성 예시의 `disable-model-invocation`을 제거/수정하는 것은
이번 실험의 명시 채택에 따른 변화로 남긴다. 수동 사용 의도를 유지할 to-questionnaire는 발견 경로 밖에 둔다.
[공식 Skills 문서](https://opencode.ai/docs/skills/).

설치하면서 SKILL.md만 떼어 내지 않는다. references/examples/plays/templates/LICENSE/PROVENANCE를
함께 보존한다. 원본의 상대 경로, 프로젝트 정책 의존성과 실제 접근 가능 범위를 확인한다.
보조 스캐너·MCP·외부 서비스를 자동 설치하거나, brand/API 예시를 새 검사기로 만들지 않는다.

ux-copy의 `$ARGUMENTS`는 현재 요청/선택한 문구를 뜻하도록 얇게 수정한다.
Claude 커넥터 placeholder를 실제 연결인 것처럼 쓰지 않고 이번 CLI 환경의 부재를 명시한다.
pr-loop의 인자·셸 전처리를 무리하게 흉내 내지 않는다. hosted PR을 실제 시험하는 후속 건에서
[OpenCode commands](https://opencode.ai/docs/commands/)의 지원 문맥으로 맞춘다.
spec-policy 명령은 기존 등록 근거가 있지만 본 실험에는 필수가 아니므로 기본 제공에 추가하지 않는다.
자연 업무에서 policy skill을 사용하는 관측을 명령 강제 호출로 대체하지 않는다.

## 참고 파일 색인

두 조건 모두 프로젝트에 `team-resources/INDEX.md` 한 파일을 둔다.
각 자료의 이름·짧은 용도·native/파일 구분·실제 경로·원본 판/변환 판을 제공한다.
이는 온보딩과 경로 안내이며 평가 정답표가 아니다.

- 기존 description에 기반한 한 줄 용도만 적는다.
- F04-D7, 미래 JSON 요구, 실패 이력, 채점 기준, 호출 횟수나 단계별 강제 순서를 넣지 않는다.
- “이번 단계에 반드시 tdd와 sdlc-feedback을 호출하라”는 식의 답을 주지 않는다.
- 필요한 본문과 연결 자원을 읽게 하며 16개 전문을 시스템 지침에 한꺼번에 넣지 않는다.
- 파일만 제공된 스킬도 AGENT가 스스로 관련성을 판단해 읽을 수 있다.
  단, to-questionnaire는 자료 색인만 보고 자동 질문 워크플로를 시작하지 않도록 명시 사용 조건을 유지한다.

A에서 native 스킬을 직접 파일 Read로 읽었다면 그 자체로 실패가 아니다.
실제 적용 증거로 인정하고 로딩 경로를 파일 읽기로 기록한다.
색인을 제공한 실험을 ‘아무 안내도 없는 자동 발견’이라고 부르지 않는다.

## 조건 B — 같은 지식을 파일로 제공

설치/호출 경로가 중요한 차단 원인일 때만 사용하는 대안이다.
A와 같은 원본·업무 본문·정책·작성 양식·교육 예시를 유지하며
16개를 `team-resources/skills/<name>/` 전체 폴더로 제공한다.
프로젝트에서 세 단계 아래이므로 작성 예시의 `../../../templates` 같은 연결을 유지할 수 있다.

B 세션에서는 대응하는 14개가 native 위치나 전역 경로에서 중복 제공되지 않아야 한다.
별도 조건 clone·프로필을 사용하고 실제 세션 노출을 확인한다. 개인의 영구 설치를 삭제하지 않는다.
OpenCode의 [패턴별 skill 권한](https://opencode.ai/docs/skills/)을 활용할 수 있으나
파일 Read까지 차단하거나 “도구를 껐다 = 모든 전역 오염이 사라졌다”고 가정하지 않는다.
분리가 불가능하면 순수 파일 조건이 아니라 혼합/오염 조건으로 기록한다.

색인의 용도·온보딩 문장은 A와 같은 수준으로 두고 위치만 실제 파일 경로로 맞춘다.
평가 대상 이벤트 직전 동일 스냅샷에서 새 session을 시작한다.
A에서 생긴 정답·리뷰 발견·이후 합의를 새 입력으로 추가하지 않는다.

스킬 전달 방식만 보려는 B에서는 **독립 검증자는 A와 같은 OpenCode agent 구성**을 유지한다.
파일형 feedback에서 참조할 기준은 실제 `.opencode/agents/sdlc-verifier.md`로 연결하고
그 경로 변환을 기록한다. 별도 기준 본문 사본을 늘려 서로 달라지게 만들지 않는다.
native 검증자도 작동하지 않으면 아래 수동 검토 대안을 별도의 환경 변화로 표시한다.

## 독립 검증자

원본 `org-skills/agents/sdlc-verifier.md`의 Review criteria를 유지하고
OpenCode의 `mode: subagent`, `steps`, `permission`, 실제 provider/model 설정으로 변환한다.
agent 명칭은 `sdlc-verifier`로 통일한다.
[공식 Agents 문서](https://opencode.ai/docs/agents/).

선행 검토의 [native-draft.patch](../probes/native-draft.patch)는 파싱 초안이다.
최종 권한 설정으로 그대로 승계하지 않는다. 개발 파일 수정·Git 변경은 맡기지 않고,
현재 자료·diff와 시험을 확인해 발견/미확인만 반환하게 한다.
시험과 셸을 허용했다고 완전 읽기 전용이 기계적으로 보장된다고 주장하지 않는다.
기존 비밀 파일 접근 제한 등 프로젝트 권한도 보존한다.

검증자 입력은 다음 최소 묶음이다: 작업/PR 범위, 현재 HEAD와 dirty/untracked 상태,
공개된 최신 합의·수락 SHA, 필수 설계/plan 경로, 실행한 시험과 남은 미확인.
HUMAN oracle·미공개 결정·이전 정답은 넘기지 않는다.
검증자 결과를 기다리고 현재 판과 대조해 AGENT가 보완한다. 매 답변마다 검증자를 호출하지 않는다.

위임이 기술적으로 불가능하면 HUMAN이 **별도 OpenCode 리뷰 session**에 같은 묶음과 기준 파일을
넘겨 수동 독립 검토를 할 수 있다. 자동 위임·대기의 성공으로 계산하지 않는다.
같은 개발 세션의 자기 검토만 가능하면 제품 검증을 HUMAN이 보완하되 독립 검토는 미관측이다.

## 실행 준비에서 확인할 사항 — 지금은 미실행

1. CLI 판, 지원 인자, 모델/추론과 실제 세션의 지침·스킬·agent·plugin·MCP 노출을 기록한다.
   기존 aside-browser 등 전역 자료가 남으면 숨기거나 미사용 여부와 영향을 기록한다.
   커스텀 config 디렉터리나 `--pure`만으로 사용자 스킬까지 격리됐다고 가정하지 않는다.
2. 활성 경로·본문·동반 자원·agent 파싱과 중복 이름을 확인한다.
   현재 사용판에 없는 Claude hooks를 새로 만들거나 OpenCode에서 실행됐다고 쓰지 않는다.
3. S1 전에만 정상 읽기·대화 이어가기·검증자 전달 경로를 작은 공개 임시 자료로 점검할 수 있다.
   F04 정답·평가 이벤트는 사용하지 않고 준비 비용도 기록한다.
   명시 호출 probe는 자연 선택의 성공 근거가 아니다.
4. 설치/변환은 HUMAN 준비 작업으로 끝내고 판을 고정한다.
   AGENT가 개발 도중 설치 스킬/정책을 자기 편의로 고치면 변화와 사유를 먼저 기록한다.
5. 후속 구현 시 저장소에 선택 목록·변환 파일·설치/갱신/제거 안내·출처 manifest를 함께 보존한다.
   거대한 installer나 의미 채점기를 만드는 것은 이 설계에 포함되지 않는다.
