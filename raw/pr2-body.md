F02 합성 실험의 두 번째 제품 변경입니다. 선행 PR #71의 merge commit `28b8fa8bff56d5becf2f8bfd63ffaa99b7f3dfac`에서 시작했습니다. 계획 `intent/0001-owner-list-and-summary/plan.md`의 PR2 범위를 구현합니다.

`summary [--owner <ID>]`가 open/done 건수를 고정된 두 줄로 출력합니다. 옵션이 없으면 미배정을 포함한 전체, 있으면 list와 같은 정확 일치 필터를 씁니다. 조회·요약의 필터를 작은 공통 함수로 재사용하고 기존 목록·show·complete를 유지합니다. 코드·관련 시험·README 사용법을 함께 담았습니다.

검증 대상 `a6f771bcab91687a6d6cfb33fb071b9de1cd70a4`: unittest 8/8(기존 5개+신규 3개), HUMAN의 독립 새 복사본 관측 7/7(목록·전체/담당자별/빈 요약·complete 후 요약, 원본 바이트 불변). 원래 시험 메서드와 helper의 AST가 불변이고 원본 fixture도 바이트 단위로 같음을 확인했습니다. diff는 3파일, 53 additions/3 deletions입니다.

통합 대상은 `codex/experiment-2026-09-11-f02-r01`이며 제작 main에 머지하지 않습니다. 호스티드 CI와 실제 조직의 다른 사람 계정 승인은 이번 실험 범위 밖입니다. HUMAN(Codex, simulated)의 실험 수락과 실제 GitHub PR 객체·merge를 구분해 기록합니다.
