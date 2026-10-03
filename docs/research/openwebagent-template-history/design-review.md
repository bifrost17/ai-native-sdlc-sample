# 0028 통합 설계 후보 검토

검토 시각: **2026-10-03 01:50:48 KST** (`2026-10-02T16:50:48Z`).
읽은 HEAD: `cf2ccb7ea4842dd6dcc7be8860c3939909049545`와 아래 파일들의 당시 미커밋 내용.
이 기록은 발견 보고서다. 설계 수락·제품 실행 성공·전체 작업 완료를 판정하지 않는다.

검토자는 이 세션에서 방법론/기록 설계 조사 문서를 작성했으나 검토 대상 제품 source는 편집하지 않았다.
작성자와 source 수정 역할은 분리됐지만 완전히 새 문맥의 독립 검토는 아니다. root 지시대로 제품 수정과 추가 에이전트 호출 없이 읽기·발견 보고만 수행했다.

## 발견

### DR01 · P2 · 새 SP06의 구현·검증 범위를 현재 plan에 연결해야 한다

[spec.md의 SP06](../../../intent/0028-openwebagent-history-feedback/spec.md)은 실제 UI/앱 셸 탐색, 설계의 검증 접근, 첫 실제 통합 경로를 선택했고 제품 source 네 파일에도 이미 변화가 있다. 그러나 읽은 [plan.md](../../../intent/0028-openwebagent-history-feedback/plan.md)의 T03은 후보 조사/승격, T03a는 SP04 원전 조사, T03b는 SP05 기록 설계까지만 설명한다. SP06을 어느 작업으로 구현하며 어떤 파일에 어떤 판단을 보태고 무엇으로 확인할지 아직 연결되지 않았다.

이는 모든 문장에 ID를 붙이라는 지적이 아니다. 다음 담당자가 새 설계의 실제 변경 범위와 구현·문서 검토를 어디서 이어갈지 판단할 현재 작업 연결이 빠졌다는 인계 문제다. source 문구가 생긴 사실이나 마지막 `make check`만으로 새 문서 의미와 적용 효과를 확인했다고 볼 수 없다.

**보완 방향:** 기존 T03을 구체화하거나 필요한 작은 작업을 더해 SP06과 `templates/spec.md`, `design-spec/references/design-depth.md`, `plan/references/execution-depth.md`, `plan/examples/disposable-ui-exploration.md`를 연결한다. 중요한 AC의 검증 접근→plan의 실행 절차, UI 탐색의 관측/제품 편입 경계, 조기 연결을 미룰 때의 대안을 어떤 문서/실험으로 확인할지 적는다. 파일별 거대 표나 새 승인 단계는 필요 없다. 기존 5개 WIP의 구현계획 구체성 변경은 이번 신규 설계 구현과 구분한다.

상태: 검토 시점 미해결. root에 전달했다. 후속 판이 고쳐졌다면 해당 판을 다시 읽고 이 기록에 재확인 근거를 덧붙여야 한다.

## 질문별 검토 결과

