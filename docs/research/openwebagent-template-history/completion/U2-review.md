# U2 review — 실제 앱과 연결하는 UI 탐색

2026-10-03. 검토자: `owa_finish_u2_review`. 검토 범위에서 중요한 미해결 발견은 없었다. 아래 판단은 문서·스킬의 적용 범위에 관한 제작 리뷰이며, 제품 실행 통과나 사람의 수락을 뜻하지 않는다. source 채택과 다음 단위 진행은 root가 판단한다.

## Scope and actual revision

- 작업 경로: `/Users/jake/Projects/ai-native-sdlc-sample`.
- 지정 diff base와 읽기 시작 시 HEAD: `bcb501f16cbf8a6b00598442d2bcada00817178e`.
- 변경 대상: `tdd-optional/project/examples/skills/design-spec/references/design-depth.md`의 UI 절과 `tdd-optional/project/examples/skills/plan/examples/disposable-ui-exploration.md`. 두 파일 전문과 routing skill을 읽었으며, 새 diff뿐 아니라 현재 0.1.9 후보의 U2 설명 전체를 검토했다.
- source diff: design-depth `+6/-1`, 탐색 예시 `+7/-0`. 다른 미커밋 파일·연구 작업이 있었으며 검토자는 수정하지 않았다.
- 연결: 0028 intent의 UI 심미성·기존 화면 통일성 문제 → FR05/SP04/SP06/SP07 → AC03/AC07 → T07. AC04 실제 개발 효과 비교는 유예 상태다.
- 이번에 작성한 파일은 이 보고서뿐이다. source, 제품, 전역 설치, 배포, Git commit/merge를 변경하지 않았다.

## Actually read contracts

`CLAUDE.md`, 0028 `intent.md`/`spec.md`/`plan.md` 전문을 읽었다. 미관측을 통과로 바꾸지 않는 제약, 사용자 후속 허가, 단위별 제작 리뷰와 U6 패키지 검증을 구별했다.

북극성은 `north-star-playbook.html`의 V3-03 직전 본문과 주석(473–478행), V3-09 본문·주석(515–524행), V8-02 본문·주석(1130–1137행)을 읽었다. V3-03은 mock을 반복해 다듬고 build로 넘기는 예와 해당 도구 경로의 미검증 상태다. V3-09는 문제 해결과 intent 미결 처리에 대한 사람의 검토다. V8-02는 작업 중 피드백과 끝의 독립 확인을 구분한다. 이 세 문단에서 모든 UI 선구현, 특정 도구 사용, 자동 시험만으로 시각 수락을 판정하는 규칙은 도출하지 않았다. 온라인 원문을 새로 조사한 리뷰는 아니다.

두 source 전문, `design-spec/SKILL.md`와 `plan/SKILL.md` 전문을 읽었다. 허용된 탐색은 의존 설계 수락 전에도 가능하고, 탐색 결과를 제품에 채택할 때 영향 spec/AC와 제품 계획을 갱신한다. 최초 planning의 제품 코드 편집 금지는 계획 작성 단계의 범위이며 후속 허용된 탐색 실행의 금지로 확대하지 않았다.

제품 `RELEASE-CONTROL.md`, `TESTING-STRATEGY.md`, `REVIEW.md`, `PROJECT-POLICY.md` 전문과 maker `docs/RELEASE-CONTROL.md`, `REVIEW.md`, `.claude/agents/verifier.md`를 읽었다. 제품 `GIT-WORKFLOW.md`는 단계 수락·후속 변경의 16–40행과 관련 검색 결과를 읽었으며 전문 검토라고 주장하지 않는다. 공개 정책은 필요한 경우의 제어, 신뢰할 시험 대상, 직접 호출과 실제 효과, 인증 보존을 요구한다. 모든 탐색에 새 플래그나 플랫폼을 요구하지 않는다. PROJECT-POLICY의 미정 데이터 값은 실제 채택 정책의 존재 증거로 사용하지 않았다.

W01 `context.md`, `intent.md`, `spec.md`, `plan.md` 전문을 읽었다. 합성 예시임을 유지하며 세션→API→화면, 모의 화면 상태와 실서버 흐름, API만 준비된 단계와 전체 공개 단위, OFF 전파 한계를 대조했다. W01에 등장하는 경로·시험 명령은 실제 제품 파일이나 이번 리뷰에서 실행한 명령이 아니다.

