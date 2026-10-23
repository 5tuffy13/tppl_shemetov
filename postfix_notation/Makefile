VENV = .venv
PYTHON = $(VENV)/bin/python
PYTEST = $(VENV)/bin/pytest
ARGS ?= 3 0 4 ~ 2 ~

all: run

$(VENV)/bin/activate:
	@if command -v uv >/dev/null 2>&1; then \
		uv venv $(VENV) && (uv pip install --offline pytest pytest-cov 2>/dev/null || uv pip install pytest pytest-cov); \
	else \
		python3 -m venv $(VENV) && $(VENV)/bin/pip install pytest pytest-cov; \
	fi

run: $(VENV)/bin/activate
	@$(PYTHON) main.py '$(ARGS)'

test: $(VENV)/bin/activate
	@$(PYTEST) --cov=main --cov-report=term-missing test_postfix.py

clean:
	rm -rf $(VENV) __pycache__ .pytest_cache .coverage htmlcov

.PHONY: all run test clean
