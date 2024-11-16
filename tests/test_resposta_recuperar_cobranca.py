# test_resposta_recuperar_cobranca.py

import unittest

from bancointer.cobranca_v3.models import RespostaRecuperarCobranca

COBRANCA_DICT = {
    "cobranca": {
        "seuNumero": "0001",
        "dataEmissao": "2024-11-15",
        "dataVencimento": "2024-11-25",
        "valorNominal": 2.5,
        "tipoCobranca": "SIMPLES",
        "situacao": "CANCELADO",
        "dataSituacao": "2024-11-15",
        "arquivada": False,
        "descontos": [
            {"codigo": "PERCENTUALDATAINFORMADA", "quantidadeDias": 0, "taxa": 1.2}
        ],
        "multa": {"codigo": "VALORFIXO", "valor": 100.0},
        "pagador": {
            "cpfCnpj": "99999999999",
            "tipoPessoa": "FISICA",
            "nome": "NOME DO PAGADOR",
            "endereco": "ENDERECO DO PAGADOR",
            "bairro": "",
            "cidade": "CIDADE DO PAGADOR",
            "uf": "PR",
            "cep": "80030000",
            "email": "",
            "ddd": "",
            "telefone": "",
            "numero": "",
            "complemento": "",
        },
    },
    "boleto": {
        "nossoNumero": "3364530754",
        "codigoBarras": "00000033641836470815337235685554229868141108",
        "linhaDigitavel": "00000033641836423654817780323916330249526185444",
    },
    "pix": {
        "txid": "336418361731693413000jHo3g7F0F2XXcE",
        "pixCopiaECola": "000201010212261010014BR.GOV.BCB.PIX2579cdpj-sandbox.partners.uatinter.co/pj-s/v2/cobv/9ba336dffb5d483c995e08e586da6cad52040000530398654042.505802BR5901*6013Belo Horizont61089999999962070503***630439AC",
    },
    "campos_adicionais": {},
}


class TestRespostaRecuperarCobranca(unittest.TestCase):

    def setUp(self):
        self.resposta_recuperar_cobranca = RespostaRecuperarCobranca(**COBRANCA_DICT)

    def test_to_dict(self):
        dict_sol_cobra = self.resposta_recuperar_cobranca.to_dict()

        # Using Assertions to Check Keys
        self.assertIn("cobranca", dict_sol_cobra)
        self.assertIn("boleto", dict_sol_cobra)
        self.assertIn("pix", dict_sol_cobra)

        # Using Assertions to Check Values
        self.assertEqual(
            dict_sol_cobra["cobranca"], self.resposta_recuperar_cobranca.cobranca
        )
        self.assertEqual(
            dict_sol_cobra["boleto"], self.resposta_recuperar_cobranca.boleto
        )
        self.assertEqual(dict_sol_cobra["pix"], self.resposta_recuperar_cobranca.pix)

    def test_add_campo_adicional(self):
        self.resposta_recuperar_cobranca.add_campo_adicional("campo_add_1", 1)
        self.resposta_recuperar_cobranca.add_campo_adicional("campo_add_2", 2)
        self.resposta_recuperar_cobranca.add_campo_adicional("campo_add_3", 3)

        # Using Assertions to Check Keys
        self.assertIn("campo_add_1", self.resposta_recuperar_cobranca.campos_adicionais)
        self.assertIn("campo_add_2", self.resposta_recuperar_cobranca.campos_adicionais)
        self.assertIn("campo_add_3", self.resposta_recuperar_cobranca.campos_adicionais)

        # Using Assertions to Check Values
        resp_cobra_dict = self.resposta_recuperar_cobranca.to_dict()
        self.assertEqual(resp_cobra_dict["campos_adicionais"]["campo_add_1"], 1)
        self.assertEqual(resp_cobra_dict["campos_adicionais"]["campo_add_2"], 2)
        self.assertEqual(resp_cobra_dict["campos_adicionais"]["campo_add_3"], 3)


if __name__ == "__main__":
    unittest.main()
