# 0024 — 구체적 spec·plan 활성화, 설치와 실제 제품 개발

활성 템플릿 반영과 팀 플러그인 **0.1.5 영구 설치**를 마쳤다. 새 제품에서 질문·문서 작성·수락·
새 구현 세션 인계·두 PR 통합·TDD·JSON 후속 변경·독립 검토·로컬 인도를 실제 수행했다.
최종 정책 후보의 부분 재시험도 통합·검증했다. **HUMAN의 최종 리뷰를 포함한 이번 관측 범위는 통과**로
판정한다. 최초 실행의 plan 커밋 분리·intent 잔류와 재시험의 참조 정정은 실패/복구로 그대로 남긴다.

목표는 [북극성](../verification/north-star-playbook.html)의 주요 흐름이 사람과 함께 대체로 작동하는 것이다.
TDD 의무는 얇은 정책, 공통 방법은 선택 설치 스킬, 작업별 첫 시험·구현·통합은 plan으로 나눴다.
spec은 구조·동작·계약과 필요한 설계 문서 집합을 선언한다. 모든 UML이나 단일 spec 파일을 강제하지 않는다.

## 활성화와 사용 기준

- 설계 입력: 후보 `2d3f2dc`와 이전 리뷰 `4774086`. 과거 설계·리서치·예시를 보존했다.
- 활성화 `0f0f3ce`: templates/spec·plan, 작성 스킬/reference, 다섯 구체 예시와 교육 입력,
  정책 검토·TDD·feedback·native verifier, 설치 안내·얇은 정책을 연결했다.
- 초기 사용판 `codex/use-template-0024@fbc23c04348bf9009f461c396ac23df1b3139f48`: 71파일,
  자동 로드 스킬과 제작 연구 없음. 자체 예시는 선택 설치용이다.
- 후속 사용판 `codex/use-template-0024-r2@d4d2153188743eb4f1bb30693b5c17afdaa0f999`: 같은 71파일,
  Git 정책 한 파일에서 최초 문서 작성과 구현 중 계획 개정의 커밋 범위를 명확히 했다. maker 대응 `e0657c9`.
- 데이터 [F04-release-json / v6.0.0 / seed102](datasets/v6/README.md)는 기존 Python CLI와 네 합성 행이다.
  첫 공개 카드에는 JSON 요구와 질문 대본·정답이 없다. 원본 v1 코드/시험과 v2 fixture는 수정하지 않았다.

[활성화 독립 리뷰](../research/sdlc-documentation/spec-plan-activation/activation-review.md)와
[단계 1 verifier](../research/sdlc-documentation/spec-plan-activation/stage1-verifier.md)는 링크·정본·사용판 대응,
원래 작은 예시 보존과 기존 회귀를 확인했다. 다문서/UI 예시의 검토를 실제 복잡한 제품 구현으로 세지 않는다.

## 실제 설치와 노출 환경

Claude Code **2.1.265**, user 플러그인 `intent-sdlc-skills@intent-sdlc-skills`를 0.1.4→0.1.5로 갱신했다.
validate/update/list와 source/cache 주요 파일 해시 일치, 별도 새 정상 세션의 manifest·본문 읽기를 확인했다.
실제 init의 로드 경로는 `/Users/jake/Projects/ai-native-sdlc-sample/org-skills`다. 설치 캐시만으로 독립 실행됐다는
뜻은 아니다. `--plugin-dir`·safe-mode를 사용하지 않았다. 플러그인 본문과 0.1.5 판은 실험 내내 고정했다.

작성 스킬 capture-intent/design-spec/plan은 HUMAN이 자체 예시를 명시적으로 선택해 제품 `.claude/skills`에
설치했다. 깨끗한 사용판에는 자동 로드하지 않는다. 다른 영구 플러그인 두 개는 실험 세션에서만 끄고 MCP·
브라우저도 껐다. 개인 스킬 목록은 함께 보였으며 OS 보안 격리는 없었다. 경로 분리·얕은 복제를 보안 차단으로
과장하지 않는다. 실제 읽은 제작 경로는 설치 스킬/출처 확인 범위이며 제작 연구·비공개 human.json/oracle은
개발 clone에 넣지 않았다.

