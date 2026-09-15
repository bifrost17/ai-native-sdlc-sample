# 합성 경계 사례 입력 preflight

2026-09-14. `boundary-input/{intent,spec,contracts,recovery}.md` 전체를 한 번 검토했다.
목적은 정당한 이월/과잉반려 대조에 앞서 실제 중요한 계약 모순이 있는지 확인하는 dataset preflight다.
root의 충분성 가정을 근거로 삼지 않았고 제품 코드·실행 결과·plan은 없는 설계 후보로 읽었다.
입력 문서는 수정하지 않았으며 이 결과를 Muse 실험 호출이나 독립 최종 제작 검증으로 세지 않는다.

## 발견

검토한 지원 범위에서 실제 중요한 계약 모순이나 인계를 막는 공백을 확인하지 못했다.
따라서 이번 preflight에서 수정이 필요한 위치를 제시할 발견은 없다.

공유 경계는 `contracts.md:4–21`의 입력 유효성·동일 ID 판정·snapshot·result 수락/거절 순서와
`contracts.md:29–36`의 R 멱등 발행·충돌·불명 결과를 대조했다. `spec.md:14–24`의 AC와
`recovery.md:10–19`의 효과 순서는 발행 호출의 중복과 요청당 한 저장 결과를 구별한다.

독립 장애는 `recovery.md:24–28`에 W만/C만/R만/C와 W/원장 실패가 각각 연결돼 있다.
특히 C가 살아 있는 W 장애 대기의 조회 허용과 C 기동 때 이전 W 확인 실패의 readiness false는
`recovery.md:30–33`에서 구분되며 `spec.md:19–23`과 모순되지 않는다. calculating만 재계산하고
publishing/published의 확정 합계를 보존하는 계약도 `contracts.md:16–27`과 맞는다.

`spec.md:42–47`의 내부 분해·원장 라이브러리·배포 값은 원자성·단독 writer·W 권한 제약을
선행 조건으로 남겼다. 지정한 공유 동작을 구현자가 임의로 바꾸도록 이월한 것으로 보지 않았다.
원장 디스크 소실과 R의 내구성/멱등 계약 변경은 `intent.md:19`, `spec.md:39`, `contracts.md:36`에서
지원 범위 밖임을 구별했다. 이월된 실제 실행 시험을 설계 공백이나 이미 통과한 시험으로 취급하지 않았다.

## 입력판과 한계

| 입력 | SHA-256 |
|---|---|
| intent.md | `332d74e1d1e27ddbdabadb40ccd03fb686b76c91c89628e887c177b4824fee1f` |
| spec.md | `41984b04f4c8d1cce35535173d180ab4efd06f607f22a23f80d959687c2bd27e` |
| contracts.md | `c48156d11523034a00726228106ca871538ef5e265c72b03a6f25bc204ca0de0` |
| recovery.md | `f0213ac6df8f34962dff172fc5f07350ac84db2c7999ec228c59e103c71f7177` |

이는 한 검토자의 제한된 문서 대조다. 무결함 설계, 실제 구현 가능성 시험, 재시작·내구성·성능의
실행 성공을 증명하지 않으며 사람의 spec 수락을 대신하지 않는다. 검토자는 검토 절차 보완의 설계와
구현에 참여했으므로 이 preflight를 제작 변경에 대한 독립 최종 심사로 표현하지 않는다.