| 검토 질문 | 실제 읽은 내용과 판단 |
|---|---|
| 설계 검증 접근이 모든 테스트 본문 선작성을 강제하는가 | `templates/spec.md:24–26`은 중요한 AC의 독립 기대·실제 경계·입력/환경·실패/관측·가상화 한계를 요구하면서 기존 시험/설계 절 참조를 허용한다. plan이 명령/절차로 구체화하고 작은 변경에 별도 표/모든 테스트 본문은 필요 없다고 명시한다. 강제 TDD나 테스트 본문 선작성으로 읽히지 않는다. |
| 실제 컴포넌트/앱 셸 탐색과 제품 완료를 혼동하는가 | `design-depth.md` 새 절은 질문에 닿는 최소 구현과 자료 판·실행 위치·상태/가상 연결·남은 검증을 다룬다. `design-spec/SKILL.md:58–61`은 채택 시 요구/AC/설계 갱신과 제품 완료 구분을 유지한다. 탐색 예시 `:32–40,47–48`도 실제 편입·제품 검증을 별도로 둔다. 초기 코드 재사용은 허용하지만 제품 완료를 자동 승계하지 않는다. |
| 정적 prototype 예시가 실제 UI 탐색과 모순되는가 | 예시 `:11–18`은 이 예시의 독립 HTML 범위를 유지하면서 실제 앱의 키·겹침·초점·상태 결합 질문은 앱 셸/컴포넌트 진입점이 적합하다고 설명한다. 기존 예시의 키보드 관찰은 그 prototype 안에서의 관찰이며 실제 제품 동작 증거로 승격하지 않는다. 이 예시 자체가 실제 앱 실행 기록은 아니다. |
| 조기 수직 경로가 모든 선행 인프라·미래 인터페이스 확정을 강제하는가 | `execution-depth.md:36–42`는 이번 인도 경계와 위험한 실제 연결을 먼저 보되, 필요한 인프라로 늦어질 때 가상 경계·연결 작업/시점·남은 위험을 남기는 대안을 제공한다. health check와 사용자 흐름 완료를 구분하고 미래 인터페이스 선확정을 명시적으로 배제한다. |
| 과거 spec 참조를 금지하는가 | `changes/README.md`의 후속 개발 절, `design-spec/SKILL.md:15–18`은 과거 수락/번호만으로 자동 승계하지 말라는 규칙이다. 현재 코드·설정·정책·적용할 수락 계약을 대조하고 보존/대체 범위를 적도록 하므로 유효한 과거 계약의 재사용을 허용한다. 현재 코드가 곧 규범이라는 규칙도 추가하지 않았다. |
| 총괄 index가 독립 상태/승인 장부가 되는가 | `changes/README.md`는 plan 링크·대상 코드판·PR 링크·남은 범위를 찾는 색인으로 정의하고, 상세 시험/과거 결정을 복제하지 않으며 상태 목록도 강제하지 않는다. PROCESS의 기존 plan 현재 요약과 Git/실행 기록 대조를 유지한다. 일부 PR merge와 전체 완료를 구분한다. |
| 새 경로가 기존 채택/역사를 자동 이동시키는가 | changes README와 세 작성 스킬은 기존 `intent/` 채택 경로를 유지할 수 있음을 명시한다. 번호도 최소 네 자리와 기존 번호 보존이다. maker 이력의 이동은 이번 source 변경에 포함하지 않는다. 실제 설치·업그레이드 경로 보존은 문서 검토만으로 검증되지 않는다. |
| PR/커밋 정책이 증거 복제·승인·강제 검사를 추가하는가 | 새 `CHANGE-DELIVERY.md:11–21,30–46`은 scope/base·영향 설계·실제 대상판·미실행/실패·가상 환경 한계와 남은 범위를 연결한다. 원문은 기존 실행 기록에 두며 작은 오탈자·자동 merge/revert 예외가 있고 commitlint/hook/자동 배포를 추가하지 않는다. 기본 PR 양식은 네 역할에 해당한다. 검사 통과/PR 생성은 수락이 아니다. |

DR01 외에 위 범위의 설계 의미를 바꿔야 할 구체적인 결함은 발견하지 못했다. 이는 모든 문서·adapter·CLI 실행을 확인했다는 뜻이 아니다. 기존 설명의 실제 적용성과 효과는 예정된 개발 재실험에서 확인해야 한다.

## 기존 WIP와 이번 후보의 구분

[baseline.md](baseline.md)의 `candidate-wip/`와 현재 파일을 직접 비교했다. 기존 5개 파일은 `CLAUDE.md`, `PROJECT-POLICY.md`, `REVIEW.md`, `docs/PROCESS.md`, `templates/plan.md`다.
그 안의 구현계획 구체성 문구는 시작 WIP에 이미 있었다. 현재 `PROJECT-POLICY.md`, `REVIEW.md`, `templates/plan.md`는 이 비교에서 시작 WIP와 같았다. `CLAUDE.md`와 `PROCESS.md`에는 이번 changes 경로/총괄/과거 계약 관련 추가 차이가 있다. 기존 WIP를 새 SP06 성과로 세지 않았다.

