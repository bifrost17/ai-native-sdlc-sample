# 0038 — 실행 보고와 보존 근거의 독립 대조

Status: review complete — 보고서의 중요한 인계 한계 1건

2026-10-03 Asia/Seoul. 검토자는 완료된 Muse 실험을 다시 실행하지 않았다. 공개 prompt/response,
공개 도구 이벤트, 모델 응답 metadata, 실제 Git 내용과 보존된 시험·HTTP/DB·재시작 출력을 읽었다.
이 문서만 작성하며 제품·maker source·다른 작업자의 변경은 수정하지 않는다. 수락·통합 권한은 root와
사용자에게 있다. SDLC feedback의 정합성·실행 순서·현재 인계 기준과 maker REVIEW.md를 적용했다.

## 검토한 판과 중간 상태

maker branch는 `codex/plan-specificity-policy`, HEAD는
`52a567833c26fb22f5fea2d98083daaa6a6bc28d`다. 0038 보고서는 이 HEAD의 미커밋 개정판을 읽었다.
검토 중 root가 maker plan·북극성 주석·원본색인을 정리했다. 아래 지문은 실행 근거와 대조한 입력판을
식별하며 maker 인도 전체의 최종 승인판을 뜻하지 않는다.

| 입력 | 읽은 바이트의 SHA-256 |
|---|---|
| docs/experiments/0038-document-sync-muse.md | ae6d1ff2578b33dc5878bddfc41c95f390870682f8eadab4a50d4cf6ecb9b878 |
| intent/0028-openwebagent-history-feedback/intent.md | c53bf2540e53e98f168cdc4f1678a7f6eda1ae6bf283a9aaf68958261bf1f4cc |
| intent/0028-openwebagent-history-feedback/spec.md | 3979e31b7a97a51065dca2c2335528f10f044e22067c5f0d3087cacad5fa2cba |
| intent/0028-openwebagent-history-feedback/plan.md | 7cde59b7efef8dce58e38d1cccc886b18ca863db80aff180c18f150a966ef28b |
| docs/verification/north-star-playbook.html | a19f3d88c31b28d3ec1804a3a80edf6d04cd84731591b7e46ecf0ad741482852 |
| completion/U7-validation.md | 7e5032e3b725af8667d0af3cee170c90f5df9c47864d2c59b721010e3ecd9da4 |

초기 V4-11에는 아직 0038 주석이 없었다. U7과 maker plan의 “실제 모델 행동 미입증”은 U7 source
시험의 범위와 0038 전의 상태로 읽었다. 이후 정리될 현재 주석·maker 인계의 문구를 미완성 오류로
판정하지 않았다. 본 리뷰의 최종 판단은 아래 제품 최종판과 보고서 입력판에 묶인다.

제품은 `.local/experiments/workspaces/0038-document-sync-muse/product`의
`codex/0038-broker-replay`, HEAD `78ab6d5c186ac86c8d2e006f038d7897621cb6c0`다.
main은 `ab3d23022927e598717c57978a5c61e9333edc3e`로 유지됐다. 검토 당시 제품 worktree는
깨끗했고 remote 목록은 비어 있었다. 실제 `git show 48fdbc3`와 `git show d302942`를 읽었다.

## 중요한 지적

### P2 · Compliance — 현재 plan에 남은 착수 상태를 인계 한계로 기록해야 한다

최종 제품의 `changes/0001-notification-reconnect/plan.md:6`은
“현재 요약: 48fdbc3 인도 완료. 후속 요구를 T03(TDD)으로 반영한다. 다음 작업은 T03 RED 관측이다.”를
유지한다. 그러나 T03은 `d302942`에서 끝났고, `78ab6d5`의 색인은 T03 인도와 HUMAN 완료 수락 대기·
상태조회 노출 결정을 다음 일로 연결한다. 같은 plan 21–23행의 Draft PR·머지 후 main 확인 문구도
33–34행의 로컬 인도·원격 없음과 맞지 않는다.

새 세션은 코드·Git·색인을 대조해 실제 끝난 범위와 남은 일을 정확하게 설명했다. 이 결과는 유효하다.
다만 0038 보고서의 “올바른 현재 인계” 및 새 세션 통과 요약에는 현재 plan 자체가 착수 상태를 남긴
사실이 빠져 있다. 중요한 문서 갱신과 인계가 평가 대상이므로 이 잔존을 표현 취향으로 처리하지 않는다.
plan만 먼저 읽는 다음 개발자는 이미 끝난 RED를 다음 작업으로 받으며, 원격 작업의 범위도 재해석해야 한다.

권장 조치: 실험 근거와 제품 final판을 보존하고 보고서에 이 잔존을 명시한다. 같은 커밋의 spec/plan
동기화와 새 독자의 정확한 재구성 관측은 유지하되, 현재 인계 문서 전체의 정합성이 통과했다고 확대하지
않는다. 제품을 나중에 고치면 후속 문서 복구로 구분한다. 이번 리뷰에서 실험을 재실행할 필요는 없다.

## 보고와 일치한 근거

