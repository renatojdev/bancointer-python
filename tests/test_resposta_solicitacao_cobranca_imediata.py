# test_resposta_solicitacao_cobranca_imediata.py


import json
import unittest

from bancointer.pix.models.resposta_solicitacao_cobranca_imediata import (
    RespostaSolicitacaoCobrancaImediata,
)

RESPONSE_SOL_COB_IMEDIATA = b"""{
          "status": "ATIVA",
          "valor": {
            "original": "46.17",
            "modalidadeAlteracao": 0
          },
          "calendario": {
            "expiracao": 3600,
            "criacao": "2024-11-28T18:19:55.524Z"
          },
          "txid": "j0oyh6jalasnd3bm3r5q2tpqjc8ukhgma0f",
          "revisao": 0,
          "chave": "+5551983334490",
          "devedor": {
            "nome": "Joao da Silva",
            "cpf": "12345678901"
          },
          "loc": {
            "id": 16788,
            "location": "https://cdpj-sandbox.partners.uatinter.co/pj-s/v2/f29d38322b154e95a53838df5acf96e1",
            "tipoCob": "cob",
            "criacao": "2024-11-28T18:19:55.512Z"
          },
          "location": "https://cdpj-sandbox.partners.uatinter.co/pj-s/v2/f29d38322b154e95a53838df5acf96e1",
          "pixCopiaECola": "00020101021226960014BR.GOV.BCB.PIX2574cdpj-sandbox.partners.uatinter.co/pj-s/v2/f29d38322b154e95a53838df5acf96e1520400005303986540546.175802BR5901*6013BELO HORIZONT61089999999962070503***630407CB",
          "solicitacaoPagador": "Servico realizado.",
          "infoAdicionais": [
            {
              "nome": "Campo 1",
              "valor": "Informacao Adicional1 do PSP-Recebedor"
            }
          ]
        }"""


class TestRespostaSolicitacaoCobrancaImediata(unittest.TestCase):

    def setUp(self):
        self.resposta_sol_cob_imediata = RespostaSolicitacaoCobrancaImediata(
            **json.loads(RESPONSE_SOL_COB_IMEDIATA)
        )

    def test_to_dict(self):
        resposta_sol_cob_imediata_dict = self.resposta_sol_cob_imediata.to_dict()

        # Using Assertions to Check Keys
        self.assertIn("status", resposta_sol_cob_imediata_dict)
        self.assertIn("valor", resposta_sol_cob_imediata_dict)
        self.assertIn("calendario", resposta_sol_cob_imediata_dict)
        self.assertIn("txid", resposta_sol_cob_imediata_dict)

        # Using Assertions to Check Values
        self.assertEqual(resposta_sol_cob_imediata_dict["status"], "ATIVA")
        self.assertEqual(resposta_sol_cob_imediata_dict["valor"]["original"], "46.17")
        self.assertEqual(
            resposta_sol_cob_imediata_dict["calendario"]["expiracao"],
            3600,
        )
        self.assertEqual(
            resposta_sol_cob_imediata_dict["txid"],
            "j0oyh6jalasnd3bm3r5q2tpqjc8ukhgma0f",
        )
        self.assertEqual(resposta_sol_cob_imediata_dict["revisao"], 0)
        self.assertEqual(resposta_sol_cob_imediata_dict["chave"], "+5551983334490")
        self.assertEqual(
            resposta_sol_cob_imediata_dict["devedor"]["nome"], "Joao da Silva"
        )
        self.assertEqual(resposta_sol_cob_imediata_dict["loc"]["id"], 16788)
        self.assertEqual(
            resposta_sol_cob_imediata_dict["pixCopiaECola"],
            "00020101021226960014BR.GOV.BCB.PIX2574cdpj-sandbox.partners.uatinter.co/pj-s/v2/f29d38322b154e95a53838df5acf96e1520400005303986540546.175802BR5901*6013BELO HORIZONT61089999999962070503***630407CB",
        )
        self.assertEqual(
            resposta_sol_cob_imediata_dict["infoAdicionais"][0]["nome"],
            "Campo 1",
        )


if __name__ == "__main__":
    unittest.main()
