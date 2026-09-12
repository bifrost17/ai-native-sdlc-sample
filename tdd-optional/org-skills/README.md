# 팀 스킬 설치와 사용

이 폴더는 우리 팀의 선택 가능한 기본 스킬 예시를 배포한다. 아래 기본 설치 안내는 Claude Code용이다.
사용 템플릿에 내장되는 필수 스킬이 아니다. 팀이 채택한 스킬과 프로젝트 정책을 함께 사용한다.

이 패키지는 **tdd-optional 0.1.2**이다. 플러그인 식별자는 intent-sdlc-skills-optional이며 작업별 검증 방식 선택을 따른다.
0.1.2 검증자는 공개 실행 근거가 있을 때 문서 선행 갱신과 사후 복구를 구별한다. 최종 파일·같은 커밋만으로
순서를 추정하지 않으며 이력이 없으면 미검증으로 남긴다. 새 승인 단계·기록 양식·검사기는 추가하지 않는다.
OpenCode 전달은 [어댑터 안내](opencode/README.md)를 따른다.
[0025](https://github.com/bifrost17/ai-native-sdlc-sample/blob/13376e8049c5650c0fe3a8a258a6595f8d3ada8f/docs/experiments/0025-opencode.md), [0026](https://github.com/bifrost17/ai-native-sdlc-sample/blob/13376e8049c5650c0fe3a8a258a6595f8d3ada8f/docs/experiments/0026-muse-spark.md),
[0028](https://github.com/bifrost17/ai-native-sdlc-sample/blob/13376e8049c5650c0fe3a8a258a6595f8d3ada8f/docs/experiments/0028-review-tdd.md)은 분리 전 판의 실행 기록이다.
현행 패키지의 설치·파싱과 자연 호출·실제 행동 증거를 구별한다. 선택형은 과거 통과를 승계하지 않는다.

## 프로젝트별 설치·갱신

선택한 `tdd-optional/` 전체(`project/`, `org-skills/`, `.claude-plugin/`)를 별도 위치에 복사해도
설치할 수 있다. `project/` 내용은 별도 제품 저장소 루트로 채택한다. 아래의 경로 두 개를
실제 절대 경로로 바꾸고, 제품 저장소에서 실행한다. 이 안내는 사용자 전역 설치를 변경하지 않는다.

```bash
EDITION_SOURCE=/absolute/path/to/tdd-optional
PRODUCT_ROOT=/absolute/path/to/adopted-product
cd "$PRODUCT_ROOT"
claude plugin validate --strict "$EDITION_SOURCE/org-skills"
claude plugin validate --strict "$EDITION_SOURCE/.claude-plugin/marketplace.json"
claude plugin marketplace add "$EDITION_SOURCE" --scope project
claude plugin install intent-sdlc-skills-optional@intent-sdlc-skills-optional --scope project
claude plugin list --json
```

프로젝트가 선택한 판만 유효하게 로드해야 한다. 다른 판의 플러그인이나 같은 이름의 프로젝트·전역
스킬이 이미 활성이라면 설치 전에 실제 로드 출처와 적용 범위를 확인하고 프로젝트 설정에서 충돌을
해결한다. 이름만 다르게 설치해 두 판의 지침을 함께 적용하지 않는다. 사용자 전역 파일을 자동으로
바꾸거나 기존 설치를 제거하지 않는다.

갱신은 설치 소스·판·로컬 변경을 먼저 확인하고 새 판을 검증한 뒤, 제품 저장소에서
`claude plugin update intent-sdlc-skills-optional@intent-sdlc-skills-optional --scope project`를 실행한다.
로컬 marketplace source를 유지하고 새 세션에서 실제 경로·manifest 판을 확인한다.
캐시 목록이나 파일 복사만으로 새 세션이 본문을 읽었다고 판단하지 않는다.
플러그인 사용은 [공식 문서](https://code.claude.com/docs/en/plugin-marketplaces)를 참고한다.

## spec-policy-pass와 spec-policy

[spec-policy-pass](skills/spec-policy-pass/SKILL.md)는 요구·설계 작성 시 관련 팀 정책 스킬을
실제로 읽고 적용하며, 적용 출처·판과 중요한 정책 충돌/미확인 판단의 근거를 남긴다.
프로젝트의 `design-spec` 등 작성 절차가 문서 형식과 수락 경계를 맡는다. spec.md가 연결한 설계
정본 전체를 같은 판으로 검토하므로 한 파일을 강제하지 않으며, 우려가 없으면 살핀 범위를 밝힌다.
기존 허가와 사람의 결정을 재사용한다. 스킬 부재와 정책 부재를 혼동하지 않는다.

명시적으로 `/intent-sdlc-skills-optional:spec-policy-pass`를 사용하거나
[/intent-sdlc-skills-optional:spec-policy <intent-id>](commands/spec-policy.md)로 조직 수준 명령을 실행한다.
명령은 북극성 PO 프롬프트를 축자로 보존하고 위 정책 검토 역할을 연결한다. 작성 스킬은 프로젝트가
채택한 것을 사용하며 이 플러그인이 별도 작성 단계를 설치하지 않는다.
[PROVENANCE](skills/spec-policy-pass/PROVENANCE.md)는 개정 안내와 초기 설계의 역사적 출처를 보존한다.

## tdd

소스는 [SKILL.md](skills/tdd/SKILL.md), 출처는 [PROVENANCE](skills/tdd/PROVENANCE.md)다.
위 플러그인 설치·갱신으로 함께 배포하거나, 이 `skills/tdd/` 폴더 전체를 채택 프로젝트의
`.claude/skills/tdd/`에 배치한다. 단독 폴더는 다른 연구 자료나 특정 외부 스킬을 필수로 읽지 않는다.
프로젝트가 두 설치 방식을 중복 채택할 필요는 없다.

사용자 또는 현재 plan이 TDD를 선택한 작업 범위에서 자동으로 사용하며 명시 호출은 `/intent-sdlc-skills-optional:tdd`다
(프로젝트 폴더로 설치했다면 `/tdd`). 검증 방식과 선택 이유는 프로젝트 정책에 따라 plan에 기록한다.
TDD 선택 범위의 공통 실행법은 이 스킬, 첫 시험·실행 순서는 해당 plan에 둔다.
다른 방식 선택을 예외 승인으로 만들지 않는다. 혼합 계획에서는 TDD로 정한 부분에만 적용한다. 스킬이 새로운 의무나 승인 권한을 만들지 않는다.
독립 기대의 선행 시험과 의미 있는 RED, 같은 기대의 GREEN, 필요한 리팩터링·회귀를 실제로 확인한다.
이미 GREEN인 동작에는 실패를 꾸미지 않으며, 정당한 시험 수정과 종료된 공개 제어 단계는
현재 계약과 남은 회귀 근거에 따라 다룬다.

새 세션에서 실제 읽은 경로·판과 구현 전 시험/실패 이유·후속 통과의 실행 근거를 확인한다.
소스 폴더나 설치 목록만으로 로드·자연 호출·TDD 준수를 입증했다고 쓰지 않는다.

## sdlc-feedback

일반 `claude` 세션에서 관련 업무를 요청하면 에이전트가 스킬 설명으로 사용을 판단한다.
명시적으로 사용하려면 `/intent-sdlc-skills-optional:sdlc-feedback`도 가능하다. 명시 호출과 자연스러운
업무 요청에서의 자동 사용은 실험에서 구분한다.

| 이벤트 | 수행 |
|---|---|
| 요구·설계 변경, 계획 이탈, 새 수락 판 | 연결된 설계 정본을 포함한 필요한 spec/plan과 하위 참조를 갱신 |
| 관련 커밋 준비 | 실제 포함 파일·선택 방식의 독립 기대·검증 근거를 확인하고 영향 문서와 구현을 함께 기록 |
| 구현 완료 보고 전 | 새 문맥의 검증자로 현재 결과를 확인하고 중요한 발견을 보완 |
| 리뷰에서 동작 결함 수신 | 선택한 방식으로 진단·수정·회귀 검증; TDD 부분만 수정 전 자동 RED 확인 |
| PR의 변경 검토 | 제출 diff와 spec/plan 대조; 댓글·CI·push는 기존 PR 도구가 담당 |
| 현황·질문·단순 산문 정정 | 불필요한 문서 변경·독립 구현 검토를 하지 않음 |

원본은 [SKILL.md](skills/sdlc-feedback/SKILL.md), 공통 판단 기준은
[sdlc-verifier.md의 Review criteria](agents/sdlc-verifier.md#review-criteria)다.
[sdlc-verifier](agents/sdlc-verifier.md)는 동등한 프로젝트 검증자가 없을 때 쓸 기본 예시다.
업무 대화는 주 세션에 유지하고 필요한 합의·수락·기준·증거를 검증자에게 전달한다.
완료 전 새 문맥 검토는 이 스킬을 채택한 팀의 의도적 규칙이다. 새 문맥·다른 모델만으로 독립 기대나
정답이 보장되지는 않는다. 먼저 요구·기준 입력의 기대를 읽고 구현·시험 diff와 대조하며, 구현을
숨긴 별도 테스트 생성 실험과 구별한다. UI·탐색에서는 허용된 브라우저/직접 관찰의 절차와 결과도
검토한다. 탐색의 질문에 답한 것과 제품 편입에 필요한 AC·회귀·통합 검증을 구분한다.
해당 PR 범위와 전체 공개 단위를 구별하고, 최신 결합/머지 결과와 실제 시험 근거를 인계한다.
이미 허가된 현재 draft 작업을 과거 수락 판과 혼동해 새 승인 절차를 만들지 않는다.
기본 검증자는 자신의 정의에 공통 판단 기준을 함께 받는다. 별도 기준 파일을 찾거나 그 경로를
전달할 필요가 없다. 다른 프로젝트 검증자를 쓰면 동등한 기준을 확인·인계한다.

일반적인 작은 구현은 Sonnet과 적정 추론을 사용한다. 기본 검증자는 여러 문서의 중요한 합의를
대조하므로 Opus/high로 설정했다. 팀은 난도·영향·불확실성과 사용자 한도에 맞게 조정한다.
더 강한 모델이 모든 오류를 없애지는 않으며, 검증자에게 Bash가 있다는 것은 셸 전체가 읽기
전용이라는 뜻이 아니다. 프로젝트 권한과 보고 전용 지침을 함께 적용한다.

스킬은 에이전트가 사용을 판단하는 지침이다. 매 응답 실행이나 강제 승인 장치가 아니다.
0018의 [sdlc-claude](https://github.com/bifrost17/ai-native-sdlc-sample/blob/13376e8049c5650c0fe3a8a258a6595f8d3ada8f/team-harness/README.md)는 별도 실행·기록 실험 도구로 남으며 일반 스킬
경로에서 호출하지 않는다. 그 CLI 전용 프롬프트는 0018 실험판으로 유지하고 새 스킬의 기준은
위 공통 파일에서 관리한다. 설치와 호출의 실제 근거는 [0019 기록](https://github.com/bifrost17/ai-native-sdlc-sample/blob/13376e8049c5650c0fe3a8a258a6595f8d3ada8f/docs/experiments/0019-event-review-skill.md)에 둔다.
