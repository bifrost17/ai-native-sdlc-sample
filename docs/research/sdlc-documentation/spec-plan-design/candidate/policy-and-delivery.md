# 정책·검토·배포 초안
설계 후보. 아래 전달/설치 작업은 미실행이며 활성 파일·영구 설치·플러그인 판은 그대로다.
기존 정책 정본은 [GitHub Flow](../../../../GIT-WORKFLOW.md), [PR 크기](../../../../PR-SIZE.md),
[공개 제어](../../../../RELEASE-CONTROL.md)다. 양식과 지침은 이를 해당 개발건의 구체적인 답으로 옮긴다.

## 채택할 짧은 기본 정책 문장
> 새 동작과 변경 동작은 시험을 먼저 작성하고 예상한 이유의 실패를 실행으로 확인한 뒤 구현한다.
> 최소 구현·재검증 후 필요한 리팩터링과 회귀 검증을 수행한다. 이미 만족한 동작과 순수 리팩터링에는
> 실패를 억지로 만들지 않는다. 팀의 관련 개발 스킬 사용을 권장한다. 의미 있는 예외와 이탈은 엔지니어와
> 정하고 근거를 기존 실행/PR 기록에 남긴다.

스킬이 없는 환경에도 이 최소 규칙이 남는다. 특정 외부 스킬 이름을 필수 정책에 넣지 않는다.
[TDD](skills/tdd/SKILL.md)는 설치 가능한 자체 기본 예시이며 이 의무의 공통 실행 방법이다.
북극성 L9는 결함의 test-first/재현 선행 커밋을 명시한다. 모든 새/변경 동작 TDD 의무는 팀의 선택이다.

## 넣을 정확한 위치
| 대상 파일·절 | 적용할 변경 |
|---|---|
| maker 루트 CLAUDE.md / Conventions | 위 팀 TDD 정책 한 항목 추가. Verifying your work의 L9 verbatim 블록은 수정하지 않음 |
| 다음 사용판 PROJECT-POLICY.md / 검증과 운영 표 | “새·변경 동작의 개발 방식” 행에 같은 TDD 의무와 실행 근거 위치를 기록. 기존 명령/운영 행 유지 |
| 다음 사용판 CLAUDE.md / Conventions | PROJECT-POLICY.md의 위 행을 준수한다는 참조. 팀 정책의 중복 정본을 만들지 않음 |
| docs/ADOPTING.md / day-one 채택 안내 | TDD 정책·실제 시험 명령/근거·예외 결정자를 채우는 위치를 위 사용판 정책 행으로 연결 |
| org-skills/skills/sdlc-feedback/SKILL.md / Change or acceptance, Implementation and commit | 아래 검토 기준의 정본을 참조하며 연결된 spec 문서 집합·test-first 근거를 해당 이벤트에서 인계 |
| org-skills/agents/sdlc-verifier.md / Review criteria | 아래 검토 문장을 관련 기존 bullet에 통합. 새 검토 loop·모델 호출은 추가하지 않음 |

사용판 파일은 maker의 현재 작업 트리에 없으며 codex/use-template-0023의 두 파일에서 위치를 확인했다.
다음 사용판을 만들 때 그 새 branch의 경로에 적용한다. 과거 기준/실험 branch를 덮어쓰지 않는다.
검증 명령은 해당 제품의 실제 명령으로 채우며 maker 명령을 복사하지 않는다.

## 기존 Review criteria에 넣을 문장
> 변경된 계약·중요 설계가 spec.md 및 선언된 설계 정본에, 파일·순서·PR·검증 변경이 plan에 반영됐는가.
> 영향 문서와 구현이 함께 기록됐는가. 새/변경 동작의 선행 시험은 예상한 이유로 실패했으며 그 기대를
> 유지해 통과했는가. 이미 GREEN인 회귀/정당한 시험 수정/단계가 끝난 공개 제어 시험의 변경을 구별했는가.
> 최신 통합 결과와 전체 공개 단위를 확인했는가. 예정 검사와 실제 결과를 섞지 않았는가.

기준의 정본은 기존 sdlc-verifier.md의 Review criteria로 유지하고 feedback 스킬은 그 절을 참조한다.
중요한 판단에는 난도·영향·불확실성에 맞는 모델/추론을 배정한다. 매 cycle 독립 리뷰·사람 승인,
새 CLI·hook·문서 의미 검사기·상태 원장은 추가하지 않는다.

## 활성화 시 전달표
| 후보 정본 | 활성화할 위치·처리 |
|---|---|
| templates/spec.md, plan.md | 루트 templates의 대응 파일 교체. 정책 링크를 프로젝트 docs/로 다시 맞춤 |
| skills/design-spec/SKILL.md | 기존 .claude/skills/design-spec/SKILL.md의 새 진입점 본문으로 교체. 아래 보존 매핑 확인 |
| skills/design-spec/references/skill-provenance.md | 기존 동일 reference의 보존본. 내용 변경 없음 |
| skills/plan/SKILL.md | 기존 .claude/skills/plan/SKILL.md의 새 진입점 본문으로 교체. 아래 보존 매핑 확인 |
| guidance/design-blocks.md | .claude/skills/design-spec/references/design-depth.md의 후속 정본으로 교체·파일명 유지 |
| guidance/execution-blocks.md | .claude/skills/plan/references/execution-depth.md의 후속 정본으로 교체·파일명 유지 |
| examples/F01,B01,F03,M01 | docs/sdlc-authoring/examples/ 아래 새 기본 예시로 보존 |
| change-walkthrough.md | docs/sdlc-authoring/change-walkthrough.md |
| 예시가 읽는 cases·baseline·JSON·M01 context | docs/sdlc-authoring/inputs/ 아래 필요한 교육 입력만 보존. 아래 입력 매핑 적용 |
| skills/tdd 전체 | org-skills/skills/tdd/에 소스·PROVENANCE 포함, org-skills/README.md에 설치/적용 항목 추가 |
| candidate/README.md, 이 전달안·리뷰/인계·원문/역사 자료 | 이 연구 폴더에 계속 보존. 교육 예시 색인은 활성화 시 docs/sdlc-authoring/README.md로 간단히 작성 |

