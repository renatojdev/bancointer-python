# test_solicitacao_emitir_cobranca.py

import json
import unittest

from bancointer.cobranca_v3.models import Cobranca
from bancointer.cobranca_v3.models import Desconto
from bancointer.cobranca_v3.models.solicitacao_emitir_cobranca import (
    SolicitacaoEmitirCobranca,
)
from bancointer.cobranca_v3.models import Message
from bancointer.cobranca_v3.models import Mora
from bancointer.cobranca_v3.models import Multa
from bancointer.cobranca_v3.models import Pessoa
from bancointer.cobranca_v3.models import PersonType


class TestSolicitacaoEmitirCobranca(unittest.TestCase):
    def setUp(self):
        self.payer = Pessoa(
            "99999999999",  # valido
            PersonType.JURIDICA,
            "NOME DO PAGADOR",
            "ENDERECO DO PAGADOR",
            "CIDADE DO PAGADOR",
            "UF",
            80030000,
            "BAIRRO DO PAGADOR",
            "pagador@email.com",
            "41",
            "9" * 9,
            "9" * 4,
            "nao informado",
        )  # OU FISICA

        self.desconto = Desconto("PERCENTUALDATAINFORMADA", 60, 1.2, 2)
        self.multa = Multa("VALORFIXO", 0, 100)
        self.mora = Mora("TAXAMENSAL", 0, 4.5)
        self.message = Message("message 1", "message 2", "message 3", "", "message 5")
        self.beneficiarioFinal = self.payer

        new_cobranca = Cobranca.criar_sobranca_simples(
            "54321", 2.5, "2024-12-03", self.payer
        )
        new_cobranca.desconto = self.desconto
        new_cobranca.mensagem = self.message
        new_cobranca.beneficiarioFinal = self.beneficiarioFinal

        self.solicitacao_cobranca = SolicitacaoEmitirCobranca(new_cobranca)

    def test_to_dict(self):
        dict_sol_cobra = self.solicitacao_cobranca.to_dict()

        # Using Assertions to Check Keys
        self.assertIn("seuNumero", dict_sol_cobra)
        self.assertIn("valorNominal", dict_sol_cobra)
        self.assertIn("dataVencimento", dict_sol_cobra)
        self.assertIn("numDiasAgenda", dict_sol_cobra)
        self.assertIn("pagador", dict_sol_cobra)
        self.assertIn("desconto", dict_sol_cobra)
        # self.assertIn("multa", dict_sol_cobra)
        # self.assertIn("mora", dict_sol_cobra)
        self.assertIn("mensagem", dict_sol_cobra)
        self.assertIn("beneficiarioFinal", dict_sol_cobra)

        # Using Assertions to Check Values
        self.assertEqual(dict_sol_cobra["seuNumero"], "54321")
        self.assertEqual(dict_sol_cobra["valorNominal"], 2.5)
        self.assertEqual(dict_sol_cobra["dataVencimento"], "2024-12-03")
        self.assertEqual(dict_sol_cobra["numDiasAgenda"], 60)
        self.assertEqual(dict_sol_cobra["pagador"], self.payer.to_dict())
        self.assertEqual(dict_sol_cobra["desconto"], self.desconto.to_dict())
        # self.assertEqual(dict_sol_cobra["multa"], None)
        # self.assertEqual(dict_sol_cobra["mora"], None)
        self.assertEqual(dict_sol_cobra["mensagem"], self.message.to_dict())
        self.assertEqual(
            dict_sol_cobra["beneficiarioFinal"], self.beneficiarioFinal.to_dict()
        )

    def test_to_json(self):
        """Testa se o metodo to_json retorna uma string JSON valida."""
        json_cobranca = self.solicitacao_cobranca.to_json()
        # Verifica se o resultado e uma string
        self.assertIsInstance(json_cobranca, str)

        # Verifica se a string JSON contém as chaves esperadas
        data = json.loads(json_cobranca)
        self.assertEqual(data["seuNumero"], "54321")
        self.assertEqual(data["valorNominal"], 2.5)
        self.assertEqual(data["dataVencimento"], "2024-12-03")
        self.assertEqual(data["numDiasAgenda"], 60)
        self.assertEqual(data["pagador"], self.payer.to_dict())
        self.assertEqual(data["desconto"], self.desconto.to_dict())
        # self.assertEqual(data["multa"], None)
        # self.assertEqual(data["mora"], None)
        self.assertEqual(data["mensagem"], self.message.to_dict())
        self.assertEqual(data["beneficiarioFinal"], self.beneficiarioFinal.to_dict())

    def test_from_json(self):
        """Testa se o metodo from_json cria um objeto Discount corretamente."""
        json_cobranca = self.solicitacao_cobranca.to_json()
        new_cobranca = SolicitacaoEmitirCobranca.from_json(json_cobranca)

        # Verifica se o novo objeto é uma instância de Person
        self.assertIsInstance(new_cobranca, SolicitacaoEmitirCobranca)

        # Verifica se os atributos do novo objeto correspondem aos originais
        self.assertEqual(
            new_cobranca.cobranca.seuNumero,
            self.solicitacao_cobranca.cobranca.seuNumero,
        )
        self.assertEqual(
            new_cobranca.cobranca.valorNominal,
            self.solicitacao_cobranca.cobranca.valorNominal,
        )
        self.assertEqual(
            new_cobranca.cobranca.dataVencimento,
            self.solicitacao_cobranca.cobranca.dataVencimento,
        )
        self.assertEqual(
            new_cobranca.cobranca.numDiasAgenda,
            self.solicitacao_cobranca.cobranca.numDiasAgenda,
        )
        self.assertEqual(
            new_cobranca.cobranca.pagador, self.solicitacao_cobranca.cobranca.pagador
        )
        self.assertEqual(
            new_cobranca.cobranca.descontos,
            self.solicitacao_cobranca.cobranca.descontos,
        )
        self.assertEqual(
            new_cobranca.cobranca.multa, self.solicitacao_cobranca.cobranca.multa
        )
        self.assertEqual(
            new_cobranca.cobranca.mora, self.solicitacao_cobranca.cobranca.mora
        )
        self.assertEqual(
            new_cobranca.cobranca.mensagem, self.solicitacao_cobranca.cobranca.mensagem
        )
        self.assertEqual(
            new_cobranca.cobranca.beneficiarioFinal,
            self.solicitacao_cobranca.cobranca.beneficiarioFinal,
        )


if __name__ == "__main__":
    unittest.main()
