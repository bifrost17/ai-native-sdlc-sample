#!/usr/bin/env bash
# scripts/deploy.sh — 배포 흉내. 실제로 배포하지 않는다.
#
# 존재 이유는 하나다: .claude/hooks/production-gate.sh 의 시험 대상이 되는 것.
# 레슨 11·12 의 「에이전트는 프로덕션 게이트까지 갈 수 있고 넘지는 못한다」를
# 시연하려면 게이트가 지키는 대상이 실물로 있어야 하는데, 이 샘플에는 배포 대상이
# 없다(설계안 §10 이월 원장: 「샌드박스 · MCP 배포 도구 · 롤백 리허설 · 환경별 티어 —
# 승격 조건: 실제 배포 대상」). 그래서 인자를 되읊는 것으로 대신한다.
#
# 이 스크립트는 승인을 스스로 검사하지 않는다. 승인은 훅이 본다 —
# 게이트를 대상 안에 두면 대상을 부르지 않는 경로로 우회할 수 있기 때문이다.
set -uo pipefail

echo "deploy.sh: 인자 = $*"

for arg in "$@"; do
  if [ "$arg" = "production" ] || [ "${arg#*=}" = "production" ]; then
    echo "deploy.sh: 대상이 production 이다 — 승인(RELEASE_APPROVAL)이 필요한 배포다."
    echo "deploy.sh: (흉내만 낸다. 실제 배포 대상은 없다.)"
    exit 0
  fi
done

echo "deploy.sh: 프로덕션이 아닌 환경 — 승인 없이 진행할 수 있다."
echo "deploy.sh: (흉내만 낸다. 실제 배포 대상은 없다.)"
exit 0
