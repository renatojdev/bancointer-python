.PHONY: install

PE=PIPENV_IGNORE_VIRTUALENVS=1 PIPENV_VERBOSITY=-1 pipenv

install:
	$(PE) run python setup.py install

black:
	$(PE) run black . --check

coverage:
	$(PE) run coverage report -m

test:
	$(PE) run python tests/tests.py

dev:
	make install
	make test