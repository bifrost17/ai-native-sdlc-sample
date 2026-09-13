# 0032 — Codex Luna 실제 실행 기록

2026-09-13. 사용자가 [상세 설계](0032-codex-luna.md)의 실행을 요청했다. 이 기록은 모델 실행 전에
시작한다. 평가 대상은 선택형 팀0.1.3이며 maker d109aff의 제품·스킬 tree는 설계 기준과 같다.
개발 Luna/high, native Sol/high, HUMAN은 현재 Codex root다. 설치·smoke 후 통과 조건이 충족되면
새 제품·새 세션으로 F04 전체를 실행한다. 결과와 원래 실패를 관측대로 추가하며 사전 통과는 없다.

private: `/Users/jake/Projects/ai-native-sdlc-experiment-private/0032-codex-luna/`.
제품: `/Users/jake/Projects/ai-native-sdlc-codex-luna-20260913/`.
maker 작업 브랜치: `codex/luna-experiment-run-0032`.

실험 전 준비는 Sol/high의 설치 어댑터 작성, Sol/medium의 기존 HUMAN observer 재사용 검토와
root의 CLI·환경·순수 사용판·기록 점검으로 나눴다. 이 준비용 하위 에이전트는 Luna 제품 실험의
개발 호출이나 native 검증자로 계산하지 않는다. 실제 설정·모델·실행 사건은 아래에 별도 보존한다.

## 현재 상태

완료. P0/P1의 전달 조건 보정, P2 전체 실행에서의 실패·HUMAN 복구, P3 한 번의 부분 재실험을 보존했다.
P3의 핵심 문서 동기화·제품 회귀는 통과다. 경미한 표 참조 한 칸은 HUMAN이 보완했고 반복은 종료했다.
전역 설치 변경·원격 push·hosted PR·실제 배포는 실행 범위에 포함하지 않는다.
P2의 intent 제약/상위 문서 참조 누락으로 0.1.4에서 기존 판단 지침 두 곳을 명확히 했다.
준비·smoke 오류는 플랫폼 문제와
제품/방법론 발견으로 구분하며 상세 설계의 예산·중단 기준을 따른다.

## P0 설치와 첫 CLI 시작 보정

순수 사용판 `096542e`, 설치 seed `338ce51`을 별도 저장소와 maker refs에 보존했다. 원본59개,
설치66개 파일의 manifest/diff, 기준3시험을 확인했다. 전역 스킬은 `skills.config`에 folder가 아닌
`SKILL.md` 파일 경로를 줬을 때 실제 catalog에서 제외됐다. 메모리 미주입, 프로젝트 진입 지침과
12개 implicit 스킬의 올바른 로컬 경로를 확인했다. 명시 사용4개는 설치 인벤토리에 있으며 기본
catalog에 안 나오는 것이 해당 정책의 정상 동작이다. static validator는 pr-loop의 원래
argument-hint를 거부하지만 실제 Codex catalog는 그 스킬을 읽었다. 이를 모든 실행 호환성으로 확대하지 않는다.

첫 smoke CLI 시도는 모델 세션 생성 전에 `invalid transport in mcp_servers.node_repl`로 끝났다.
debug prompt 점검용 MCP 비활성화 override를 `--ignore-user-config` 실행에도 전달해, command/transport가
없는 설정을 만든 실험 transport 오류였다. 실제 exec는 사용자 config를 제외하므로 그 MCP override만
제거한다. 원본 stderr/metadata를 남기고 새 CLI 시작으로 재시도한다. 모델 실패나 제품 실패로 세지 않는다.

## P1 명시 호출 smoke와 실행 조건 확정

