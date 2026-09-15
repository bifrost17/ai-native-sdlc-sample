# 0024 전체 흐름 회귀 평가 범위

2026-09-11 현재의 **평가 계획**이다. 북극성 원문과 기존 주석의 판정을 바꾸거나 아직 끝나지 않은
제품 실험을 통과로 기록하지 않는다. 이번 후보는 `185dd5e..0f0f3ce`의 활성 변경이며, 현재 확인된
범위는 다음과 같다.

- 정적 활성화: 활성 양식·작성 지침·예시·팀 플러그인 0.1.5와 사용판의 대응 및 링크·형식.
- 단계 1 verifier: `make check`(96 tests, 기존 skip 1; hooks 28/28; eval fixture 8/8), plugin validate,
  diff 범위와 사용판을 독립 검토해 단계 1을 PASS로 판정했다. 이는 설치나 제품 행동의 판정이 아니다.
- 설치 probe: 새 정상 세션에 0.1.5 스킬/에이전트가 노출되고 실제 source manifest와 `tdd`,
  `sdlc-feedback`, `spec-policy-pass`, `sdlc-verifier` 본문을 읽은 사실. 파일 존재·본문 읽기와 제품에
  실제 적용한 행동은 구별하며, probe 자체에서는 제품 파일을 바꾸거나 스킬을 실행하지 않았다.
- 제품 작성 단계의 **판정 전 관측**: T2에서 `capture-intent`, T3에서 `design-spec`과
  brand/data-compliance/spec-policy-pass 본문 읽기·적용, T4에서 `plan` 호출이 남았다. T3 초안의 근거 없는
  규모·부정확한 정책 설명·provenance 혼용은 HUMAN 리뷰로 정정했다. T4 plan에는 TDD 단계 선후 모순과
  기존/new tracker 오표기가 발견되어 T4b에서 Opus/high로 정정 중이다. 제품 코드는 아직 시작하지 않았다.
  이는 스킬 호출과 사람 개입·역량 상향의 관측이지 작성 흐름 PASS나 무오류의 근거가 아니다.

근거 정본은 [intent](../../../../intent/0024-spec-plan-activation/intent.md),
[spec](../../../../intent/0024-spec-plan-activation/spec.md),
[plan](../../../../intent/0024-spec-plan-activation/plan.md),
[실험 운영 원칙](../../../experiments/README.md), [실험 설계](experiment-design.md),
[단계 1 보고](stage1-verifier.md)와 `runtime/installation.json`, `runtime/install-probe.meta.json`이다.
작성 대화는 위의 제한된 행동 관측에만 쓰며, 산출물 수락·작업 branch·RED/GREEN·통합·인도·최종 독립
검증은 진행 중이므로 전체 제품 판정 근거로 쓰지 않는다.

## 판정 방법

이번 목표는 얇은 사내 팀 정책 아래 사람이 중요한 결정을 읽고 개입하며 주요 개발 흐름이 대체로
작동하는지 확인하는 것이다. 북극성 179개 문단을 다시 모두 모델 평가하지 않는다.

- **재관측**: `CLAUDE.md`, 작성 스킬, 팀 TDD/feedback/verifier와 직접 맞닿은 행동, 그리고 그 행동의
  앞뒤 인계만 새 제품 대화·파일·시험·Git 근거로 본다.
- **고정 근거 재사용**: 원문, 역할, governance, 측정법과 변경되지 않은 경로의 기존 판정은 해당 핀과
  인용문이 그대로인지 확인하고 재사용한다. 새 관측과 모순되거나 참조 경로가 바뀌면 다시 연다.
- **미관측**: 실행 환경이 제공하지 않는 조직 승인, hosted PR/CI, 실제 배포·운영·장기 metrics는 PASS로
  세지 않는다. CLI 결과를 UI·인증·DB·운영의 근거로 넓히지 않는다.
- 기존 실패는 역사와 현재 실행 기록에 남긴다. 다만 피드백 뒤 고친 후보는 새 clone·새 세션의 관련
  경계에서 다시 관측할 수 있으며, 과거 실패만으로 새 후보의 통과를 영구 차단하지 않는다.
- 첫 행동 시험과 RED→GREEN은 이번 팀이 spec/plan에 채택한 TDD 계약을 검증하는 항목이다. 이를
  북극성 모든 팀에 직접 강제되는 보편 요구로 바꿔 쓰지 않는다.

## 챕터 2~13 범위표