guidance를 제3의 새 규칙 위치에 병설하지 않는다. 기존 reference 경로의 정본을 위 내용으로 교체한다.
원래 references의 제약 중 이 후보가 바꾸지 않은 의미는 아래 매핑대로 보존되며 역사 판은 Git에 남는다.
후보의 상대 링크는 검토 배치용이다. 진입점·양식·reference·예시·walkthrough 내부 링크 전부를 실제 활성
배치에 맞춰 고친다. 작성 스킬 두 폴더만 단독 복사하면 링크가 깨지므로 그 방식으로 설치하지 않는다.

### 기존 작성 지침 보존/교체 매핑
| 기존 대상·내용 | 새 본문/정본에서 처리 |
|---|---|
| design-spec L3 근거·사람 수락/초안 허가·Status/Upstream | 후보 첫 부분과 끝 Review/갱신 절에 의미 유지. 원문 출처 줄 번호 유지, 사용자의 기존 허가 재질문 금지 |
| design-spec 팀 스킬 선택·spec-policy-pass 기본 예시·출처/판 | 후보 앞부분에 유지, 기존 skill-provenance.md 그대로 보존 |
| design-spec Writing 여섯 역할/중요 미정·우려 | 후보 역할 목록과 spec 양식/조건부 reference로 교체, 연결 정본을 추가 |
| plan L4 근거·단계 수락/문서 SHA·권한 | 후보 앞부분에 유지, docs/GIT-WORKFLOW.md를 정본으로 연결 |
| plan 결함 재현 선행 커밋·INTENT_TASK=fix·mutation 원본 복구 | 후보 중간에 유지. 일반 기능에 fix 모드를 켜지 않음 |
| plan 파일/순서/위험/Proof·갱신 | 후보와 plan 양식으로 교체·TDD 선행/문서 집합을 보강 |
| 기존 design-depth.md / execution-depth.md | 위 전달표대로 같은 경로의 새 정본으로 교체. 기존 공개/권한·복구·병렬 제약은 연결된 정책과 후보의 해당 블록에서 보존 |
| 기존 feature/bug/migration 예시, plan feature/bug/migration | 역사 설명/기존 참조 보존용으로 남기되 현행 작성 예시 링크는 F01/B01/M01로 교체. 해당 폴더 안내에 후속 예시 경로를 표시; 실제 계약을 사후 재작성하지 않음 |
| 기존 plan two-pr.md와 two-pr-spec.md(F02) | 독립적으로 공개 가능한 두 PR의 별도 예시로 유지. F03는 한 공개 단위라 이를 대체하지 않음 |

### 예시 입력의 전달
F01/B01/F03의 cases는 이 패키지 inputs/cases.md의 해당 제품 맥락을 보존한다. baseline 두 파일과
f01/b01-requests.json도 교육 입력으로 함께 옮긴다. M01 합성 context의 근거 파일은 현재
.claude/skills/design-spec/examples/migration/context.md@efa7339를 inputs/m01-context.md로 보존한다.
기존 예시의 입력 판 표기는 제작 자료라는 한계를 유지한다. 옮긴 예시의 입력 링크는 새 위치로 바꾼다.

F03 역사 spec/plan·과거 결과는 이 연구 폴더 inputs/에 그대로 보존하며 현행 구현 인계에서는 읽기를
요구하지 않는다. 교육 예시의 출처 표기는 연구 경로/고정 Git 판을 가리키게 바꾸고 필수 입력 링크와
구별한다. 모든 역사 데이터를 사용 템플릿으로 복제하지 않는다. 사용판에는 제품의 실제
templates·정책을 전달하고, 교육 예시/팀 스킬은 선택 가능한 별도 자료로 둔다.

## 자체 TDD 설치 안내 초안
소스는 [skills/tdd/SKILL.md](skills/tdd/SKILL.md), 출처는 [PROVENANCE](skills/tdd/PROVENANCE.md).
채택 프로젝트의 .claude/skills/tdd/에 전체 폴더를 배치하거나, 활성화 후 기존 org-skills 플러그인으로
배포한다. 이 단일 폴더는 다른 후보 파일/특정 CLI를 필수 의존성으로 참조하지 않는다.
연구 폴더에 있는 것만으로 설치/로드됐다고 쓰지 않는다.

활성화 PR에서 기존 org-skills 플러그인 판과 marketplace 판을 함께 갱신하고 기존 절차를 수행한다:
```bash
claude plugin validate --strict ./org-skills
claude plugin marketplace update intent-sdlc-skills
claude plugin update intent-sdlc-skills@intent-sdlc-skills --scope user
claude plugin list --json
```
최초 설치는 기존 [org-skills/README.md](../../../../../org-skills/README.md)의 marketplace add/install 절차다.
그 안내의 정본은 그대로 두고 TDD 항목만 추가한다. 갱신 후 새 세션에서 실제 로드 경로·판과 자연 요청
적용을 검증한다. 이번에는 설치하지 않는다. 후속 사용판/파생 실험 branch에서 실제 대화·구현·TDD·
문서 동기화·회귀를 평가하고 통과한 범위만 북극성 주석에 반영한다.
