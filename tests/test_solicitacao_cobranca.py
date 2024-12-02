# test_solicitacao_cobranca.py


import json
import unittest

from bancointer.pix.models.solicitacao_cobranca import (
    SolicitacaoCobranca,
)
from bancointer.utils.exceptions import BancoInterException

SOL_COB_IMMEDIATE_REQUEST = b"""{
                              "calendario": {
                                "expiracao": 3600
                              },
                              "devedor": {
                                "nome": "Joao da Silva",
                                "cpf": "12345678901",
                                "cnpj": null
                              },
                              "valor": {
                                "original": "46.17",
                                "modalidadeAlteracao": 0
                              },
                              "chave": "+5551983334490",
                              "solicitacaoPagador": "Servico realizado.",
                              "infoAdicionais": {
                                "nome": "Campo 1",
                                "valor": "Informacao Adicional1 do PSP-Recebedor"
                              }
                            }"""


SOL_COBV_REQUEST = b"""{
              "calendario": {
                "dataDeVencimento": "2020-12-31",
                "validadeAposVencimento": 30
              },
              "loc": {
                "id": 789
              },
              "devedor": {
                "logradouro": "Alameda Souza, Numero 80, Bairro Braz",
                "cidade": "Recife",
                "uf": "PE",
                "cep": "70011750",
                "cpf": "12345678909",
                "nome": "Francisco da Silva"
              },
              "valor": {
                "original": "123.45",
                "multa": {
                  "modalidade": "2",
                  "valorPerc": "15.00"
                },
                "juros": {
                  "modalidade": "2",
                  "valorPerc": "2.00"
                },
                "desconto": {
                  "modalidade": "1",
                  "descontoDataFixa": [
                    {
                      "data": "2020-11-30",
                      "valorPerc": "30.00"
                    }
                  ]
                }
              },
              "chave": "5f84a4c5-c5cb-4599-9f13-7eb4d419dacc",
              "solicitacaoPagador": "Cobranca dos servicos prestados."
            }"""


class TestSolicitacaoCobranca(unittest.TestCase):

    def setUp(self):
        """Cobranca object for test purposes."""
        self.sol_cob_immediate = SolicitacaoCobranca(
            **json.loads(SOL_COB_IMMEDIATE_REQUEST)
        )
        self.sol_cobv_venc = SolicitacaoCobranca(**json.loads(SOL_COBV_REQUEST))

    def test_to_dict(self):
        dict_cobra = self.sol_cob_immediate.to_dict()
        # Using Assertions to Check Keys
        self.assertIn("calendario", dict_cobra)
        self.assertIn("devedor", dict_cobra)
        self.assertIn("valor", dict_cobra)
        self.assertIn("chave", dict_cobra)
        self.assertIn("solicitacaoPagador", dict_cobra)
        self.assertIn("infoAdicionais", dict_cobra)
        # Using Assertions to Check Values
        self.assertEqual(
            dict_cobra["calendario"]["expiracao"],
            3600,
        )
        self.assertEqual(
            dict_cobra["devedor"]["nome"],
            "Joao da Silva",
        )
        self.assertEqual(
            dict_cobra["devedor"]["cpf"],
            "12345678901",
        )
        self.assertEqual(
            dict_cobra["valor"]["original"],
            "46.17",
        )
        self.assertEqual(
            dict_cobra["valor"]["modalidadeAlteracao"],
            0,
        )
        self.assertEqual(
            dict_cobra["chave"],
            "+5551983334490",
        )
        self.assertEqual(
            dict_cobra["solicitacaoPagador"],
            "Servico realizado.",
        )
        self.assertEqual(
            dict_cobra["infoAdicionais"]["nome"],
            "Campo 1",
        )
        self.assertEqual(
            dict_cobra["infoAdicionais"]["valor"],
            "Informacao Adicional1 do PSP-Recebedor",
        )

    def test_to_dict_failures(self):
        # calendario required
        calendario = self.sol_cob_immediate.calendario
        self.sol_cob_immediate.calendario = None
        with self.assertRaises(BancoInterException) as contexto:
            self.sol_cob_immediate.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'solicitacaoCobrancaImediata.calendario' é obrigatório.",
        )
        # valor required
        self.sol_cob_immediate.calendario = calendario
        self.sol_cob_immediate.valor = None
        with self.assertRaises(BancoInterException) as contexto:
            self.sol_cob_immediate.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'solicitacaoCobrancaImediata.valor' é obrigatório.",
        )
        # chave required
        self.sol_cob_immediate.valor = 54.16
        self.sol_cob_immediate.chave = ""
        with self.assertRaises(BancoInterException) as contexto:
            self.sol_cob_immediate.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'solicitacaoCobrancaImediata.chave' é obrigatório.",
        )

        # test invalid cases
        # chave
        self.sol_cob_immediate.chave = "xpto"
        with self.assertRaises(BancoInterException) as contexto:
            self.sol_cob_immediate.to_dict()
        self.assertEqual(
            contexto.exception.erro.codigo,
            502,
        )
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'solicitacaoCobrancaImediata.chave' é inválido.",
        )

    def test_cobv_to_dict(self):
        dict_cobrav = self.sol_cobv_venc.to_dict()
        # Using Assertions to Check Keys
        self.assertIn("calendario", dict_cobrav)
        self.assertIn("dataDeVencimento", dict_cobrav["calendario"])
        self.assertIn("validadeAposVencimento", dict_cobrav["calendario"])
        self.assertIn("devedor", dict_cobrav)
        self.assertIn("valor", dict_cobrav)
        self.assertIn("original", dict_cobrav["valor"])
        self.assertIn("multa", dict_cobrav["valor"])
        self.assertIn("juros", dict_cobrav["valor"])
        self.assertIn("desconto", dict_cobrav["valor"])
        self.assertIn("modalidade", dict_cobrav["valor"]["desconto"])
        self.assertIn("data", dict_cobrav["valor"]["desconto"]["descontoDataFixa"][0])
        self.assertIn(
            "valorPerc", dict_cobrav["valor"]["desconto"]["descontoDataFixa"][0]
        )
        # Using Assertions to Check Values
        self.assertEqual(
            dict_cobrav["calendario"]["dataDeVencimento"],
            "2020-12-31",
        )
        self.assertEqual(
            dict_cobrav["devedor"]["logradouro"],
            "Alameda Souza, Numero 80, Bairro Braz",
        )
        self.assertEqual(
            dict_cobrav["valor"]["multa"]["modalidade"],
            "2",
        )
        self.assertEqual(
            dict_cobrav["valor"]["desconto"]["descontoDataFixa"][0]["valorPerc"],
            "30.00",
        )
        self.assertEqual(
            dict_cobrav["chave"],
            "5f84a4c5-c5cb-4599-9f13-7eb4d419dacc",
        )


if __name__ == "__main__":
    unittest.main()