| 챕터 | 이번 후보에서 재관측할 범위 | 고정 가이드·기존 근거 재사용 | 이 실행에서 미관측 또는 아직 미완료 |
|---|---|---|---|
| 2 intent.md | 자연 문제 설명 뒤 분석가 질문, HUMAN 정정, 실제 문서 판·SHA의 수락과 다음 단계 인계 | 세 유입 경로, originator 언어, commit된 intent가 증거라는 원칙과 leading/lagging 정의 | 비 Git 기여자 connector와 조직 공용 intent home 권한 |
| 3 요구·설계 | 설치된 관련 정책 스킬의 실제 선택·본문 적용, 구체 계약/AC/우려, HUMAN의 두 질문과 실제 spec 판 수락 | PO/AGENT 역할, spec 정본·출처/판 기록, 기존 정책 내용과 metrics 정의 | `design-spec`과 정책 본문 적용은 관측했으나 초안 오판을 HUMAN이 정정함. 최종 spec 적합성·수락, UI mock→Code, 별도 policy/tech lead 승인은 미완료 |
| 4 plan mode | 수락 spec에서 파일·첫 RED·최소 구현·PR/통합 증거를 잇는 plan, 앞 대화를 못 본 구현 세션, 업무 변경 시 관련 plan과 구현의 같은 commit 갱신 | 읽기 전용 계획·사람 수락·repo 정본, 기존 first-pass/rework 측정 정의 | `plan` 호출 뒤 선후 모순·기존/new 오표기를 정정 중. 제품 plan 수락, PR1/PR2 실행·변경 동기화·최종 diff 대조는 미완료 |
| 5 CLAUDE.md | 새 얇은 TDD 정책과 완료 전 검증/verifier 지시가 shallow 제품 clone의 실제 행동에 미친 영향 | 한 페이지, repo 체크인·코드처럼 review, 반복 실수만 추가하는 원칙과 기존 metrics | `/init`, 조직 code-owner 승인, 신규 구성원 장기 시간 지표 |
| 6 skill | 사용판에서 선택 설치한 `design-spec`/`plan`과 별도 팀 플러그인 0.1.5의 `spec-policy-pass`/`tdd`/`sdlc-feedback`이 관련 시점에 실제 호출·적용되는지와 서로 다른 자연 표현의 trigger | SKILL.md 구조, 권고/결정론적 hook 구분, 정책 오너/source-of-truth와 측정법 | T2~T4에서 작성 스킬 호출과 정책 본문 적용은 관측했지만 초안 오판·정정 중 plan도 남음. 제품 TDD/feedback 적용과 구현·완료 표현의 호출은 미완료 |
| 7 session·subagent | 순차 PR 경계·별도 branch/worktree, 완료/중요 변경에서 fresh-context `sdlc-verifier`가 현재 계약과 증거를 독립 검토하는지 | 독립 작업 분해, 2~3 session부터 시작, repo 설정/귀속 및 기존 생산성·재작업 metrics | 실제 병렬 Claude session, 조직 단위 동시성·생산성 일반화 |
| 8 feedback loop | 의미 있는 새 행동의 첫 RED 원인→최소 GREEN→인접/전체 회귀, 원 출력, 작업 중 loop와 끝의 verifier 역할 분리 | 단일 test target·0이 아닌 실패, test를 고쳐 통과시키지 않는 원칙, 기존 governance/metrics | 제품 RED/GREEN·최종 독립 실행은 미완료. UI screenshot loop는 이 CLI 범위 밖 |
| 9 지속적 eval | 바뀐 agent 지침과 가까운 기존 `make check`/fixture 회귀 및 제품 사례의 실제 행동 회귀만 확인 | prompt+AC 검사, incident→eval, pass-rate와 결과 보존 원칙 및 기존 고정 데이터 | 외부 모델 semantic `make evals`, 20~50 실제 업무, hosted non-interactive CI/API 예산·required gate |
| 10 PR review | 현재 spec/plan/정책과 실제 diff·시험을 verifier/HUMAN이 대조하고 중요한 발견·복구·수락을 기록하는지 | `REVIEW.md`의 버그·보안·spec/plan/설계 패스, 중요/nit/skip 정의와 metrics | hosted Claude review, `@claude` 댓글/push, branch protection과 별도 code-owner 승인 |
| 11 approval hook | 단계 1에서 바뀐 경로의 hook wiring과 의도적 bad input 결과만 회귀 확인; 제품 흐름에 새 영향이 생기면 다시 연다 | 허용/차단·이유/경로, 설정/managed settings 구분과 기존 hook·측정 근거 | 조직 승인 목록, MDM 배포, 실제 release approver와 운영 gate |
| 12 CI/CD | local-only 통합·fresh directory 인도 사실을 배포와 구분하고 최종 제품 상태만 확인 | 읽기 전용 triage, gate 뒤 PR, 환경별 자율성·DORA 정의의 기존 근거 | hosted CI/CD, sandbox/단기 토큰, MCP 배포·상태, branch protection, rollback rehearsal |
| 13 maintain | 새 제품 결과가 기존 유지보수 안내와 모순되지 않는지만 확인 | deterministic 감시, tier, intent 분류와 leading/lagging metrics의 고정 근거 | live metrics store, headless 전체 사슬, 실제 incident/Claude Tag, 장기 finding→merge·반복률 |

## 제품 관측 뒤 주석에 추가할 우선 후보

아래 8개는 활성 변경과 가장 가까운 원문 블록이다. 현재 주석의 `충실`/`부분` 판정은 그대로 두고,
제품 근거가 실제로 생긴 블록에만 새 관측과 한계를 덧붙인다. 한 실행이 모든 블록을 만족할 필요는 없다.

