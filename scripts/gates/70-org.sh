# scripts/gates/70-org.sh — 관리형 설정 예시 게이트(설계안 §6.3).
#
# scripts/check_all.sh 가 scripts/gates/*.sh 를 source 하는 확장 지점(PR #7,
# feat/0001-artifact-validator)이 main 에 들어오면 이 한 줄이 게이트 정본에
# 그대로 붙는다 — check_all.sh 자체는 이 레인이 만지지 않는다(파일 소유 1:1).
# 그 확장 지점이 아직 main 에 없는 동안은 run_gate 가 정의돼 있지 않아 이
# 파일을 단독 실행(bash scripts/gates/70-org.sh)하면 그 사실 그대로 에러가
# 난다 — 그 원문을 브리프 보고에 남긴다.
run_gate "관리형 설정 예시" bash tests/test_managed_settings.sh
