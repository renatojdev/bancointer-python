# test_resposta_solicitacao_cobranca_imediata.py


import json
import unittest

from bancointer.pix.models.resposta_solicitacao_cobranca import (
    RespostaSolicitacaoCobranca,
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
          ],
          "pix": [
            {
              "endToEndId": "E12345678202009091221kkkkkkkkkkk",
              "txid": "655dfdb1a4514b8fbb58254b958913fb",
              "valor": "110.00",
              "horario": "2020-09-09T20:15:00.358Z",
              "infoPagador": "0123456789",
              "devolucoes": [
                {
                  "id": "123ABC",
                  "rtrId": "Dxxxxxxxx202009091221kkkkkkkkkkk",
                  "valor": "10.00",
                  "horario": {
                    "solicitacao": "2020-09-09T20:15:00.358Z"
                  },
                  "status": "EM_PROCESSAMENTO"
                }
              ]
            }
          ]
        }"""


class TestRespostaSolicitacaoCobrancaImediata(unittest.TestCase):

    def setUp(self):
        self.resposta_sol_cob_imediata = RespostaSolicitacaoCobranca(
            **json.loads(RESPONSE_SOL_COB_IMEDIATA)
        )

    def test_to_dict(self):
        resposta_sol_cob_imediata_dict = self.resposta_sol_cob_imediata.to_dict()

        # Using Assertions to Check Keys
        self.assertIn("status", resposta_sol_cob_imediata_dict)
        self.assertIn("valor", resposta_sol_cob_imediata_dict)
        self.assertIn("calendario", resposta_sol_cob_imediata_dict)
        self.assertIn("txid", resposta_sol_cob_imediata_dict)
        self.assertIn("infoAdicionais", resposta_sol_cob_imediata_dict)
        self.assertIn("pix", resposta_sol_cob_imediata_dict)

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
        self.assertEqual(
            resposta_sol_cob_imediata_dict["pix"][0]["endToEndId"],
            "E12345678202009091221kkkkkkkkkkk",
        )
        self.assertEqual(
            resposta_sol_cob_imediata_dict["pix"][0]["txid"],
            "655dfdb1a4514b8fbb58254b958913fb",
        )
        self.assertEqual(
            resposta_sol_cob_imediata_dict["pix"][0]["valor"],
            "110.00",
        )
        self.assertEqual(
            resposta_sol_cob_imediata_dict["pix"][0]["devolucoes"][0]["id"],
            "123ABC",
        )
        self.assertEqual(
            resposta_sol_cob_imediata_dict["pix"][0]["devolucoes"][0]["rtrId"],
            "Dxxxxxxxx202009091221kkkkkkkkkkk",
        )
        self.assertEqual(
            resposta_sol_cob_imediata_dict["pix"][0]["devolucoes"][0]["horario"][
                "solicitacao"
            ],
            "2020-09-09T20:15:00.358Z",
        )
        self.assertEqual(
            resposta_sol_cob_imediata_dict["pix"][0]["devolucoes"][0]["status"],
            "EM_PROCESSAMENTO",
        )


if __name__ == "__main__":
    unittest.main()
