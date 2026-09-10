F02 합성 개발 실험: 담당자별 요청 목록을 먼저 인도하는 변경입니다. 공통 intent/spec/plan은 상태 요약까지 설명하지만 이 PR의 제품 범위는 목록 조회입니다.

`list --owner <ID>`는 정확 일치하는 요청을 원본 순서와 기존 탭 형식으로 출력하며 done도 포함합니다. 없는 담당자는 빈 stdout/rc=0입니다. 구현·관련 시험·사용 설명을 같은 PR에 두었습니다. summary는 후속 PR 범위입니다.

검증 대상 `cff4c2b74ca45e3346d549a9a20b0eedfa6a515f`: 로컬 unittest 5/5(기존 3개 유지), HUMAN의 독립 CLI 관측 3/3(담당자/대소문자/전체 및 원본 바이트 불변). 계획의 README 추가·출처 정정도 실제 변경과 함께 기록했습니다. 전체 diff는 241 additions/1 deletion이며 그중 제품 코드는 4 additions/1 deletion, 관련 시험은 13 additions입니다. 줄 수만으로 크기를 판단하지 않았습니다.

HUMAN(Codex, simulated)이 대상 커밋을 읽고 단계 결정과 최종 통합 판단을 기록합니다. 실제 조직의 별도 사람 간 승인이나 호스티드 CI를 검증하는 실험은 아닙니다.

통합 대상은 `codex/experiment-2026-09-11-f02-r01`이며 제작 `main`에 머지하지 않습니다. 입력은 합성 데이터입니다.
