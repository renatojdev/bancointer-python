# tests_banking.py


import unittest

from test_consultar_extrato import TestConsultarExtrato
from test_consultar_extrato_pdf import TestConsultarExtratoPDF
from test_consultar_saldo import TestConsultarSaldo
from test_incluir_pagamento import TestIncluirPagamento
from test_incluir_pagamento_darf import TestIncluirPagamentoDarf
from test_cancelar_agendamento_pagamento import TestCancelaAgendamentoPagamento
from test_buscar_pagamento import TestBuscarPagamento
from test_buscar_pagamento_darf import TestBuscarPagamentoDarf
from test_incluir_pagamento_pix import TestIncluirPagamentoPix
from test_consultar_pagamento_pix import TestConsultarPagamentoPix


# Tests Suites
def suite():
    my_suite = unittest.TestSuite()

    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestConsultarSaldo)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestConsultarExtrato)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestConsultarExtratoPDF)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestIncluirPagamento)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestIncluirPagamentoDarf)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(
            TestCancelaAgendamentoPagamento
        )
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestBuscarPagamento)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestBuscarPagamentoDarf)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestIncluirPagamentoPix)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestConsultarPagamentoPix)
    )

    return my_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