읽은 범위는 root spec/plan, changes README, 세 작성 스킬, spec 양식, design-depth/execution-depth, disposable UI 예시, 새 PR/commit 정책·양식과 그 Git 정책 연결이다. 관련 PROCESS/CLAUDE/REVIEW/README diff도 대조했다. 북극성의 정본 하나·spec/plan 갱신·PR 기록 원칙과 앞선 연구에서 확보한 공식 근거를 사용했다.

## 검토 대상 판 고정

아래 12개 파일의 `경로 + NUL + SHA-256 + LF`를 경로순으로 연결한 집계 SHA-256은
`537c71964cdc33700deace06a131a524922cf7dc3e402b350305244890ce63d5`다. 이 해시는 검토 대상 식별용이며 설계 충분성의 자동 판정이 아니다. 이후 파일이 달라졌다면 이 결론을 새 판 전체에 자동 적용하지 않는다.

| 경로 | SHA-256 |
|---|---|
| `intent/0028-openwebagent-history-feedback/spec.md` | `f8e29afc91534de408f96258cbafdb3f63725c02579f62192f444c9708f7d8dc` |
| `intent/0028-openwebagent-history-feedback/plan.md` | `50728b291081d0c9ff0ad15c660318c69243df9659c2449017aab04e16d32df0` |
| `tdd-optional/project/changes/README.md` | `ec1e937cc24f818c0859cc952b842e4fc72d681ec30b4611bd68419fb2a5afd9` |
| `tdd-optional/project/templates/spec.md` | `38f5892daa17e7c184bf8be1c98e68cf5c36ca5448548251691c6382087fe7c2` |
| `tdd-optional/project/examples/skills/capture-intent/SKILL.md` | `71d45b46e920c42b59ca413e40d48775a511ee8e3f082244fcf94aa8a0d8bf49` |
| `tdd-optional/project/examples/skills/design-spec/SKILL.md` | `99d498d2edcb37f0b66046640ba0a8f4fdbbb16e44102c935bf68c9b4e741965` |
| `tdd-optional/project/examples/skills/plan/SKILL.md` | `08a5e02ffdfc14bfa72b306a256e66fb82ef18012b3f7448d0ff649d49f5abeb` |
| `tdd-optional/project/examples/skills/design-spec/references/design-depth.md` | `97195339c312c35eb1d8665b9e7b445a634c5d1a8628aec9009cf2666d0af94a` |
| `tdd-optional/project/examples/skills/plan/references/execution-depth.md` | `f9d51123d790963d74b8e6d0ef4de4326eaee3b78f8878b7708b6ed814917c45` |
| `tdd-optional/project/examples/skills/plan/examples/disposable-ui-exploration.md` | `13683b7a8f05827f427447c2f2358edeb23d7e79c6d3c9ca5b8d7822fd8d4e02` |
| `tdd-optional/project/docs/CHANGE-DELIVERY.md` | `274c1d8766e79c49b563172059baa356ae34ac199828d4aaafffe36dc01372a3` |
| `tdd-optional/project/.github/pull_request_template.md` | `01e54f5f921293e680f3773e669691b2f132e08f8d9bb9134a9eddf3dc19fe98` |

## 실행하지 않은 확인

제품·전역 설치·배포 adapter를 변경하거나 실행하지 않았다. `make check`, GitHub에서 PR 양식의 실제 노출, CLI의 본문 작성, 기존 채택 저장소의 업그레이드, 실제 브라우저/서비스 통합·전후 개발 재실험은 이 검토에서 실행하지 않았다. PR 양식이 존재하는 사실은 이런 실행의 대체 증거가 아니다.