리뷰 방법에는 설치된 `sdlc-feedback/SKILL.md`, 보고서 문장에는 `stop-slop-ko/SKILL.md`를 적용했다. 메모리 `MEMORY.md:517–524`는 북극성 우선·실험 유예·원문 보존 선호를 확인하는 데 사용했고, 현행 판단은 위 checkout의 계약을 직접 읽어 내렸다.

## Adversarial checks and disposition

| 반증하려 한 해석 | 실제 문구와 적용 범위 | 판단 |
|---|---|---|
| 정적 예시의 제품 비연결·중지 지시가 실제 컴포넌트 탐색을 금지한다. | 탐색 예시 13–14행은 해당 정적 plan의 읽기 전용 경계다. 16–25행은 실제 component/앱 셸을 선택할 때 아래 파일·순서·위험 범위를 바꾸라고 하며, 24–25행은 제품 비연결 조건을 모든 UI 설계의 금지 규칙으로 해석하지 말라고 명시한다. | 34–35행/45–47행을 맥락 없이 적용하면 금지로 읽히지만, 현재 전문을 따르는 독자에게 그 충돌은 남지 않는다. 실제 RequestForm 수정은 계획에 파일·범위를 표시하면 가능하다. |
| prototype에서 키보드·취소를 확인하면 제품에서도 완료다. | 예시 3–7행은 합성 입력과 고정 제약이다. 36–40행은 직접 관찰과 탐색 성공 범위를 정하고, 45–55행은 실제 저장·인증·제품 CSS와 최신 통합 판의 검증을 따로 남긴다. | 정적 시안 자체의 조작 관찰은 유효하다. 이를 실제 앱의 전역 키 처리·제출 방지 증거로 승격할 수 없으며 design-depth 24–25행도 그 한계를 설명한다. |
| 모든 초기 UI 코드를 폐기해야 하거나, 반대로 그대로 제품에 넣어도 된다. | 예시 39행은 선택하지 않은 prototype을 폐기한다. 22–24행과 design-depth 29–30행은 편입할 코드·spec/AC·실제 연결·품질·회귀를 요구한다. | 선택한 코드의 재사용을 허용하면서 제품 편입의 남은 일을 유지한다. prototype 재작성이나 무검증 편입을 강제하지 않는다. |
| 자동 시험 통과가 심미성·기존 UI 통일성의 수락이다. | design-depth 22–28행은 실제 기준 화면/컴포넌트/스타일과 사람의 시각 기대·피드백을 연결하고, 자동 시험 통과를 심미성·통일성 수락으로 바꾸지 않는다. 예시 18행도 시각 피드백을 남긴다. | 상태·키보드 자동화와 시각 판단의 근거를 분리한다. 모든 관찰에 추가 사람 승인 단계를 만들지는 않는다. |
| 앱 셸/sandbox라는 이름만 붙이면 일반 사용자 노출이나 실제 쓰기를 허용한다. | design-depth 31행과 예시 22–24행은 현재 공개·데이터 정책을 적용한다. design-depth 17–18행의 직접 정책 링크와 RELEASE-CONTROL의 효과 경계에서 메뉴 숨김만으로 충분하지 않음을 읽을 수 있다. | 격리 경로가 인증·노출·효과 제어를 대신한다는 문구가 없다. 실제 채택 시 어떤 제어가 필요한지는 현재 제품의 접근·효과 경계로 정하며 모든 탐색에 동일 서버 gate를 요구할 근거도 없다. |
| 실제 component를 쓴다는 이유로 모든 화면과 모든 상태를 먼저 완성해야 한다. | design-depth 23–25행은 불확실한 결합과 이번 위험에 닿는 상태를 고르며, 30행은 모든 화면 완성·특정 UI 도구를 요구하지 않는다. 탐색 예시는 질문·고정 제약을 만족하는 작은 비교다. | SP04/SP06의 선택형 탐색 범위와 맞는다. loading/error/focus는 주입 가능한 예이며 모든 작업에 공통 체크리스트를 새로 부과하지 않는다. |
| 예시의 “수락된 판”은 모든 작은 탐색 결정에 새 승인을 요구한다. | 예시 40행은 탐색 결과를 제품 계약으로 채택하는 후속 경계다. design-depth 32행, routing skill의 기존 허가 재사용, GIT-WORKFLOW의 영향받는 결정만 확인하는 규칙을 함께 읽었다. | 새로운 제품 계약에 필요한 기존 수락과 허용된 범위 안의 설계 선택을 구별한다. 새 도구 gate·예외 승인·검증 장부를 추가하지 않는다. |
| UI 직접 관찰을 허용하면서 U1의 독립 기대·실제 경계 검증을 약화한다. | design-depth의 “중요한 AC의 검증 접근”은 base와 바이트가 같다. UI 절은 시각·행동·서버 효과와 가상화 한계를 더 구분한다. TESTING-STRATEGY와 W01의 모의 화면/실서버 Proof도 그대로 적용된다. | 문서상 회귀를 찾지 못했다. 비TDD 탐색에 인위적 RED를 요구하지 않는 것은 기존 선택형 계약이며 제품 편입의 검증 면제가 아니다. |

