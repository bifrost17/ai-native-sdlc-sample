# ai-native-sdlc-sample

Anthropic의 AI-Native SDLC Playbook을 바탕으로 우리 팀이 사용할 **템플릿·스킬·정책**을 만든다.
사람이 참여하는 실제 개발에서 중요한 요구·설계·계획과 검증이 연결되는 것이 목표다. 모든 실수를
제거하기 위해 절차나 검사기를 계속 늘리지는 않는다. 우리 팀은 사내 동료에게 소프트웨어를 제공하며,
정책은 실제 영향과 대응 가능성에 맞게 얇게 유지한다. Unofficial; not an Anthropic project.

## 사용할 템플릿 선택

| 배포판 | 개발 방식 | 채택·설치 안내 |
|---|---|---|
| **TDD 기본형** | 새·변경 동작은 test-first 기본. 의미 있는 RED→GREEN과 기존 예외를 유지한다. | [tdd-first](tdd-first/README.md) |
| **TDD 선택형** | 작업별로 TDD·동작별 구현 후 테스트·기존 테스트 활용·혼합을 선택한다. | [tdd-optional](tdd-optional/README.md) |

두 판은 intent→spec→plan, 영향 문서 갱신, 회귀 보호, 독립 검토와 사람의 의사결정 구조를 공유한다.
선택형에서 TDD를 고르지 않았다는 이유만으로 예외 승인을 요구하지 않는다. 테스트를 약화하거나
실행하지 않은 검증을 통과로 보고해도 된다는 뜻은 아니다.

선택형의 구체적인 판단은 [검증 방식 가이드](tdd-optional/project/docs/TESTING-STRATEGY.md)에 있다.
[선택형 SDLC 설계](docs/decisions/tdd-optional-sdlc.md)는 조사에서 채택한 근거, 플레이북에서 유지·조정한 부분,
UI 탐색과 제품 완료의 경계 및 문서별 책임을 설명한다.

선택한 판의 **`project/` 내용만 새 제품 저장소의 루트에 복사**한다. 팀 스킬은 그 판의 `org-skills/`에서
별도 선택 설치한다. 기존 사용 후보 `84a77b3`를 기본형의 출발점으로 삼았으며, 제품에는 제작용 훅이나
활성 작성 스킬을 자동 설치하지 않는다. 채택한 제품의 루트에서 작업하고, 제작 저장소의 하위 폴더를
독립 제품 세션과 같다고 가정하지 않는다. 두 판의 팀 패키지를 같은 제품에 중복 적용하지 않는다.

```text
tdd-first/       project/ + org-skills/    기존 TDD 기본형
tdd-optional/    project/ + org-skills/    TDD 선택형
docs/           연구·결정·실험·플레이북 평가
intent/         템플릿 자체의 제작 이력
tests/, evals/  배포판과 제작 도구 검증
```

문서 양식과 작성 예시는 각 `project/`가 정본이다. 루트 `.claude/skills/`의 작성 도구는 대상 판으로
연결하는 제작용 안내이며 별도의 제품 양식을 갖지 않는다. 공통 내용의 작은 중복은 허용하되 두 판을
공통 폴더·symlink·생성기에 실행 의존시키지 않는다. [구조 결정과 이행 범위](docs/decisions/template-variants.md)

## 북극성과 근거

북극성은 **[AI-Native SDLC Playbook과 문단별 주석](docs/verification/north-star-playbook.html)**이다.
원문은 설계·판단의 기준이며 주석은 당시 템플릿·스킬·실행이 얼마나 충실히 따랐는지 기록한다.
기존 주석의 경로·판정은 역사적 근거로 보존하며 새 선택형의 통과 증거로 승계하지 않는다.

- [기본형의 보존 범위](docs/verification/variants/tdd-first.md)
- [선택형의 의도한 차이와 검증](docs/verification/variants/tdd-optional.md)
- [TDD와 구현 후 테스트 조사](docs/research/tdd-vs-test-after/README.md): 연구 16건, 프로젝트 8개·PR/MR 72건,
  원문 다운로드와 반대 근거를 포함한다. 실제 TDD 사용률이나 보편적 생산성 우열을 추정한 자료는 아니다.