| ID | 북극성 원문 요건 | 후속 제품에서 필요한 근거 |
|---|---|---|
| `V4-11` | “구현이 계획에서 벗어나면 같은 commit에서 `plan.md`를 갱신하라. 둘 사이의 동기화를 강제하는 hook을 쓰는 것을 고려하라.” | JSON 업무 변경 뒤 영향 plan, 구현·시험이 같은 관련 commit에 있고 최신 수락 spec을 가리키는지. HUMAN 지적 뒤 복구와 자발적 반영을 구별 |
| `V6-04` | skill은 `SKILL.md` 하나를 담은 폴더이며 frontmatter가 언제 trigger되는지, 본문이 무엇을 할지 말한다. | 0.1.5의 실제 로드 본문과 관측된 호출 시점·행동이 description/body 역할에 맞는지 |
| `V6-05` | skill을 repo의 `.claude/skills/<name>/`에 두어 코드와 함께 배포하거나 plugin으로 조직 전체에 배포한다. | 설치판·실제 source/manifest 0.1.5, 프로젝트 작성 스킬 위치, 새 제품 세션 노출을 구별한 기록. 조직 전체 배포로 과장하지 않음 |
| `V6-06` | “관련 작업을 여러 방식으로 Claude에게 요청해 매번 skill이 로드되는지 확인하라.” | T2~T4의 작성 요청에서 관측된 Skill trace와 이후 이름을 지시하지 않은 구현·변경·완료/검토 요청의 trace. 미호출·오판·직접 호출 복구를 그대로 남김 |
| `V7-09` | verifier 예시는 앱 실행, 변경 동작과 두 인접 흐름 확인, 실행/관측/plan 불일치 보고, 수정 금지를 요구한다. | fresh-context 검증자가 현재 제품·spec/plan·전체/인접 시험을 읽고 수정 없이 findings와 미확인을 보고한 원문 |
| `V8-02` | feedback loop는 작업 전체를 관통하고, verifier는 완료 시점에 새 context로 최종 확인한다. | 개발 세션의 반복 RED/GREEN/회귀와 완료 전 별도 verifier 호출·대기·결과를 시간 순서로 구분한 trace |
| `V8-09` | 검증을 완료의 일부로 두고, 완료 보고 전에 test를 실행해 출력을 보여 준다. | 최종 통합 HEAD와 fresh-directory 인도에서 실제 명령·rc·원 출력이 완료 보고보다 앞선 기록 |
| `V10-05` | review 정책은 버그/논리, 보안, spec·plan·설계 원칙 준수 패스와 중요/nit/skip의 정의를 둔다. | verifier/HUMAN이 현재 합의·문서·diff·시험을 의미로 대조한 findings, 복구 후 재검토와 남은 한계 |

`V2-09`, `V3-09`, `V4-06`, `V4-08`, `V4-09`, `V8-07`도 전체 흐름 확인에는 필요하지만 원문·역할과
직접 가이드가 이번 활성 변경에서 바뀌지 않았다. 실제 질문·수락·계획 인계·RED/GREEN은 최종 실행 기록에
남기되, 새 사실이 기존 주석을 보강할 만큼 구체적일 때만 해당 V 블록을 추가한다.

## 최종 확인 전에는 결론 내리지 않을 것

최종 평가는 최소한 다음 원 증거를 읽은 뒤에만 쓴다.

1. use/seed/PR1/PR2/final main의 고정 SHA·tree와 shallow 경계, maker 연구·비공개 HUMAN 자료 미포함.
2. 실제 HUMAN/AGENT 대화에서 intent/spec/plan 판과 수락 SHA, 허가 재질문·초안 오판·HUMAN 정정·
   모델/effort 상향 사유를 포함한 원문. T4b의 수정 결과와 남은 plan 모순도 확인.
3. PR1의 공개 부분 상태와 PR2의 최초 요약, 그 뒤 처음 공개한 JSON 변경의 의미 있는 RED→GREEN,
   기존 동작 회귀, 요청 파일 불변과 일반 OFF/시험 ON/완성 공개·중단.
4. 변경 합의가 관련 spec/plan과 구현 commit에 연결됐는지, HUMAN이 문서 갱신을 따로 상기했는지 여부.
5. 실제 Skill/Agent 호출·Read trace와 설치판/소스 판, 호출되지 않은 이벤트 및 직접 호출한 복구의 구분.
6. 최종 통합 HEAD의 root 재실행과 fresh-context verifier 원문, fresh-directory 인도 재현.
7. local-only와 hosted PR/CI, 단일 HUMAN과 조직 승인, CLI 인도와 운영 배포를 구분한 한계표.

성공은 R4/R5의 실제 제품 결과와 사람 인계, R6의 실패 보존·독립 검증이 함께 뒷받침할 때 해당 관측
범위에 한해 말한다. 중요한 실패가 있으면 최초 실패와 복구를 모두 남기고, 지침을 작게 고친 뒤 새
clone/새 세션의 **영향받은 구현 경계**를 다시 시험한다. 표현 차이·적절한 단계 생략·무관한 스킬 미호출을
실패로 만들거나, 실패 없는 전체 실행을 이유 없이 반복하지 않는다.