3회 CLI 시작 중 첫 회는 위 설치 transport 오류이며, 실제 모델 턴은2회다. 같은 Luna/high 세션을
resume했고 서로 다른 Sol/high native 자식2개가 검증 기준을 읽고 결과를 반환한 뒤 종료됐다.
첫 구현은 인사 함수와3시험이며 기존3시험을 포함한6시험을 root도 재확인했다. 보존 commit
`d557e85`는 HUMAN이 만들었다. 두 번째 검토가 제기한 bytes 입력 허용은 문자열 입력 계약 밖이므로
제품 결함으로 승격하거나 정책을 추가하지 않는다. 두 번째 턴의 JS 구문 오류와 자가 복구도 남긴다.

실제 spawn 도구의 인자는 message/model/reasoning_effort/fork_context/items이며 named custom-agent
선택은 없다. `.codex/agents/sdlc-verifier.toml`의 자동 역할 등록·적용은 검증되지 않았다. 관측된 조건은
**독립 native 자식에게 설치된 TOML 기준을 직접 읽게 하고 Sol/high를 명시한 방식**이다.
이를 설계의 호출 전달 방식 보정으로 수용하며, 본문 전달·fresh 검토·결과 대기의 증거와 구별한다.

**원 설계와의 차이:** 스킬 감사 preflight5–6의 named custom-agent 설정 적용 gate는 충족하지 못했다.
root는 P2 시작 전에 사용자 진행 보고와 이 기록에서 파일 직접 읽기 조건을 선택했다. P1 전체를
원 설계대로 통과한 것으로 소급하지 않는다. 변경된 실험 조건은 “새 native Sol/high 문맥 + 설치된
검증 기준 파일의 실제 읽기 + 보고 전용·대기·종료”이며, named TOML 자동 적용의 호환성 판정은
미검증으로 남긴다. 새로운 검사기나 sandbox 확대 대신 이미 관측된 전달 방법의 SDLC 사용을 평가한다.

workspace-write sandbox는 `.git/refs` 변경을 거부했다. Luna는 우회하지 않고 미커밋 결과를 제출했다.
P2에서는 설계에 둔 HUMAN Git 대행을 시작 조건으로 한 번 고지한다. root가 브랜치·stage/commit·merge를
수행하고 Luna의 자체 Git 성공으로 평가하지 않는다. sandbox나 승인 경계는 넓히지 않는다.

P2는 seed `338ce51`에서 새 복제본 `f04-r01`, 새 세션
`01a098ae-7183-77c0-8eeb-28b28275edb0`으로 시작했다. smoke 파일·대화·판정은 전달하지 않았다.
제품 요청에는 공개 문제 카드와 Git 대행 조건만 넣었으며, 스킬 이름이나 미래 D7 요구는 없었다.

## P2 최초 제출과 D7 진입

첫 턴은 업무 질문이었다. HUMAN은 실제 질문에 owner 정확 일치·완료 포함·원순서, 세 줄 집계,
`TRACKER_OWNER_INSIGHTS=1`만 ON, 그 밖의 값 OFF, 파일 보존, 공개 담당을 답했다.
Luna는 두 신규 동작에 TDD를 선택했다. 문서 뒤 목록 RED→GREEN, 요약 RED→GREEN을 공개 사건에서
확인했으며 전체8시험을 통과했다. 소스·문서·시험이 포함된373행 추가/2행 삭제의 최초 제출은
HUMAN이 `1e250f1`에 보존했다. independent text observer43명령·2추가 판정도 통과했다.

단계별 문서 SHA 수락을 기다리지 않고 문서3개를 함께 작성한 뒤 구현에 들어간 **인계 공백**은 남긴다.
HUMAN의 “이 결정으로 작업을 진행”은 한정된 draft 작업 허가로 해석할 수 있지만, 아직 없던 문서 판의
수락을 뜻하지는 않는다. spec/plan Upstream은 working tree였고 구현 전 기준3시험도 직접 실행하지
않았다. 기준 시험은 P0에서 HUMAN이 확인했고 Luna는 자기 실행 기록의 과한 표현을 스스로 정정했다.
사후 현재 판 수락을 구현 전 단계 수락으로 소급하지 않는다.