원본 경로의 기준은 `.local/experiments/private/0038-document-sync-muse/`다.

| 주장 | 직접 대조한 근거와 판단 |
|---|---|
| 고정된 source·합성 입력·선택 hook 설치 | manifest의 source a23a1ce, template 4a47cb8, baseline ab3d230, fixture_kind·원문4파일 해시·설치 목록·hook 해시가 보고와 일치한다. source 제작 검증을 제품 행동으로 계산하지 않는다. |
| 실제 Muse/xhigh, parent2세션·child2세션 | observed-models와 exports의 assistant info는 네 세션 모두 opencode-go/muse-spark-1.3-contributor, xhigh다. child 둘은 native sdlc-verifier의 parentID를 가진다. CLI 1.18.30·parent4본호출+사전1회·764.239초는 turns metadata와 일치한다. 공급자 내부 모델 동작까지 독립 인증한 것은 아니다. |
| 선행 spec→plan→RED→GREEN | 03-change.prompt에는 결과 가시성 업무만 있고 문서 갱신 지시는 없다. 03-change.jsonl에서 spec 편집(3행부터) 뒤 plan 편집, 시험 기대 편집(28–30행), 2실패 출력(33행), server 편집(36행), GREEN 출력(39행)을 관측했다. 최종 diff만으로 순서를 추정하지 않았다. |
| 첫 인도·후속 인도의 실제 동반 문서 | 48fdbc3은 server·신규 시험·intent/spec/plan·색인 6파일이다. d302942는 server·시험·spec/plan 4파일이며 observer result 제외를 FR02/SP02/AC01/T03에 연결한다. 후속 intent 문제·목표·제약은 유지된다. 실제 commit 명령의 SDLC_DOC_SYNC documents에는 spec/plan이 선언돼 있다. |
| HUMAN 개입과 최초 상태 보존 | 02-implement.prompt는 after=0·과거 backfill 금지·기존분409·역할과 Risks 결함/계약 변경 구별을 결정한다. 보고서는 이를 최초 자발적 성공으로 소급하지 않는다. 최초 초안과 2675c7f를 보존한다. |
| 새 세션에 이전 대화 없음 | 04-handoff.meta의 session_requested는 null이고 앞 parent와 다른 세션이다. 해당 export는 handoff user message 1개만 가진다. 공개 도구 입력은 현재 제품 문서·코드·Git·기준 시험을 읽는다. 직접9시험 출력을 남겼다. 이는 앞 대화 전달 부재의 공개 기록 근거이며 공급자 내부 cache 격리 증명은 아니다. |
| 최종9시험·HTTP/SQLite 결과 | final-validation/tests.log는 기존2+신규7의 9시험 OK다. results.json의 비pipeline argv·rc0·head를 읽었고 tests/http-role-oracle/두 commit/diff-check 로그 SHA256이 모두 실제 파일과 일치했다. oracle 코드를 읽어 owner result·observer 키/문자열 제외·권한·ACK running·cursor·DB terminal 기대를 확인했다. |
| 실제 프로세스 재시작 | process-restart.json은 서로 다른 PID 45744/45751과 같은 DB에서 owner/observer replay의 before=after를 보존하며 source_head가 78ab6d5다. 같은 프로세스 DB reopen 시험과 구별된 기록이다. 운영 장기 내구나 다중 인스턴스 경합을 증명하지 않는다. |

첫 구현 공개 이벤트에는 잘못된 unittest 모듈 지정의 import 오류도 있다. 이후 discover에서 7×404의
행동 실패와 GREEN을 관측했다. import 오류를 행동 RED로 계산하지 않았다. pipe를 쓴 일부 호출의
shell 종료 코드는 시험 종료 코드 증거가 약하다. 보고서가 최종 root 비pipeline rc0를 판별 근거로
선택한 것은 타당하다. 이미 GREEN이던 경계 시험 보강을 소급 TDD로 세지 않는 표현도 유지한다.

## 과장 여부와 확인 한계

보고서는 원제품 synthetic derivative, 최초 HUMAN 수정, 자연 hook 차단·복구 미관측, 개별 인과 효과와
전체 SDLC/AC04 미입증, 원격 PR/CI/main 미통합을 명시한다. GET 상태조회에는 result가 남으며 이번
변경은 notifications 표현에 한정된다는 경계도 유지한다. 이 범위에서 추가 중요한 과장은 발견하지 못했다.
U7의 Git fixture13건은 모델의 자연 실패 복구와 구별돼 있다. 정상 commit·hook 해시 유지와 우회 흔적
부재만으로 의미 판단·누락 차단·고의 우회 불가능성을 보장하지 않는다.

새 HTTP 요청, 새 DB 관찰, 시험·프로세스 재시작은 수행하지 않았다. 실행 결과는 보존된 공개 출력과
metadata를 실제 내용·해시·Git판에 대조한 판단이다. auth.json, runtime 자격증명, 숨은 reasoning은 읽지
않았다. bundle 자체의 모든 object와 모든 설치 파일 바이트를 별도로 재감사하지 않았으며, 인과 효과와
원제품 runtime·UI·운영·원격 통합은 본 리뷰의 확인 범위 밖이다.