발견된 source 수정 요구: 없음. Bugs, Security, Policy/scope 관점에서 위 반례를 대조했으며 표현 취향이나 아직 수행하지 않은 제품 실험을 결함으로 등록하지 않았다. 이 결론은 전체 0.1.9 패키지 정합성 판정으로 확대할 수 없다.

## Commands and observed results

다음은 판정에 사용한 읽기·비교 명령이다. 각 호출은 exit 0이었다. 큰 `cat` 묶음의 도구 출력이 잘린 경우 해당 계약을 작은 범위로 다시 읽었다. 명령 종료 코드만으로 문서를 읽었다고 간주하지 않았고 위 목록에 실제 확인 범위를 남겼다.

```text
pwd
git status --short
git rev-parse HEAD
git diff bcb501f16cbf8a6b00598442d2bcada00817178e -- tdd-optional/project/examples/skills/design-spec/references/design-depth.md tdd-optional/project/examples/skills/plan/examples/disposable-ui-exploration.md
git diff --numstat bcb501f16cbf8a6b00598442d2bcada00817178e -- tdd-optional/project/examples/skills/design-spec/references/design-depth.md tdd-optional/project/examples/skills/plan/examples/disposable-ui-exploration.md
git diff --check -- tdd-optional/project/examples/skills/design-spec/references/design-depth.md tdd-optional/project/examples/skills/plan/examples/disposable-ui-exploration.md
rg -n 'V3-03|V3-09|V8-02' docs/verification/north-star-playbook.html
nl -ba tdd-optional/project/examples/skills/plan/examples/disposable-ui-exploration.md
nl -ba tdd-optional/project/examples/skills/design-spec/references/design-depth.md | sed -n '17,46p'
```

`git diff --check`의 출력은 비어 있었다. 이는 공백 검사이며 의미·실행 검증이 아니다. U1 인접 절은 다음 읽기 전용 명령으로 base와 비교했다.

```sh
python3 -c 'from pathlib import Path; import hashlib,subprocess; p="tdd-optional/project/examples/skills/design-spec/references/design-depth.md"; base=subprocess.check_output(["git","show","bcb501f16cbf8a6b00598442d2bcada00817178e:"+p]).decode(); current=Path(p).read_text(); head="## 중요한 AC의 검증 접근"; tail="## 설명과 계약을 잇는 형태"; extract=lambda s:s.split(head,1)[1].split(tail,1)[0]; old,new=extract(base),extract(current); print("U1 verification block unchanged:", old==new); print("U1 block SHA-256:",hashlib.sha256(new.encode()).hexdigest()); assert old==new'
```

```text
U1 verification block unchanged: True
U1 block SHA-256: 25e33bd93708229cb9cbc23058ee37d88aa89ee777d0bd41a356c95df09a322c
```

## Input hashes

`shasum -a 256`으로 읽은 파일 판을 고정했다. 해시는 내용 검토를 대신하지 않는다. Git 경로는 저장소 루트 기준이다.

