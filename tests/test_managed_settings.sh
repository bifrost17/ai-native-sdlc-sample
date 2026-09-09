#!/usr/bin/env bash
# tests/test_managed_settings.sh — org/managed-settings.example.json 계약 시험 (`make test` 안).
# L12 899~926행이 정의하는 관리형 전용 키의 닫힌 목록 안에서만 이 예시가
# 키를 쓰는지 잰다(있는 척 넣은 미문서 키가 없어야 한다) + allowManagedHooksOnly
# 를 켰으면 hooks 블록이 있어야 한다(L12 920행 — 안 두면 프로젝트 훅이 전부 죽는다).
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$ROOT" || exit 1
FILE="org/managed-settings.example.json"

python3 - "$FILE" <<'PY'
import json, sys
path = sys.argv[1]
KNOWN = {"$schema", "//", "permissions", "allowManagedPermissionRulesOnly",
         "sandbox", "allowManagedHooksOnly", "disableSideloadFlags",
         "strictKnownMarketplaces", "allowManagedMcpServersOnly",
         "requiredMinimumVersion", "hooks"}
try:
    cfg = json.load(open(path, encoding="utf-8"))
except Exception as exc:
    print("JSON 파싱 실패: %s" % exc); sys.exit(2)
unknown = [k for k in cfg if k not in KNOWN]
if unknown:
    print("공식 목록 밖 키: %s" % unknown); sys.exit(1)
if cfg.get("allowManagedHooksOnly") is True and "hooks" not in cfg:
    print("allowManagedHooksOnly=true 인데 hooks 블록이 없다 — 프로젝트 훅이 전부 죽는다")
    sys.exit(1)
if "hooks" in cfg:
    names = set()
    for entries in cfg["hooks"].values():
        for e in entries:
            for h in e.get("hooks", []):
                names.add(h.get("command", "").split("/")[-1].strip('"'))
    readme = open("org/README.md", encoding="utf-8").read()
    missing = [n for n in names if n and n not in readme]
    if missing:
        print("org/README.md 가 등록된 훅을 언급하지 않는다: %s" % missing); sys.exit(1)
    # README 가 이름 댄 훅 파일(`*.sh`)은 실재해야 한다 — 지운 훅을 가리키던 자리를 계기가 못 봤다.
    import os, re
    ghost = [n for n in set(re.findall(r"`([a-z-]+\.sh)`", readme)) if not os.path.isfile(".claude/hooks/" + n)]
    if ghost:
        print("org/README.md 가 이름 댄 훅 파일이 없다: %s" % sorted(ghost)); sys.exit(1)
print("org/managed-settings.example.json 키 %d개 전부 공식 목록 안" % len(cfg))
PY
rc=$?
[ "$rc" -eq 0 ] && echo "PASS  managed-settings 키·훅 계약" || echo "FAIL  managed-settings 키·훅 계약 (rc=$rc)"
exit "$rc"
