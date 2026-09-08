.PHONY: check test help

check:
	bash scripts/check_all.sh

test:
	@echo "no tests yet (W1)"

help:
	@echo "Targets:"
	@echo "  check  - run scripts/check_all.sh (gate of record)"
	@echo "  test   - placeholder until W1"
	@echo "  help   - this message"