일반 개발 Sonnet/medium, 중요한 개정·리뷰 Sonnet/high, 반복된 계획 판단 정정과 부분 재시험 Opus/high를
사용했다. 실제 모델은 `claude-sonnet-5`와 `claude-opus-5`, native 기본 검증도 Opus/high였다.
root가 HUMAN, Claude Code가 개발 AGENT이며 root는 제품 코드를 대신 구현하지 않았다.
기록 도우미는 prompt 전달·공개 stream 보존만 한다. 검토·채점·자동 후속 대화를 실행하는 새 하네스가 아니다.

## 전체 실행에서 관측한 것

| 구간 | 실제 결과 |
|---|---|
| T1–T2 질문과 intent | 명령 모양·null·없는 owner·집계 출력·공개 제어를 질문. capture-intent 호출, HUMAN이 intent@68d0d35를 읽고 수락 |
| T3–T4 설계·계획 | design-spec/plan 호출과 정책 본문 적용. 근거 없는 규모·정책 요약·출처 판 혼용, TDD 선후 모순은 HUMAN 리뷰로 정정. spec@1d03481, plan@ccb5d57 수락 |
| T5 새 구현 세션 | 작성 대화를 전달하지 않고 문서·수락 SHA·현재 코드로 PR1 구현. owner 시험 RED→필터 GREEN, OFF 제어 시험 RED→게이트 GREEN. 9시험·HUMAN 27관측 |
| T5b PR1 검토·통합 | 자연어 리뷰 요청에서 native verifier 호출, 6종 mutation. execution.md 누락은 HUMAN이 실제 근거로 보완. merge cf6bab0에서 9시험·27관측 재확인 |
| T6 최신 main의 PR2 | 텍스트 summary 첫 RED→GREEN, 이미 만족한 회귀는 처음부터 GREEN. d4e24d9, 13시험. 이 결과를 읽은 뒤에만 JSON 요구 공개 |
| T7 JSON 업무 변경 | 문서·스킬 이름을 지시하지 않았는데 spec@3c0e0c6·plan@efa6a5b와 참조를 갱신, JSON RED→GREEN, 구현 fb6e374·14시험. **plan과 구현 커밋 분리, intent의 “항상 세 줄” 잔류** |
| T8–T9 리뷰와 복구 | native 7종 mutation·실제 동작 확인, PR2 execution 누락 발견. root가 남은 intent·계획 요약·같은 커밋 미충족도 확인. T9는 명시적 정정이므로 최초 자발적 성공으로 세지 않음 |
| 최종 수락·통합·인도 | HUMAN이 정정 intent@d92ae03·spec@5e84fe1·plan@76ba4f7을 읽고 수락. merge e433115에서 14시험·50관측. 별도 로컬 공개 수락 뒤 같은 소스로 OFF→ON→OFF 12명령, 소스/데이터 hash 불변. 최종 기본 OFF |

작성 세션은 `a65dfe3f-1485-4fcb-bcbf-6ee662bdff36`, 새 구현 세션은
`bd556b7e-cc6f-4661-8c03-d688aa147622`다. 각 세션 내부는 실제 `--resume` 대화다.
T3의 광범위한 `find /`는 HUMAN이 확인한 해당 프로세스만 중단했다. T2의 불필요한 커밋 재질문,
기록자 표시를 편집 권한으로 오해한 T8 응답, 일부 시험의 tail 파이프 한계도 보존한다.
첫 RED는 재연출하지 않았다. 실제 공개 Write/Edit·실패 출력·production Edit·GREEN 순서를 root가 대조했다.
검증자의 나중 RED 재현은 실패 원인 대조이며 역사적 순서 증거로 사용하지 않는다.

## 커밋 경계 부분 재시험

