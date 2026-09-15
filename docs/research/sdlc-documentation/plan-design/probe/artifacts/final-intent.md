# Intent: 담당자 목록을 먼저 쓰고 주간 상태 요약을 잇기
Author: HUMAN Codex root, F02 모사. Status: draft.

## Problem
사내 요청 목록에서 내 담당 건을 찾는 일이 반복되고, 주간 확인에는 열린 건과 완료 건수를 따로 센다.

## Proposed outcome
담당자 목록부터 동료에게 인도하고 사용한다. 상태 요약까지 완성될 때까지 목록 전달을 기다리지 않는다.

## Affected users and systems
기존 로컬 요청 CLI를 쓰는 사내 동료, tracker.py와 JSON 데이터.

## Constraints
기존 명령·저장 필드 유지, 조회는 읽기 전용, 외부 서비스·계정·새 의존성 없음.

## Open questions
담당자 일치·요약 형식은 HUMAN과 spec 입력에서 합의한다. 이번 실험은 Plan부터 관측한다.
