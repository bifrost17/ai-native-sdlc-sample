# 정책·검토·배포 초안
설계 후보. 이 문서의 명령은 실행하지 않았으며 활성 파일·영구 설치·플러그인 판은 그대로다.

## 채택할 짧은 기본 정책 문장
> 새 동작과 변경 동작은 시험을 먼저 작성하고 예상한 이유의 실패를 실행으로 확인한 뒤 구현한다.
> 최소 구현·재검증 후 필요한 리팩터링과 회귀 검증을 수행한다. 이미 만족한 동작과 순수 리팩터링에는
> 실패를 억지로 만들지 않는다. 팀의 관련 개발 스킬 사용을 권장한다. 의미 있는 예외와 이탈은 엔지니어와
> 정하고 근거를 기존 실행/PR 기록에 남긴다.

스킬이 없는 환경에도 이 최소 규칙이 남는다. 특정 외부 스킬 이름은 필수 정책에 넣지 않는다.
[TDD](skills/tdd/SKILL.md)는 설치 가능한 자체 기본 예시이며 이 의무의 공통 실행 방법이다.
북극성 L9는 결함의 test-first/재현 선행 커밋을 명시한다. 모든 새/변경 동작에 대한 TDD 의무는
이번 팀의 선택이다. 테스트 결과를 예쁘게 만들기 위한 약화 금지와 정당한 요구/시험 정정은 구별한다.

## 기존 피드백/검토 기준에 넣을 문장
> 변경된 계약·중요 설계가 spec.md 및 선언된 설계 정본에, 파일·순서·PR·검증 변경이 plan에 반영됐는가.
> 영향 문서와 구현이 함께 기록됐는가. 새/변경 동작의 선행 시험은 예상한 이유로 실패했으며 그 기대를
> 유지해 통과했는가. 이미 GREEN인 회귀/정당한 시험 수정/단계가 끝난 공개 제어 시험의 변경을 구별했는가.
> 최신 통합 결과와 전체 공개 단위를 확인했는가. 예정 검사와 실제 결과를 섞지 않았는가.

기존 sdlc-feedback와 sdlc-verifier의 해당 기준을 수정하는 안이며 새 CLI·hook·의미 검사기를 만들지 않는다.
중요한 설계/시험 판단에는 난도·영향·불확실성에 맞는 높은 모델/추론을 배정한다. 매 cycle 독립 리뷰·사람 승인 없음.

## 활성화 시 파일 전달표
| 이 후보의 정본 | 활성화할 위치·처리 |
|---|---|
| templates/spec.md, plan.md | 루트 templates의 대응 파일 |
| skills/design-spec, skills/plan | 기존 .claude/skills의 같은 작성 스킬을 보강 |
| guidance와 examples | docs/sdlc-authoring/guidance와 examples로 보존하고 작성 스킬의 상대 링크를 그 설치 위치에 맞게 조정 |
| skills/tdd | org-skills/skills/tdd에 전체 폴더 포함, PROVENANCE 및 배포 README 항목 추가 |
| 위 정책/검토 문장 | CLAUDE.md·사용 템플릿 기본 정책 및 기존 feedback/verifier 기준의 관련 부분만 갱신 |

후보는 검토용 상대 링크를 사용한다. 작성 스킬 두 폴더만 복사하면 외부 예시/양식 링크가 깨진다.
활성화 작업에서 위 자료를 함께 배치하고 링크를 실제 배치에 맞춰 고친 뒤 검사해야 한다.
TDD 단일 폴더는 독립적으로 복사 가능하며 외부 파일/특정 CLI를 필수 실행 의존성으로 참조하지 않는다.
어떤 스킬도 무조건 사용 템플릿 안에 설치하지 않는다. 팀은 기본 예시를 채택하거나 동등한 자체 방법을 쓸 수 있다.

## 자체 TDD 설치 안내 초안
소스는 이 패키지의 skills/tdd/SKILL.md다. 채택 프로젝트의 .claude/skills/tdd/에 같은 파일을
배치하면 프로젝트 스킬이 된다. 또는 활성화 시 org-skills에 포함해 기존 사용자 플러그인 배포를 쓴다.
현재 연구 폴더에 둔 것만으로 Claude Code에 설치/로드됐다고 쓰지 않는다.

활성화 PR에서 기존 org-skills 플러그인 판과 marketplace 판을 함께 갱신하고 다음 기존 절차를 수행한다:
```bash
claude plugin validate --strict ./org-skills
claude plugin marketplace update intent-sdlc-skills
claude plugin update intent-sdlc-skills@intent-sdlc-skills --scope user
claude plugin list --json
```
최초 설치는 기존 org-skills/README.md의 marketplace add/install 경로를 따른다. 갱신 후 새 세션에서
실제 로드 경로·판을 확인하고 자연 요청에서 적용되는지 검증한다. 후보 검증에는 이 설치를 수행하지 않는다.
그 다음 사용 템플릿/파생 실험 브랜치에서 실제 대화·구현·TDD·문서 동기화·회귀를 평가한다.
통과 전 북극성 주석의 행동 평가 등급을 올리지 않는다.