| 실행 | 기준과 조건 | 관측·판정 |
|---|---|---|
| r01 | 텍스트 summary d4e24d9의 새 shallow clone, 새 Opus/high. 원 정책·플러그인 0.1.5, 업무 요구만 전달 | 정책 검토·TDD Skill을 자연 호출하고 intent/spec/plan 개정·실제 test-first·완료 전 native 검토. b4aad4c에서 16시험·HUMAN 50관측. **plan ac1674b와 구현 2e1e4ed 분리로 같은 커밋 기준 미충족**, 통합하지 않음 |
| r02 | 같은 d4e24d9에 use0024-r2 Git 정책만 적용한 fe61fe7. 새 Opus/high, r01과 같은 업무 prompt | feedback·TDD·brand·data-compliance Skill과 완료 전 native 검토를 자연 호출. **dc05fc0에 plan·구현·시험·USAGE 동시 커밋**. 실제 JSON RED→GREEN. native 발견을 자체 보완한 96c0043은 17시험. HUMAN 최종 문서 정정/수락 뒤 merge c5ea850에서 17시험·50관측, 이번 경계 통과 |

r02 native 검토는 계획 요약의 R/AC·공개 판단 P5 누락, 실패 경로의 AC/시험 공백을 찾아냈다.
개발 AGENT는 HUMAN의 추가 힌트 없이 spec@e18a807·시험과 plan@96c0043으로 보완했고,
이미 만족한 회귀 두 건은 첫 실행 GREEN으로 남겼다. 임시 사본의 mutation 세 종류는 실제 실패했다.
검토가 시작된 dc05fc0에는 execution 기록이 없었지만 부모가 b4c0863에서 먼저 보완한 상태였으므로
그 발견을 마지막 판의 미해결로 그대로 옮기지 않았다.

최종 96c0043에는 plan 진입점의 옛 spec 참조와 원 텍스트 단계의 “유일한 RED”가 남았다.
HUMAN이 실제 파일을 읽고 r02b에서 정정을 요청했다. 같은 세션 Sonnet/high가 71b67c2에 기록했다.
이는 자발적인 전체 사슬 무결성 성공이 아니다. HUMAN이 원 T06 trace·정책 seed의 출처를 확인하고
`--json`+owner·기존 오류 유지 두 가정을 수락한 대화도 보존했다. 특히 fe61fe7은 개발자가 바꾼 정책이
아니라 실행 전 HUMAN이 준비한 입력이며, 그 출처 기록을 clone에 함께 넣지 않은 것은 HUMAN의 준비 누락이다.
확인 기록을 소급하지 않았다. 최종 실행 근거의 15/17시험 표기와 끝 공백은 HUMAN이 정정했다.

최종 수락 판은 intent@7d32d1a82cf251b6d48ffa4298e32d8d77fa6f19,
spec@e18a80780c220e98293fd4cb6672872dcd457bcf, plan@71b67c2e648fa1c4deecd113b2672aa9e773b287다.
HUMAN 수락 기록 54b1d8d 후 local merge **c5ea850d1204bc9adf84741c07e673cf402f75c7**의 fresh archive에서
17시험·50관측을 확인했다. 마지막 **910e2ac29c51bc15e1f162b0d6d5adf850e7d99c**는 통합 근거만 기록하며
제품 코드/시험은 같다. 일반 OFF를 유지했고 부분 실행의 별도 일반 공개·운영 배포는 수행하지 않았다.