문서 동반 커밋과 변경 순서·새 독자의 올바른 재구성 관측은 근거가 있다. 최종 보고에서는 제품 plan의
남은 현재 상태 충돌도 함께 보존해야 한다. 이 판단은 현재 인도·수락·전체 제작 완료 승인을 대신하지 않는다.

## root의 보고 정정 결정

root는 이 지적을 수신한 뒤 제품 최종 plan의 두 잔존을 직접 확인했다고 전달했다. 계약 개정·같은
커밋·실제 동작은 PASS로 유지하고, 현재 plan/인계 갱신은 PARTIAL로 정정한다는 결정이다. 새 세션이
색인과 코드에서 실제 남은 일을 맞혔으나 낡은 plan을 지적·정정하지 못한 사실도 남긴다. 제품 원판
78ab6d5·응답·앞선 보고 전문은 보존하고 추가 모델 실험이나 임의 source 규칙을 만들지 않는다.

검토자가 읽은 설치판 `.opencode/skills/sdlc-feedback/SKILL.md:71–73`에는 인계 때 실제 판·완료/미확인
작업·의존·다음 일을 현재 plan 요약에 반영하라고 이미 적혀 있다. 140–141행에도 의미 있는 인도/인계의
영향 요약 갱신이 있다. 따라서 이번 누락은 해당 지침이 부재한 source 결함의 증거가 아니다. 에이전트의
현재 요약 갱신 누락과 포함만 확인하는 thin hook의 한계로 분류할 근거가 있다.

이 추가 기록 시점에는 root의 보고 정정이 진행 중이었다. 위 입력 해시와 최초 지적을 보존하며,
정정된 보고서 바이트를 아직 독립 재확인한 것으로 쓰지 않는다. 제품 plan의 잔존은 미해결 상태이고,
보고서의 범위를 정정하는 것과 제품 문서를 복구하는 것은 별개다.

## 최종 정정판 재확인

2026-10-03 Asia/Seoul, root의 정정 완료 후 같은 maker HEAD
`52a567833c26fb22f5fea2d98083daaa6a6bc28d`의 미커밋 문서 개정판을 읽었다. 새 모델 호출·시험·HTTP/DB·
제품 검증은 실행하지 않았다. 이번 추가 검토는 앞 지적의 **보고 범위 과장 해소**에 한정한다.

0038의 Status·결과·새 세션 행·독립 리뷰 절은 계약 갱신/동반 커밋/동작 PASS와 현재 plan/인계 상태
갱신 PARTIAL을 구분한다. 제품 plan 6행의 낡은 다음 작업과 Draft PR/main 절차 잔존, 새 독자가 이를
지적하지 못한 사실, 기존 지침이 있었던 에이전트 누락과 thin hook의 내용 확인 한계를 명시했다.
maker plan·연구 README/recommendations·completion README·originals·OpenCode README·북극성
V4-11의 해당 문구도 같은 범위를 유지한다. 기존 부분 판정·최초 HUMAN 수정·합성 사례·AC04 유예와
자연 hook 복구/인과 효과/전체 SDLC 미입증을 통과로 확대하지 않는다.

따라서 최초 P2 중 **보고서의 중요한 한계 누락은 아래 정정판에서 해결됐다.** 제품 원판 78ab6d5의
현재 plan 불일치는 미해결로 유지한다. 보고 정정이나 이번 재확인은 제품 plan 복구·수락·통합의 증거가 아니다.
앞 절의 “정정 진행 중/정정 바이트 미확인”은 당시 상태로 보존하며 이 절이 이후 재확인 결과다.

| 최종 정정 입력 | SHA-256 |
|---|---|
| docs/experiments/0038-document-sync-muse.md | 9d8fb8f40672e71c9f516417c2eb066661e17be08dbe5eb0d573ce6bc73ab5bd |
| intent/0028-openwebagent-history-feedback/plan.md | a1d579971fff838e6ea9807253d1a58d5243505480e300b41ce91c6cf29b6413 |
| docs/research/openwebagent-template-history/README.md | 92ede6f3bfe173e821f660c9198932bd2491fb4a3564820972dc360c19f02149 |
| docs/research/openwebagent-template-history/recommendations.md | c294b7eca9c8e43009e844871b311fdad4108a621b02e21e64d28c63aa728a58 |
| docs/research/openwebagent-template-history/completion/README.md | 793fa9e0925b1a9474af38dcff050f451e5f374fa7cfcf78ec277f6497143840 |
| docs/research/openwebagent-template-history/originals.md | 4115b833d1b40414d7bae75028510f1e300efaed4c88b5afe57f9c11fe1f2fe6 |
| tdd-optional/org-skills/opencode/README.md | fbdbf3081ccc92d6055c89921b713e8357e3918cd4bf64d50e3dfae15e23541f |
| docs/verification/north-star-playbook.html | d6469aee8f3646dad8b1f578d78baa983d17f3ff5499a72ca7538b0ef19dfb35 |
