# 0038 — Muse Spark와 문서 갱신 커밋 확인

Status: completed — 계약 갱신·동반 커밋·동작 확인 통과, 현재 plan/인계 상태 갱신은 부분

사용자 원문: “open code cli muse spark xhigh로 실험해봐”. 0037의 중단과 별개로 새 한 사례를 실행한다.
북극성 V4-11의 변경과 plan 동시 갱신, V8-01/02의 실제 피드백·새 문맥 검토가 기준이다.
root는 HUMAN (Codex, simulated), OpenCode의 Muse Spark는 개발 에이전트다.
완벽한 제어가 아니라 중요한 변경과 문서·실제 커밋이 대체로 함께 유지되는지 관측한다.

## 입력·설치·Git 판

제작 source `a23a1ce`의 0.1.9와 선택 Git hook을 별도 저장소에 적용한다. native 팀11개·작성3개,
수동 자료2개·검증자·hook 설치 파일/해시와 adapter 적용을 기록한다. source maker와 원제품·전역
스킬은 바꾸지 않는다. template 기본 branch→fixture 시작판 main→별도 작업 branch를 보존한다.
배포판의 기본 설치 비활성은 그대로이며 **실험 제품이 hook을 명시 채택**한다.

[입력](datasets/v9/broker-replay/public.md)은 0018의 ACK/최종 완료 구분에서 구성한 작은 HTTP/SQLite
브로커다. 기존 0037 fixture의 원문 4파일을 보존해 재사용한다. 합성 프로그램이며 원제품 stack/
과거 결함을 그대로 재현한 것으로 보고하지 않는다. 현재 계약은 baseline API·시험이며 옛 ACK
문서는 역사다. 이 사례는 전체 UI·전후 쌍·장기 운영 검증을 대신하지 않는다.

OpenCode 요청 모델은 `opencode-go/muse-spark-1.3-contributor`, variant는 `xhigh`다.
실제 CLI 판·발견/읽기·관측 metadata는 실행 자료로 확인한다. 이름 목록이나 설정만으로 실제 호출을
통과로 하지 않으며 다른 모델로 몰래 바꾸지 않는다. XDG config/data/cache/state와 공개 입력을 격리하고
인증 값·숨은 추론·HUMAN의 oracle은 제품/공개 로그에 넣지 않는다.

## 대화와 관측

1. 설치·격리·작은 실제 사전 응답을 확인한다.
2. 에이전트가 현재 코드/계약에서 알림 replay의 intent·spec·plan을 작성한다. HUMAN이 실제 초안에
   피드백하고 중요한 미정을 결정한다. 필요한 작성 스킬을 지정한 사실은 자연 선택으로 세지 않는다.
3. 수락한 범위의 구현·시험·작은 로컬 인도를 요청한다. hook 채택 안내는 기존 프로젝트 지침에서
   제공하며 매 커밋 문서 수정이나 새 검토를 요구하지 않는다.
4. 첫 구현 뒤 [HUMAN 후속 조건](datasets/v9/broker-replay/human.md)의 결과 가시성 변경을 전달한다.
   첫 후속 메시지에는 문서 갱신을 따로 상기하지 않는다. 실제 요구 변경을 관련 spec/plan·구현에
   연결하는지, hook 오류가 있으면 이유를 읽고 올바르게 복구하는지 관측한다.
5. 새 세션은 앞선 대화 없이 현재 문서·코드에서 인계와 회귀를 확인한다. root는 새 checkout의
   독립 HTTP/DB 관찰·전체 시험·실제 커밋/문서 내용을 판정한다.

총 본실험 30분·parent 최대6호출·native child 최대2호출, 사전 호출1회·최대5분으로 제한한다.
사람 피드백과 복구는 초기 자발적 성과와 구분한다. 작은 표현 차이나 그림 개수로 반복하지 않는다.
미완료·인증/도구 오류·우회도 그대로 남긴다. 실제 hosted PR·push·merge·배포는 하지 않는다.

## 평가와 보존

실제 replay 순서/내구성·ACK running·역할 경계, 중요한 spec/plan 개정과 같은 커밋, 올바른 현재
인계, stage 누락 차단과 의미 있는 복구를 구별한다. 기계 시험의 차단 성공은 실제 모델의 의미 판단과
별개다. 모든 갱신이 성공해도 hook의 개별 인과 효과를 입증하지 않는다. bypass·거짓 빈 목록으로
통과할 가능성은 그대로 유지한다. 이 한 사례로 Codex·Claude 모델 행동이나 전체 AC04를 승격하지 않는다.