한 PR 선택은 별도로 수용했다. 공유 필터·공개 설정과 작은 제품 변경량에 비춰 합리적이며
PR 크기 정책이 여러 PR을 강제하지 않는다. 따라서 이번 r01에는 PR1 부분 통합/PR2 최신 main
재분기의 증거가 없다. 두 기능의 순차 TDD와 최종 한 PR의 로컬 통합 범위로 평가를 제한한다.

자발적 native 검토자는 새 Sol/high `01a098b7-b096-72e3-bf70-6f620abb58ae`였다. 설치 TOML 기준·
현재 문서와 미추적 파일까지 읽고8시험·직접 관측 후 중요한 발견 없음으로 반환했다. 부모는 결과를
기다린 뒤 종료했다. 검토자는 과거 RED 선후 관계를 현 파일만으로 확정하지 않았고, HUMAN이 별도
공개 순서를 대조했다. 검토자가 단계별 수락 공백까지 해결했다는 주장은 하지 않는다.

HUMAN은 제출 문서·코드·시험을 읽고 `1e250f1`을 **다음 작업의 현재 기준판**으로 수락했다.
같은 세션의 세 번째 턴에 JSON 업무 요구를 처음 전달했다. 프롬프트에는 문서명·스킬명·갱신 상기가
없다. 수락 SHA와 한 PR 수용·최종 merge/일반 공개 보류는 실제 업무 조건으로 함께 전달했다.
JSON 전 상태는 `codex/experiment-0032-r01-pre-json`에 보존했다.

## P2 JSON 결과·실패·HUMAN 복구

D7의 성공한 공개 사건은 spec 갱신14 → plan16 → 시험19 → RED21 → 구현24 → GREEN26이다.
의도한 JSON 실패를 먼저 관측했고 전체9시험, 독립 observer55명령/3추가 판정을 통과했다.
`c9e6e43`에는 spec·plan·구현·시험·USAGE를 함께 담았다. 그러나 다음 두 누락이 있었다.

- intent의 “요약은 세 줄” 제약을 JSON과 대조하지 않았다. spec/plan만 갱신했으므로 **영향받은 문서
  전체의 갱신**은 실패다. 완료 native 검토자도 이 모순을 놓쳤다.
- plan의 Upstream은 JSON이 없는 `spec.md@1e250f1`만 가리켰다. 수락 기준 SHA와 현재 JSON 확장을
  구별해 실제 사용하는 문서 내용을 연결하지 못했다.

JSON 핵심 시험은 RED부터 진행했지만 완료 후 집계 assertion은 GREEN 뒤 추가됐다. 모든 세부
assertion이 RED부터였다고 주장하지 않는다. focused6은 기존5메서드+신규JSON1메서드이며 “신규6”이 아니다.

두 번째 완료 native Sol/high 검토자는 `01a098c4-0621-7bc0-9a60-ac7800e3564e`다. 보고는03:20:37에
이미 완료됐다. 부모의 상태 메시지가 종료된 자식을 다시 시작한 뒤 close와 닫힌 ID 조회가 겹쳤다.
원래 검토 보고는 반환됐으며, 후속 중복 턴의 중단을 원래 결과 유실로 계산하지 않는다.

HUMAN이 누락을 구체적으로 지적한 call04에서는 문서·정책만 복구했다. 세 번째 native 검토는
정책 P1~P3 소개 모순을 찾았고 Luna가 고쳤다. 마지막 fresh 검토 C4는601초 호출 한도로 중단됐으며
최종 보고가 없다. 그 전에 읽기·9시험·diff 검사 및 plan 검증 ID의 정책 P1~P3 중복 우려를 남겼다.
HUMAN이 검증 ID를 PF1~PF5로 바꾸고 현재 상위 문서의 경로·절을 명시해 `3a01c9f`로 수락·보존했다.
최신 native 전체 검토가 완료됐다고 세지 않는다. 현재 수락을 최초 단계의 사전 수락으로 소급하지 않는다.

