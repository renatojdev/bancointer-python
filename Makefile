.PHONY: install

PE=PIPENV_IGNORE_VIRTUALENVS=1 PIPENV_VERBOSITY=-1 pipenv

install:
	$(PE) run python setup.py install

black:
	$(PE) run black . --check

coverage:
	$(PE) run coverage report -m

test:
	$(PE) run python tests/tests_models.py # suite tests
	$(PE) run python tests/test_emitir_cobranca.py
	$(PE) run python tests/test_recuperar_cobranca.py
	$(PE) run python tests/test_recuperar_cobranca_pdf.py
	$(PE) run python tests/test_cancelar_cobranca.py

dev:
	make install
	make test