원본 입력·prompt/response·도구 공개 이벤트·Git refs/bundle·설치/source SHA256·독립 실행 전문은
`.local/experiments/{workspaces,private}/0038-document-sync-muse/`에 보존한다. 과거 0037을 덮지 않는다.
필요한 일반 개선만 원인에 맞게 검토하며 제품별 새 검사기·승인 단계를 추가하지 않는다.

## 결과

root는 계약 갱신·동반 커밋·실제 동작 범위를 통과로 판정한다. 최종 독립 리뷰에서 현재 plan의
인계 문구 누락을 확인해 **인계 상태 갱신은 부분**으로 정정한다. 기존 PROCESS·feedback에 현재
요약을 갱신하라는 지침이 있어 이번 누락에 새 일반 규칙이나 프로그램을 추가하지 않는다.
전체 템플릿의 무오류 동작·hook의 개별 인과 효과를 입증한 것은 아니다.

실제 CLI는 **1.18.30**, parent 두 세션과 native 검증자 두 세션의 응답 metadata에서
**opencode-go/muse-spark-1.3-contributor / xhigh**를 확인했다. 사전1회·본실험 parent4회·child2회,
본실험 CLI 실행 합계764.239초였다. child 대기 시간은 parent 시간에 포함돼 중복 합산하지 않는다.
첫 설계 호출 시작부터 새 독자의 응답까지 약19분으로 계획 예산 안에서 끝났다. 모델을 대체하지 않았다.

| 단계 | 실제 관측·판 |
|---|---|
| 설치·사전 | 명시 채택 스킬14개와 hook 안내/설치본 읽기. 초기 template `4a47cb8`, fixture/설치 main `ab3d230` |
| 초안 | `2675c7f`에 intent/spec/plan·색인 작성. 현재 ACK running을 과거 note보다 우선. 미정 Q1–Q4를 질문 |
| HUMAN 피드백 | after 기본값0·과거 순서 backfill 금지·기존분409·수락/구현 역할 확정. 합의 위반을 spec 변경으로 정당화하는 계획 문구 수정 요청 |
| 첫 인도 | `48fdbc3`에 코드·신규 시험·intent/spec/plan·색인을 함께 기록. native 검토 후 시험2곳·참조를 보완. 독립 HTTP/DB oracle PASS |
| 후속 요구 | 가시성 변경 메시지에는 문서 갱신 지시 없음. 공개 이벤트에서 **spec→plan→새 기대 RED→코드 GREEN** 관측 |
| 후속 인도 | `d302942`에 코드·시험·spec/plan을 함께 기록. intent의 문제/목표/제약은 유지. 동반 문서 목록에 spec·plan을 선언한 실제 hook 커밋 성공 |
| 현재 색인 | 별도 `78ab6d5`가 최신 인도판·HUMAN 수락 대기·남은 상태조회 가시성 결정을 연결. 완료/병합으로 오인하지 않음 |
| 새 세션 | 이전 대화 없이 현재 색인·문서·코드/Git에서 구조·전이·404→409→400·ACK running·observer 결과 제외·실제 남은 일을 설명. 직접9시험 PASS. 다만 plan의 낡은 다음 작업/원격 절차 충돌은 지적하지 못함 |
| 독립 최종 | 새 clone HEAD `78ab6d5`에서 기존2+신규7=9시험, 독립 역할/순서/cursor/상태 HTTP·SQLite oracle, diff 확인 PASS. 서로 다른 OS PID의 서버 재시작 뒤 replay와 역할별 result 표현도 동일 |

첫 구현은 신규7시험의 404 실패 후 통과를 관측했고, 후속 요구는 결과 노출의 2실패 후 통과를 관측했다.
검토자가 보강한 이미 동작하는 경계 시험은 소급 TDD로 계산하지 않았다. native 검토는 보고만 했고
실제 Git commit/동반 문서 내용·현재 실행은 root가 별도로 확인했다. 시험 명령을 pipe로 출력한 일부
도구 호출은 종료 코드를 직접 입증하지 않으므로 root의 비pipeline 최종 실행을 판별 근거로 사용했다.

자연 hook 차단·실패 후 모델 복구는 **미관측**이다. 에이전트가 정상 신호를 전달해 커밋했으므로
누락 차단 성공은 U7의 Git fixture13건 근거와 구분한다. `--no-verify`/hook 삭제 흔적은 없고 설치된
두 파일의 해시는 그대로였다. 거짓 빈 목록·형식 개정·의미 판단 오류가 가능한 한계는 남는다.

