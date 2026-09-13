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

P0/P1 완료(아래 호출 전달 조건 보정), P2 전체 실행과 HUMAN 보완을 보존하고 P3 부분 재실험을 준비한다.
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