r01의 native 검증자는 별도 계획 커밋을 단계별 작성 절차로 해석했다. 또 제작 저장소의 untracked 연구 파일을
org-skills 변경으로 잘못 읽은 지적은 개발자가 경로를 다시 확인해 기각했다. 모델·검증자 판단도 대조 대상이다.
root/Astra가 확인한 최초 작성·후속 변경 규칙의 범위 중첩과 작은 수정은
[독립 판단](../research/sdlc-documentation/spec-plan-activation/commit-boundary-assessment.md)에 남겼다.
새 단계·검사기·필수 스킬을 추가하지 않았다. 원 사용판·첫 실패를 보존했고 동일 데이터 재시험을 독립 성공률이나
정책 문구 하나의 통계적 효과로 해석하지 않는다. 초기 60분/12턴은 필요한 부분 재시험·리뷰를 위해 90분/16턴으로
도달 전에 연장했다. 개발 대화는 **14 HUMAN 턴**, 각 CLI 실행 시간 합은 **4,595.3초(약 76.6분)**,
가격표 기준 비용 합은 **US$29.4715**다. 원 실험 시작부터 마지막 개발 응답까지 약 82분이며 기록 마감 시간과 구분한다.
설치 probe는 별도로 61.58초·US$0.3234다. 각 meta의 마지막 result만 합했고 보고된 native 비용을
별도로 더하지 않았다. 실제 구독 청구액·Codex 비용·HUMAN 작업 시간과 다르다. full 원 실행 11턴,
r01 1턴, r02 2턴이며 마지막 문서 정정은 Sonnet/high로 낮췄다.

## 전체 흐름 평가와 한계

| 범위 | 판정에 사용한 근거 |
|---|---|
| 2–4 의도·설계·계획·인계 | 실제 질문·수락 판, 구체 계약과 파일/시험/PR 계획, 새 구현 문맥, 문서 개정·누락·복구·커밋 경계 구분 |
| 5–8 지침·스킬·개발·검증 | 얇은 정책·선택 설치·실제 Skill/Read/Agent 기록, 첫 RED/GREEN·기존 회귀, native 검토와 HUMAN의 독립 대조 |
| 9–10 eval·review | 제작 make check/fixture 회귀와 실제 제품 검토. 외부 모델 semantic eval·hosted CI/PR 리뷰는 실행하지 않음 |
| 11–13 통합·인도·운영 인계 | 실제 두 local merge, 최신 main·fresh directory·공개/중단, 다음 결정과 범위 밖 기록. 조직 승인·실제 운영·장기 지표는 미관측 |
| 고정 근거 재사용 | 바뀌지 않은 원문·역할·정책 오너·metrics·hook/CI 구조는 이전 핀과 diff 대조. 179개 문단을 매번 재채점하지 않음 |

[평가 범위표](../research/sdlc-documentation/spec-plan-activation/assessment-scope.md)는 실행 중 세운 범위를 보존한다.
완료된 제품의 시험 통과와 모든 이벤트의 스킬 자동 호출은 다른 판정이다. 원 실행 T5/T6/T7은
TDD/feedback 본문 호출 없이 방법을 수행했고, T5b/T8은 HUMAN 리뷰 요청 후 native 검증자가 선택됐다.
r01은 실제 TDD Skill과 완료 전 native 검토가 관측됐다. 무관한 스킬 미선택은 실패가 아니며 매번 호출을 보장하지 않는다.

[마감 독립 verifier](../research/sdlc-documentation/spec-plan-activation/closing-review.md)는 maker@e0657c9의
최신 local main 포함 상태에서 `make check`를 확인했다. **96시험(기존 플랫폼 skip 1), hook 28/28,
eval fixture 8/8, managed-settings PASS**다. 격리된 설정 훅의 Makefile Edit bad input도 rc2로 차단했다.
최초 원 실행과 r01의 AC5 실패, r02의 같은 커밋 경계 통과, 마지막 HUMAN 문서 정정을 별도로 대조했다.
독립 검토자의 첫 검사 출력 수집 래퍼가 실패해 make check를 한 번 다시 수행한 사실도 원 보고에 남겼다.
플레이북은 기존 판정/179개 ID를 유지하고 관련 **12개 주석에 새 관측만 추가**했다. 추가 문단만 제거하면
원문과 이전 주석 전체가 e0657c9와 바이트 동일하다. 모든 챕터를 무조건 재채점하거나 새 검사기를 추가하지 않았다.

이번 제품은 단일 CLI이므로 다문서·웹 예시는 교육/정적 검토 범위다. 실제 UI·서버 인증·DB 동시성·운영 배포·
장기 안정화·release-control cleanup은 검증하지 않았다. 기존 F03의 cleanup은 역사적 근거로만 남긴다.

