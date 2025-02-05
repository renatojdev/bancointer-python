.PHONY: install

PE=PIPENV_IGNORE_VIRTUALENVS=1 PIPENV_VERBOSITY=-1 pipenv

install:
	$(PE) run pip install '.[dev]' # install dev dependencies

black:
	$(PE) run black . --check

coverage:
	$(PE) run coverage report -m

test:
	$(PE) run python tests/tests_models.py # suite tests
	$(PE) run python tests/tests_cobranca.py
	$(PE) run python tests/tests_banking.py
	$(PE) run python tests/tests_pix.py

dev:
	make install
	make test

clean:
	@echo "Limpando arquivos gerados..."
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.py[co]' -exec rm -f {} +
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .eggs/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	@echo "Limpeza concluída!"