또한 `GET /requests/{id}`는 기존 계약대로 result를 반환한다. native 검증자가 이를 드러냈고
현재 spec/plan·인계에 남겼다. 이번 요구는 알림 응답 표현이며 서비스 전체 결과 기밀성/인증은
대상이 아니다. 원제품 stack·UI 심미성·다중 인스턴스 경합·원격 PR/CI/main 통합·운영을 검증하지 않았다.
제품 main `ab3d230`는 baseline으로 보존하고 실험 코드는 `codex/0038-broker-replay`에 유지했다.

## 독립 리뷰의 발견과 판정 정정

최종 제품 `78ab6d5`의 `changes/0001-notification-reconnect/plan.md:6`은 T03을 구현·시험·커밋한 뒤에도
“다음 작업은 T03 RED 관측”이라고 남았다. 같은 파일의 Order of work에는 Draft PR·main 머지 절차도
남아, 바로 아래 로컬 인도 표 및 `changes/README.md`의 최신 상태와 충돌한다. 새 독자는 색인·코드에서
실제 남은 일을 설명했지만 이 plan 문구를 발견해 보고하지 못했다. 현재 요약이 최신이라는 주장은 부족했다.

Sol/medium의 [독립 리뷰 전문](../research/openwebagent-template-history/completion/0038-review.md)을
받은 root가 원문·최종 파일을 대조해 중요한 인계 누락으로 수용했다. 앞선 통과 보고와 그 시점의 문서는
응답 원문·해시 스냅샷으로 보존하며, 이번 기록에서 계약 동기화 PASS와 인계 상태 PARTIAL을 구분한다.
계약·T03 계획·시험은 수정됐고 구현과 같은 커밋에 포함됐지만 이것이 plan 전체의 최신 상태를 보장하지 않는다.

원인 판단: 0.1.9의 `docs/PROCESS.md` 중단·인계 절과 설치된 `sdlc-feedback`은 현재 plan 요약·판·남은 일의
갱신을 이미 명시한다. 이번 사례는 충분한 지침을 따르지 않은 에이전트 누락이며 hook의 선언 경로 포함
확인이 문서 내용의 정확성을 보장하지 않는 실제 한계다. 새 상태 장부·검사기·매번 강제 개정을 추가하지 않는다.
원 제출판과 새 독자의 응답을 보존하고 모델을 추가 호출하거나 제품을 root가 고쳐 최초 성공으로 덮지 않는다.
따라서 **현재 plan/총괄 표가 항상 서로 최신으로 일치한다는 목표는 이번 사례에서 완전히 확인되지 않았다.**

## 원본과 재확인 경로

아래 자료는 `.local/experiments/private/0038-document-sync-muse/` 아래에 보존한다.
원문은 요약으로 대체하지 않으며 숨은 추론·인증 값을 제외하고 공개 response/tool 필드를 유지한다.

- `manifest.json`, `setup-commands.json`, `runtime-preflight.json`: source/설치/fixture·hook 해시, patch와 격리 확인.
- `turns/{00-preflight,01-design,02-implement,03-change,04-handoff}.*`: 원문 prompt·response·공개 도구 JSONL·stderr·시간/세션/종료 metadata.
- `exports/`, `observed-models.json`: parent/검증자 전체 공개 세션 자료와 실제 모델/variant. 초기 export는 hash별 snapshot으로도 보존.
- `first-delivery/`, `changed-delivery/`: 당시 문서 snapshot·원문 hook commit 입력·Git판과 독립 HTTP/DB 관찰.
- `final-validation/`: 새 clone 시험/HTTP/DB/프로세스 재시작·실제 커밋 파일·전체 출력.
- `product-refs.txt`, `product.bundle`, `preservation.json`: template/main/개발 branch와 설치 hook 변경 없음. Git bundle은 `.git/hooks`를 포함하지 않으므로 hook 해시는 별도 manifest에 둔다.
- `evidence-index.json`: 위 원본·실행/입력102파일의 길이·SHA-256과 최종 PASS/PARTIAL 구분. 독립 리뷰 전 보고의 스냅샷 manifest도 연결한다.

이번 결과는 0037의 중단·실패, 앞선 최초 문서 누락, 전체 AC04 전후 비교 유예를 덮어쓰지 않는다.