```text
ca5a6758b93491b6407eb5a7d6da6bc6ccc1819897653e4cbe767d42a1c08f0b  CLAUDE.md
56c380d188c3eeff0b6c30951d831159fc32db27f781680caa13200235cd9106  intent/0028-openwebagent-history-feedback/intent.md
ff36f8b563e39326cc161fee680b7bbdeb728eb8659cf0943618229209ab0905  intent/0028-openwebagent-history-feedback/spec.md
16e20b67481a60eca32061c69bae8a34b4ca166db6267f8c4d684712ae46ac4a  intent/0028-openwebagent-history-feedback/plan.md
e83feccdbe520f42db4d3d366f91e18b00898145a6256421993e515ee865830e  tdd-optional/project/examples/skills/design-spec/references/design-depth.md
0139f98bcc296da42d981fe0040a8e41ee2b2fa3f4e3291be6f3cb8e134c88a3  tdd-optional/project/examples/skills/plan/examples/disposable-ui-exploration.md
99d498d2edcb37f0b66046640ba0a8f4fdbbb16e44102c935bf68c9b4e741965  tdd-optional/project/examples/skills/design-spec/SKILL.md
08a5e02ffdfc14bfa72b306a256e66fb82ef18012b3f7448d0ff649d49f5abeb  tdd-optional/project/examples/skills/plan/SKILL.md
e11f73355e5b2ec329f6d485487341ebc6d15aa7a54c4d4a5a7ef4f17329ca50  docs/verification/north-star-playbook.html
da97242c7f7140b8c1090c67b0fe5f0ba43eb58063210d82280c27e067044ff8  docs/RELEASE-CONTROL.md
da97242c7f7140b8c1090c67b0fe5f0ba43eb58063210d82280c27e067044ff8  tdd-optional/project/docs/RELEASE-CONTROL.md
c2243207740bb1b59bbcf7332af9daf5a0470b08d10ae19e8dfb2af5c2cb9246  tdd-optional/project/docs/TESTING-STRATEGY.md
82831f2d6c03e148a372f917ee74172e2cf5abf53f11b4398945ae4d4b40d93c  tdd-optional/project/docs/GIT-WORKFLOW.md
7587cae2849954087a28da9d5258373416e27075041d06d7c5ee1bca1180f2a2  tdd-optional/project/REVIEW.md
bfd4554f2f753bca5374d732f4733fe48cd3f4a97d94a491d7cda1dc88aae696  REVIEW.md
97ef9153885472dae3e564f5914172e1a70c156db33f184f7ced97e1e0ef31ac  tdd-optional/project/PROJECT-POLICY.md
45ac0109cc14ccdf27aba75e3b65eb970758f4f66363f7c8b131076a1db90000  tdd-optional/project/docs/sdlc-authoring/examples/W01/context.md
c64fe0a9cae76f0ed991278f48042cce4c69f378781fe8e515d0c388d2966557  tdd-optional/project/docs/sdlc-authoring/examples/W01/intent.md
79a3eb21a7669c982c9072308e552733967561b9fbd2e43a394a600c398d49e5  tdd-optional/project/docs/sdlc-authoring/examples/W01/spec.md
db169a401d24e89476c4294dddc96843af926254f5e1a12654a1ee4bb51ef4b8  tdd-optional/project/docs/sdlc-authoring/examples/W01/plan.md
de01e577a0cdaacda538c0197adff6e11eaaec32561011f13717911ac3a1b395  .claude/agents/verifier.md
```

## Unexecuted and limits

maker `make check`, package/adapter/strict 검사와 전체 회귀는 요청된 U6에서 실행할 범위라 이번에 반복하지 않았다. `.claude/agents/verifier.md`의 전체 체인 완료 절차를 수행했다고 주장하지 않는다. 이 리뷰는 T07의 문서 단위 검토다.

브라우저, 실제 component 렌더, 사용자 시각 피드백, 제품 UI 통합, 전후 비교 실험을 실행하지 않았다. 지침의 자연 선택이나 작성자의 실제 오독 감소는 확인하지 못했다. 제품 실험 AC04는 계속 미입증이며 새 완료 gate를 추가할 이유로 사용하지 않는다. 현재 두 source와 인접 계약에서 중요한 충돌이 발견되지 않았다는 결과만 root에게 넘긴다.
