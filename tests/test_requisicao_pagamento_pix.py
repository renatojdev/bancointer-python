# test_requisicao_pagamento_pix.py


import unittest

from bancointer.banking.models.destinatario_pagamento_pix import (
    DestinatarioPagamentoPix,
)
from bancointer.banking.models.instituicao_financeira import InstituicaoFinanceira
from bancointer.banking.models.requisicao_pagamento_pix import RequisicaoPagamentoPix
from bancointer.banking.models.tipo_conta import TipoConta
from bancointer.banking.models.tipo_destinatario_pagamento_pix import (
    TipoDestinatarioPagamentoPix,
)
from bancointer.utils.exceptions import BancoInterException


class TestRequisicaoPagamentoPix(unittest.TestCase):

    def setUp(self):
        """Cobranca object for test purposes."""
        self.pix_payment_request = RequisicaoPagamentoPix(
            46.17,
            DestinatarioPagamentoPix(
                TipoDestinatarioPagamentoPix.CHAVE, chave="+5541943339900"
            ),
        )

    def test_to_dict(self):
        dict_cobra = self.pix_payment_request.to_dict()
        # Using Assertions to Check Keys
        self.assertIn("valor", dict_cobra)
        self.assertIn("destinatario", dict_cobra)
        # Using Assertions to Check Values
        self.assertEqual(dict_cobra["valor"], 46.17)
        self.assertEqual(dict_cobra["destinatario"]["tipo"], "CHAVE")

    def test_to_dict_failures(self):
        # valor required
        self.pix_payment_request.valor = None
        with self.assertRaises(BancoInterException) as contexto:
            self.pix_payment_request.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'requisicaoPagamentoPix.valor' é obrigatório.",
        )
        # destinatario required
        destinatario = self.pix_payment_request.destinatario
        self.pix_payment_request.valor = 54.12
        self.pix_payment_request.destinatario = None
        with self.assertRaises(BancoInterException) as contexto:
            self.pix_payment_request.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'requisicaoPagamentoPix.destinatario' é obrigatório.",
        )

        # test invalid cases
        # valor
        self.pix_payment_request.destinatario = destinatario
        self.pix_payment_request.valor = "2.15"
        with self.assertRaises(BancoInterException) as contexto:
            self.pix_payment_request.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'requisicaoPagamentoPix.valor' é inválido. (de 2.5 até 99999999.99)",
        )
        # destinatario chave
        self.pix_payment_request.valor = "2.5"
        self.pix_payment_request.destinatario.chave = "email@invalido"
        with self.assertRaises(BancoInterException) as contexto:
            self.pix_payment_request.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'destinatarioPagamentoPix.chave' é inválido.",
        )
        # destinatario dados bancarios
        self.pix_payment_request.valor = "2.5"
        self.pix_payment_request.destinatario.chave = "email@teste.com"
        banks_data_dest = DestinatarioPagamentoPix(
            TipoDestinatarioPagamentoPix.DADOS_BANCARIOS,
            cpfCnpj="1239329",
            contaCorrente="3211",
        )
        self.pix_payment_request.destinatario = banks_data_dest
        # destinatario dados bancarios - tipoConta
        with self.assertRaises(BancoInterException) as contexto:
            self.pix_payment_request.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'destinatarioPagamentoPix.tipoConta' é obrigatório.",
        )
        # destinatario dados bancarios - agencia
        self.pix_payment_request.destinatario.tipoConta = TipoConta.CONTA_PAGAMENTO
        with self.assertRaises(BancoInterException) as contexto:
            self.pix_payment_request.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'destinatarioPagamentoPix.agencia' é obrigatório.",
        )
        # destinatario dados bancarios - nome
        self.pix_payment_request.destinatario.agencia = "0001"
        with self.assertRaises(BancoInterException) as contexto:
            self.pix_payment_request.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'destinatarioPagamentoPix.nome' é obrigatório.",
        )
        # destinatario dados bancarios - instituicaoFinanceira
        self.pix_payment_request.destinatario.nome = "Nome da Pessoa"
        with self.assertRaises(BancoInterException) as contexto:
            self.pix_payment_request.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'destinatarioPagamentoPix.instituicaoFinanceira' é obrigatório.",
        )
        # destinatario dados bancarios - cpfCnpj invalid
        self.pix_payment_request.destinatario.instituicaoFinanceira = (
            InstituicaoFinanceira("87654321")
        )
        with self.assertRaises(BancoInterException) as contexto:
            self.pix_payment_request.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'destinatarioPagamentoPix.cpfCnpj' é inválido.",
        )
        # destinatario pix copia e cola
        banks_data_dest = DestinatarioPagamentoPix(
            TipoDestinatarioPagamentoPix.PIX_COPIA_E_COLA
        )
        self.pix_payment_request.destinatario = banks_data_dest
        with self.assertRaises(BancoInterException) as contexto:
            self.pix_payment_request.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'destinatarioPagamentoPix.pixCopiaECola' é obrigatório.",
        )


if __name__ == "__main__":
    unittest.main()