HUMAN은 한 PR 범위를 로컬 main에 merge commit으로 통합했다. 통합된 판의 **새 복제본에서도
9시험·55명령/3추가 판정**을 통과했다. 제품의 일반 공개·flag 제거는 보류했다. 이 결과는 기능과
사람을 포함한 복구 인도의 통과이며, 원래0.1.3 문서 동기화의 자연 준수 통과가 아니다.

## P3 보완판과 새 부분 실험

**소스 `f78c906507e95ff948cdc41902f15b5ae5438a4c`, 팀0.1.4.** Astra/ultra가 기존 feedback/verifier
두 판단을 명확히 하고 Sol/high가 독립 검토했다. 목표가 같아도 현재 intent 제약을 비교하고, 수락
기준 SHA와 실제 허용된 현재 상위 문서의 경로·절을 구별한다. 영향 없는 문서의 편집·새 승인 단계·
별도 계획 커밋·의미 검사기는 요구하지 않는다. 순수 제품 정책과 Luna/high·Sol/high는 그대로다.

설치 명령·전체 폴더 복사·Codex patch·TOML·얇은 AGENTS 예시를
[재사용 배포판](../../tdd-optional/org-skills/codex/README.md)에 포함했다. 전체16스킬/59원본파일 중
53파일이 byte 동일하며6개의 SKILL.md만 선언한 플랫폼 변환을 받는다. 검토 기준 전문은 source와
일치한다(진입 목록 AGENTS만 추가).0.1.4 첫 patch 적용이 offset backup `.orig`를 만든 문제는
배포 patch의 행 위치를 갱신해 해결했고, 깨끗한 적용·backup/reject 없음까지 재확인했다.
전체 maker 검사102시험(1skip), hooks28, eval fixture8, managed settings 검사도 통과했다.

최종 배포 점검에서 같은 패키지의 OpenCode verifier 사본도0.1.4 기준으로 동기화하고 patch 행 위치·
README/색인을 맞췄다. frontmatter·권한·단계 한도는 유지했으며 기준 전문 일치·깨끗한 patch 적용과
maker 전체 검사만 다시 확인했다. OpenCode 모델 재실험은 아니다. Codex에서 실험한 project/shared
skills/shared verifier/Codex adapter는 f78c906 이후 byte 동일하다. 이 후속 배포 검사는 원본 증거와
분리한 `delivery-addendum/`에 보존한다.

JSON 이전 `1e250f1`에서 새 seed `1eb7e250a22100a5d3a12862deb54de401d1d11e`를 만들었다.
seed에는 두 설치 파일(feedback와 verifier TOML)만 변경됐다. 제품·시험·기존 문서는 같다.
미래 JSON·복구·maker 정답의 Git 객체 부재, 기준8시험, 새 catalog의 로컬 implicit12개를 확인했다.
다른 세션에서 보이는 전역 `.agents/skills`도 실행 override로 제외했다. root의 첫 catalog 검사는
alias를 r2로 고정해 실패했으나 제외 후 r1으로 재번호화된 것이었고, 실제 경로로 다시 검증해 통과했다.
전역 파일을 수정하지 않았다.

새 제품 `f04-r02`, 새 Luna 세션 `01a098de-49fd-7203-a75e-8cb0b54b1da3`에 r01 D7 프롬프트를
byte 동일하게 전달했다. 문서명·스킬명·갱신 상기는 없다. 초기 문서·구현은 이전 r01의 수락 baseline을
사용하므로 **JSON 사건의 부분 재실험**이다. 최초 단계별 인계·초기 계획 선택·전체0.1.4 사슬의
통과를 이 표본으로 주장하지 않는다. 새 문맥과 소스 차이가 함께 있어 문구만의 인과 실험도 아니다.
예산은 사전 설계의3호출/25분이며 완료하면 반복을 종료한다.

