# Playbook L9 line 619: "wrap it in a single target such as make test or npm test that exits non-zero on failure"
# Shared contract of the three lanes: test / evals / check. CI calls `make check`.
.PHONY: test evals check
test:
	python3 -m unittest discover -s tests
	bash tests/test_hooks.sh
evals:
	bash evals/run.sh
check: test evals
