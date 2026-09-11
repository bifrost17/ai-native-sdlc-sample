# F02: 계획 인계·두 순차 통합·구현 중 갱신

root는 **사람 리뷰를 포함한 이 작은 실행 범위의 결과를 통과**로 판단했다. 계획 작성 대화를
받지 않은 새 Claude Code 세션이 첫 기능을 구현했고, 두 PR에 해당하는 변경을 로컬 제품 main에
순차 통합했다. PR1의 plan 누락은 실패로 보존했으며 HUMAN이 요청한 복구를 자발적 갱신 성공으로
세지 않는다. [프로토콜](protocol.md), [초기 판](initial-receipt.json), [최종 판](final-receipt.json).

## 실제 대화와 판

| 턴 | 입력과 실제 결과 | 판단 |
|---|---|---|
| [1](turn-01.md) | 합의된 intent 8a43246·spec fa3d4ba, 실제 코드와 선택 plan skill을 읽고 e14345b 작성 | 목록 먼저, 공유 파일·선택 의미로 순차 두 PR, PR별 main 상태/Proof를 정함 |
| [2](turn-02.md) | HUMAN이 원래 대화 없는 인계를 점검하게 하자 문서가 main에 없다는 base 공백 발견 → 9cb9894 | 사람의 인계 질문 뒤 보완. root가 이 판 수락 후 문서를 d6660fb로 먼저 통합 |
| [3](turn-03.md) | 새 세션에서 최신 제품 main의 별도 worktree로 PR1 구현 1033eea, 8시험 통과 | 제품 동작은 통과. 낡은 plan 설명을 알면서 남긴 것은 문서 갱신 실패 |
| [4](turn-04.md) | HUMAN의 구체 피드백 후 10b08bc로 amend, plan+구현 같은 커밋 | assisted recovery. 원래 1033eea 보존. 독립 목록/읽기 전용 6확인 뒤 91ccf7f 통합 |
| [5](turn-05.md) | 그 main에서 PR2 새 branch/worktree·새 세션. 기존 오류 검증 보강 요청에 plan·시험·코드·설명을 ee972b0에 함께 커밋 | 16시험 통과. 동작 요구 변화가 없어 intent/spec 유지. 없는 Verification 절 참조는 정정 필요 |
| [6](turn-06.md) | HUMAN의 문서 참조 정정 후 63328e1로 amend; 코드·시험 불변 | 존재하지 않는 참조를 실제 실행/커밋 기록으로 고침. 12독립 동작 확인 후 f20a165 통합 |

각 turn의 `-input.md`/`-prompt.txt`, `-invocation.json`, `.jsonl`, `-summary.json`, `-export.json`에
실제 입력·CLI 설정·필터링한 도구 I/O·모델 결과·비공개 추론 제외 해시를 남겼다. 입력은 실제
앞선 응답을 읽고 작성했다. 고정 대본을 미리 주지 않았다. 리뷰 보고의 PASS는 사람 역할 root의
관측 범위 판정이며 실제 조직의 제품 수락을 뜻하지 않는다.

## 무엇을 실제로 확인했나

- 계획 세션 e66d9410…, 첫 구현 dbd35e85…, 두 번째 구현 3625d764…의 서로 다른 세션 ID.
  새 구현에 이전 채팅/리뷰/출력 대본은 전달하지 않았다. plan과 선언된 spec·intent·현재 정책/코드,
  실제 Git 상태를 입력으로 썼다. 신입 엔지니어 본인 실험이나 참조 없는 plan 한 장 실험은 아니다.
- PR1만 통합한 main 91ccf7f에서 목록 기능이 사용 가능하고 summary는 아직 없다.
  [PR1 HUMAN 관측](pr1-human-oracles.json)은 목록 선택·기존 목록·바이트 보존과 미제공 summary를 확인한다.
- PR2는 91ccf7f에서 시작하고 최종 main f20a165에는 목록·요약·기존 명령이 함께 있다.
  [최종 HUMAN 관측](final-human-oracles.json)은 F02 원래 oracle 7개와 HANA/- 요약·기존 오류
  등 5개를 합쳐 12/12 통과했다. complete 이후 요약과 조회 바이트 보존을 포함한다.
- 실제 시험은 baseline 3개 → PR1 8개 → PR2 16개다. 기존 test_tracker.py와 requests.json,
  intent/spec 바이트를 유지했다. 구현·시험은 실험 branch에만 있고 maker 제품에는 추가하지 않았다.
- PR2의 검증 방법 보강은 plan 갱신을 직접 상기하지 않은 후속 작업 요청에서 같은 구현 커밋으로
  반영됐다. 이는 한 번의 관측이며 PR1의 실패를 지우거나 일반 성공률을 증명하지 않는다.

## 보존과 한계

maker 저장소에 codex/exp-0022-base, plan, owner, summary, main 및 실패 보존 refs를 유지한다.
정확한 이름·SHA는 final-receipt.json에 있고 실제 제품 clone과 worktree도 로컬에 남아 있다.
R1 사용판에서 실행했으며 R2 사용판 수정은 예시의 출처 경로/핀 설명뿐이다. 최종 plan 양식과
실행에 쓴 선택 skill 본문은 같다. R3는 maker 측 측정 설명의 연동 정정이다.

이는 Plan→Build→검증/로컬 통합 부분 실험이다. 요구 발굴, hosted PR·CI·운영 배포, 병렬 개발,
실제 데이터 이행/복구, 자동 스킬 발견은 확인하지 않았다. M01은 별도 정적 예시 검토다.
실수마다 새 정책·검사기를 넣지 않고 실제 결과·중요 문서 정합성·사람의 리뷰로 마무리했다.
독립 verifier도 최종 main과 PR1 상태의 시험·직접 동작·동일 커밋·보존된 실패를 확인했다.
[최종 보고](../reviews/verifier-final.md)와 [명령 원문](../reviews/verifier-logs/)을 함께 남겼다.