## P3 결과와 종료 판정

새 CLI 호출1회,559.127초로 종료했다. 성공한 공개 사건은 **intent22 → spec24 → plan28 →
JSON 시험31 → argparse RED33 → 구현35 → 집중6시험 GREEN37**이다. USAGE도26에서 선행 갱신했다.
기존 수락 SHA는 text-summary baseline으로 명시하고, 실제 상위 문서는 현재 working tree의
intent/spec로 구별했다. plan Order/Proof의 AC9는 실제 spec AC9와 연결된다. 별도 승인 요청이나
문서 갱신 상기 없이 수행했고, 영향6파일을 **`98bb300`에 함께 커밋**했다(Git은 HUMAN 대행).

최신 native Sol/high `01a098e3-3482-73d2-8a42-bb111efcf89e`는 fresh 문맥에서 설치 기준과 현재
파일·diff·시험·직접 동작을 확인했다. 부모가72에서 보고를 받고77에서 종료한 뒤80에서 완료를
보고했다. named custom-agent 자동 적용은 여전히 미검증이다. 검토자는 과거 RED 순서를 최종
트리만으로 증명하지 않았으며 위 선후 관계는 HUMAN이 공개 사건으로 확인했다.
별도 child와 좁은 인계로 시작한 공개 문맥은 확인했지만, spawn 로그에는 `fork_context=false` 필드
자체가 직렬화되지 않아 그 인자 전달을 직접 증명하지는 않는다.

검토자는 plan 파일 추적 표의 AC9 누락3행을 찾았다. Luna는 tracker/tests 두 행을 고쳤지만 spec
행은 남겼다. 뒤 Order/Proof와 실제 spec에는 AC9가 이미 있어 핵심 계약·작업 누락은 아니다.
HUMAN이 한 칸을 `0c17376`으로 정정했다. 원본 제출의 경미한 미완료를 보존하고 “모든 발견을
자율 해결”로 세지 않는다. 이 문구 정정 때문에 새 전체 검토나 템플릿 규칙을 추가하지 않았다.

HUMAN 수락 후 로컬 통합 **`e7d9df35d485dc673b9263b195ae1171667b0a4b`**의 새 복제본에서
**9시험·55명령/3추가 판정**을 모두 통과했다. 선택한 사건의 중요 문서 갱신, 검토·대기, 전체 제품
회귀와 인도는 충분하므로 P3는 첫 실행에서 종료한다. 초기 단계별 인계·전체0.1.4 사슬, 실제
hosted PR/CI·운영 배포·장기 운영은 미검증이며 r01의 중요 실패와 북극성의 기존 부분 판정을 유지한다.

## 동적 항목 평가

| 항목 | r01 전체0.1.3 | r02 부분0.1.4 |
|---|---|---|
| 업무·설계·계획 인계 | 업무 질문/구체 문서 자연 수행. 최초 단계별 수락은 공백, HUMAN 현재 수락으로 복구 | 받은 기준판의 JSON 변경만 수락. 최초 사슬은 재평가하지 않음 |
| 영향 문서 선행·같은 커밋 | spec/plan 선행은 관측. intent와 실제 upstream 누락은 중요 자연 수행 실패 | intent/spec/plan 선행·current upstream 구별·같은98bb300: **핵심 통과** |
| 선택 검증 방식 | TDD 자연 선택, 목록/text/JSON 핵심 RED→GREEN. 일부 assertion은 GREEN 뒤 | 현재 계획의 TDD를 따름. 실제 JSON RED→GREEN |
| 스킬 | 프로젝트 지침과 feedback·정책·TDD 본문 읽기/결과 확인. 설치16개 전체 사용은 아님 | 같은 관련 본문을 사용. 관계없는 스킬 미사용은 감점하지 않음 |
| 최신 native 검토·대기 | C1/C2/C3 보고 반환. C2의 중복 재개와 C4 미완료·HUMAN 복구 보존 | 새 Sol 검토→부모 대기→반환→close. 낮은 표 참조 누락 한 칸은 HUMAN 보완 |
| GitHub Flow·공개 | 한 PR 수용, HUMAN 로컬 merge. 중간 PR 통합·재분기는 미관측 | 이전 수락판의 새 분기·HUMAN merge. 기본 OFF·개발 ON·다시 OFF 유지 |
| 전체 제품 회귀·새 복제본 | 통합판 fresh 9시험·55명령/3추가 판정 통과 | 통합판 fresh 9시험·55명령/3추가 판정 통과 |
| 사실·사람 판단 | 원래 실패·중단·사후 복구와 현재 수락을 분리 | 핵심 통과와 경미한 HUMAN 정정을 분리. 과거 실패를 소급하지 않음 |

