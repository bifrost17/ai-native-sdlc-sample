.PHONY: check test help

check:
	bash scripts/check_all.sh

test:
	python3 -m unittest discover -s tests -v

help:
	@echo "Targets:"
	@echo "  check  - run scripts/check_all.sh (gate of record)"
	@echo "  test   - run the unittest suite (tests/)"
	@echo "  help   - this message"
