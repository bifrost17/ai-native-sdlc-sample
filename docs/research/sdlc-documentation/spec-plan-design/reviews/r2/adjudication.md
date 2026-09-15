# r1 발견 처리와 r2 변경 범위

root 판단. Astra는 r1 PASS/비차단 1건, Opus/high는 CHANGES REQUIRED/차단 3건이다.
기술 spec 자체가 충분하다는 동의만으로 전달 과정의 회귀를 무시하지 않고 아래를 모두 처리한다.

| 발견 | 처리·변경 위치 | 결론 |
|---|---|---|
| Opus B1 정책 정본 링크 소실 | templates/spec·plan, guidance/execution-blocks·design-blocks 및 F03에서 기존 정책 정본 연결 | 수용 |
| Opus B2 기존 작성 스킬/참조 교체 모호 | policy-and-delivery의 실제 경로·보존/교체 표, L3/L4 근거·수락/출처·fix/mutation 지침 보존, provenance 동일 사본, 조건부 지침의 UI/성능 경계 유지 | 수용 |
| Opus B3 팀 TDD 위치/원문 혼동 | maker CLAUDE Conventions, 새 사용판 PROJECT-POLICY 검증/운영 행과 CLAUDE 참조, ADOPTING, 정확 feedback/verifier 절 지정. L9 verbatim 미수정 | 수용 |
| Astra A1 / Opus N2·N5 | walkthrough·입력·README/전달안 위치를 표에 명시, 후보 전체 링크 재배치 범위 설명 | 수용 |
| Opus N1 Upstream 의문 | 4a74823의 intent 네 경로와 23845b5의 spec 네 경로를 git cat-file로 확인, 모두 존재. 현재 동시 개정 F03/M01 plan은 Current change로 연결 | 의문 해소, 기존 핀 수정 불필요 |
| Opus N3 운영 정본 | M01 spec에서 design/operations는 조건, 제품 docs/operations는 실제 명령/절차라고 구분 | 수용 |
| Opus N4 공개 기록 위치 | F03 제품 intent/f03-owner-insights/decisions.md를 구체 기록 위치로 지정 | 수용 |
| root R1 공개 전 리허설 | F03 AC6/P4 사본 리허설과 실제 일반 공개/관측 구분 | 수용 |
| root R2 DB 선택 | M01 시작 시 기존 DB·user_version/스키마 확인, 실패 시 시작 거부·DB 비생성/fallback 없음; plan 선행 시험 연결 | 수용 |
| root R3/R4 시각 | 실제 owner 필드/Optional 타입, 짧은 cleanup 라벨 | 수용·재렌더 |
| root R5 인계 입력 | F03 context의 역사 자료를 필수 읽기에서 제외, 현재 spec/plan 정본 유지 | 수용·새 Sonnet 재점검 |

실제 제품 파일/스킬 설치는 여전히 범위 밖이다. r2에는 위 영향 경로만 바꾸며 F01/B01 기본 계약과
TDD 본문은 그대로다. 새 리뷰는 이 변경 및 연결 회귀에 집중한다. 최초 실패/한도/중단/리뷰를 덮어쓰지 않는다.