고정 플레이북 원문·양식 설명·역할 원칙은 반복 채점하지 않았다. 첫 Codex 전환의 지침 로딩·
스킬 경로·검토 권한·실제 사건은 새 조건으로 평가했다. [이전 실험과 비교](comparisons/prior-runs-vs-0032.md).

## 보존과 실행 한계

순수 사용판, 설치 seed, smoke, 원본 제출, HUMAN 복구, 통합판을 maker의 별도 refs에 보존한다.
`codex/use-template-optional-0032`, `codex/experiment-0032-seed-r01`, `-seed-r02`, `-smoke-r01`,
`-r01-pre-json`, `-r01-json-initial`, `-r01-final`, `-r01-integrated`, `-r02-submission`, `-r02-final`,
`-r02-integrated`다. 마지막 이름들은 공통 `codex/experiment-0032` 접두사를 생략했다.

공개 프롬프트·JSONL·model/effort와 시간 metadata·native 보고·HUMAN Git/수락·observer·설치 manifest·
원본 실패·독립 감사는 별도 `codex/experiment-0032-evidence` 브랜치의 `experiment-records/0032/`에
보존한다. 숨겨진 추론과 인증 자료는 저장하지 않는다. private transport/observer는 실험 지원 도구이며
제품이나 배포 템플릿의 의미 검사기가 아니다. 모델의 검토와 HUMAN의 관측/수락을 대체하지 않는다.

원본 증거 커밋은 `7730151b80bc0d2a006975d3c73afae0a8f10e2e`이며327개 파일과 별도 manifest를 담는다.
최종 증거 `ce5d2c4a99c846f64ef0e10a0789052ca2100b4c`는 이 원본을 바꾸지 않고 배포 검사 부록만 추가했다.
로컬 [증거 안내](/Users/jake/Projects/ai-native-sdlc-experiment-records/0032-codex-luna/experiment-records/0032/README.md),
[제품11refs bundle](/Users/jake/Projects/ai-native-sdlc-experiment-bundles/0032-codex-luna-products.bundle),
[최종 증거 bundle](/Users/jake/Projects/ai-native-sdlc-experiment-bundles/0032-codex-luna-evidence-final.bundle)을 남겼고
두 bundle 검증이 통과했다. 다른 경로에서는 위 Git evidence ref와 `experiment-records/0032/`를 사용한다.

전체 CLI 시작은8회(smoke3, r01 4, r02 1)이며1회는 모델 세션 이전 설정 오류다. native 검토자는
서로 다른7세션이고6세션은 보고를 반환했다. 미완료 C4와 이미 완료한 C2의 불필요한 후속 재개를
별도 보존한다. usage는 각 CLI가 제공한 범위 그대로 남기며 실제 계정 요금이나 모델 우열로 환산하지 않는다.
전역 설치 변경·sandbox 확대·remote push·hosted PR·실제 배포 없이 로컬 실험을 종료했다.
