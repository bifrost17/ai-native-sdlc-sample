# Playbook L9 line 619: "wrap it in a single target such as make test or npm test that exits non-zero on failure"
# check = test. evals need ANTHROPIC_API_KEY (rc=2 SKIP without it), so they are not a PR check here;
# .github/workflows/agent-evals.yml runs `make evals` with the key — L10 line 689: "on a schedule and on
# any change to CLAUDE.md, skills, or hooks".
.PHONY: test evals check
test:
	python3 -m unittest discover -s tests
	bash tests/test_hooks.sh
	bash tests/test_evals.sh
	bash tests/test_managed_settings.sh
evals:
	@[ -n "$$ANTHROPIC_API_KEY" ] || { echo "SKIP: ANTHROPIC_API_KEY 없음 — evals 는 돌지 않았다(rc=2, 통과 아님)"; exit 2; }
	bash evals/run.sh
check: test