- [사람·스킬·훅·CI의 책임 경계](docs/BOUNDARY.md), [레슨별 연결](docs/PLAYBOOK-MAP.md)

모델과 추론 수준은 작업의 난도·영향·불확실성에 맞춘다. 중요한 판단과 반복되는 실수에는 더 역량 높은
모델·추론을 사용하되, 개별 실수마다 새 절차나 검사기를 만들지 않는다. 일반 테스트 통과, 스킬 발견,
설정 파싱과 실제 에이전트 행동은 각각 다른 근거다.

## 팀 정책과 선택 설치 스킬

`policies/`는 팀 정책의 제작 기준·예제다. 제품은 자기 `PROJECT-POLICY.md`에 실제 값과 결정자를 기록한다.
기본형 패키지는 기존 `intent-sdlc-skills` 식별자를 유지하고, 선택형은 `intent-sdlc-skills-optional`을 쓴다.
설치 명령과 현재 버전은 [기본형 패키지](tdd-first/org-skills/README.md),
[선택형 패키지](tdd-optional/org-skills/README.md)에서 확인한다. 기존 사용자 설치를 이 구조 변경만으로
갱신하거나 비활성화하지 않는다. 채택한 판·설치한 판·실제 로드한 경로를 함께 확인한다.

Claude 및 OpenCode용 검증자·설치 어댑터를 포함하며, 선택형에는
[Codex 프로젝트 설치](tdd-optional/org-skills/codex/README.md)도 제공한다. [팀 CLI](team-harness/README.md)는 기존의
선택적 실행·기록 실험 도구로 보존한다. 회사의 사람 승인과 GitHub 병합 권한은 별도의 통제다.

## 이 저장소의 개발과 검증

루트 [CLAUDE.md](CLAUDE.md)는 템플릿 제작 지침이다. 제품의 개발 명령과 정책은 복사한 `project/`에서 정한다.

```bash
make check
SDLC_EDITION=tdd-first make evals
SDLC_EDITION=tdd-optional make evals
```

`make check`는 패키지 경로·격리, 기존 훅과 제작 도구의 결정적 검사를 실행한다. 모델 평가에는
`ANTHROPIC_API_KEY`가 필요하며 없으면 종료 코드 2로 미실행을 알린다. 평가 범위와 판별 결과 위치는
[evals 안내](evals/README.md)에 있다. 이 검사만으로 모든 에이전트의 TDD 선택·실행을 증명하지 않는다.

공통 변경은 두 판의 영향을 함께 검토하고, 선택형만의 정책 변경은 기본형으로 자동 전파하지 않는다.
승인·상태·문서 의미를 판정하는 별도 자동 검사기는 두지 않는다. 결과와 미확인 범위를
[배포판 검증 기록](docs/verification/variants/README.md)에 남긴다.

## 기존 실험과 이력

[실험 안내](docs/experiments/README.md)에 HUMAN 역할·실행 방법·초기 데이터가 있다. 실제 제품 대화·코드·시험은
당시 실험 브랜치와 고정 커밋에 남긴다. 제작 자산만 개선하고 실험 제품 전체를 제작 main에 합치지 않는다.

기본형의 출발 사용판은 `codex/use-template-0026@84a77b3`, 팀 스킬 기준은 `ece15c4`의 0.1.7이다.
[0024](docs/experiments/0024-spec-plan-activation.md), [0026](docs/experiments/0026-muse-spark.md),
[0027](docs/experiments/0027-muse-larger.md), [0028](docs/experiments/0028-review-tdd.md)의 실행 성공·실패·HUMAN 복구를
보존한다. 당시 자료의 옛 경로는 해당 커밋을 기준으로 읽는다. 현재 소스는 두 최상위 폴더이며,
옛 사용 브랜치와 새 폴더를 동시에 최신 정본으로 유지하지 않는다.

별도 제품 채택의 책임 항목은 [채택 안내](docs/ADOPTING.md), 보안·규정·브랜드·UX 예제는
[정책 안내](policies/README.md), 변경 검토는 [REVIEW.md](REVIEW.md)에 있다.