## 보존

제작 main에는 방법·고정 데이터·색인·판단을 두며 전체 제품·공개 대화·명령 출력은 실험 기록 branch에 보존한다.
마감 때 [보존 대조표](../research/sdlc-documentation/spec-plan-activation/preservation-audit.json)로
제작 작업 폴더의 runtime 자료 64개가 세 archive의 원본/공개 해시에 모두 대응함을 확인한 뒤 중복 사본을 제거했다.
원 제품은 `/Users/jake/Projects/ai-native-sdlc-exp-0024-f04`, 첫 부분 실행은
`/Users/jake/Projects/ai-native-sdlc-exp-0024-json-retest`, 후속은 `.../ai-native-sdlc-exp-0024-json-r2`다.
각 기록 branch의 `EXPERIMENT.md`는 기준/판정을, `raw/manifest.json`은 원본과 공개 사본 SHA-256·크기를 가진다.
원 실행 기록은 `codex/experiment-2026-09-11-f04-r01@f77217fb59c9e7761a533247f8568a807a1406d9`(49개 자료),
실패한 r01은 `codex/experiment-2026-09-11-f04-json-retest@1959913d1271273eda48c2f55359765e1d1b4d7e`(6개 자료)다.
최종 r02는 `codex/experiment-2026-09-11-f04-json-r2@0fe8aae196b669da5f5ba6037a63b17f918619ca`(13개 자료)다.
세 ref를 제작 저장소에도 로컬 fetch했으며 제품 이력을
제작 main으로 merge하지 않는다. 예: `git show codex/experiment-2026-09-11-f04-json-r2:EXPERIMENT.md`.
private thinking/signature는 수집 때 제거하고,
공개 사본의 이메일은 가린다. 비공개 HUMAN 입력과 관측 helper는 진행 중 개발 clone에 전달하지 않았다.
원 공개 trace의 이메일을 포함한 보존 사본은 저장소 밖
`/Users/jake/Projects/ai-native-sdlc-experiment-private/0024-activation/originals/`에 둔다. 숨겨진 추론은 그 사본에도 없다.
HUMAN helper는 실행 종료 뒤 기록 자료로만 복사했고, 공개 대화 전달 도우미는 maker의 기존 sanitize 함수에
의존함을 명시했다. 이는 새로운 자동 판단 하네스나 채택 템플릿의 필수 실행 도구가 아니다.
원격 push·호스티드 PR/CI·실제 운영 배포를 수행한 것으로 쓰지 않는다.

| 실행 | 제품 최종 판 / 실제 merge | 기록 ref / archive 판 | 결과 |
|---|---|---|---|
| F04 전체 | b712a2f / cf6bab0·e433115 | `codex/experiment-2026-09-11-f04-r01` / f77217f | 기능 14시험·50관측·공개/중단 12. 첫 문서/커밋 경계 실패와 HUMAN 복구 |
| JSON r01 | b4aad4c / 미통합 | `codex/experiment-2026-09-11-f04-json-retest` / 1959913 | 기능 16시험·50관측, 같은 커밋 실패 |
| JSON r02 | 910e2ac / c5ea850 | `codex/experiment-2026-09-11-f04-json-r2` / 0fe8aae | 같은 커밋 경계 통과·native 보완·HUMAN 참조 정정, 통합 17시험·50관측 |

공개 사본에서 이메일은 원 실행 27건, r01 18건, r02 18건을 가렸고 숨겨진 추론/서명 payload·
자격증명 패턴·남은 이메일은 검토 범위에서 0건이다. Git의 기존 작성자 메타데이터는 이력 보존을 위해
재작성하지 않았다. private 사본 디렉터리는 700, 파일은 600이다. 세 archive diff는 제품 최종 판 대비
`EXPERIMENT.md`/`raw/`만이며 원본·공개 해시와 JSON 파싱을 확인했다. 제작 저장소는 non-shallow 상태를 유지한다.
