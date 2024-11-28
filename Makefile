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
