# solicitacao_emitir_cobranca.py

import json

from bancointer.cobranca_v3.models import Cobranca
from bancointer.cobranca_v3.models import Desconto
from bancointer.cobranca_v3.models import Message
from bancointer.cobranca_v3.models import Mora
from bancointer.cobranca_v3.models import Multa
from bancointer.cobranca_v3.models import Pessoa


class SolicitacaoEmitirCobranca(object):
    def __init__(self, cobranca: Cobranca):
        self.cobranca: Cobranca = cobranca

    def to_dict(self):
        # Checks that all the necessary fields are present
        cobranca_dict = self.cobranca.to_dict()

        if self.cobranca.descontos is not None and len(self.cobranca.descontos) > 0:
            cobranca_dict["descontos"] = [
                desconto.to_dict() for desconto in self.cobranca.descontos
            ]
        if self.cobranca.multa:
            cobranca_dict["multa"] = self.cobranca.multa.to_dict()
        if self.cobranca.mora:
            cobranca_dict["mora"] = self.cobranca.mora.to_dict()
        if self.cobranca.beneficiarioFinal:
            cobranca_dict["beneficiarioFinal"] = (
                self.cobranca.beneficiarioFinal.to_dict()
            )

        return cobranca_dict

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(json_request):
        data = json.loads(json_request)
        pagador_data = data["pagador"]
        multa_data = None
        if "multa" in data:
            multa_data = data["multa"]
        mora_data = None
        if "mora" in data:
            mora_data = data["mora"]
        mensagem_data = data["mensagem"]
        beneficiario_final_data = {}
        if data["beneficiarioFinal"] is not None:
            beneficiario_final_data = data["beneficiarioFinal"]
        # Get dicts data
        pagador = Pessoa(**pagador_data)
        beneficiario_final = Pessoa(**beneficiario_final_data)

        sol_cobranca = Cobranca()
        sol_cobranca.seuNumero = data["seuNumero"]
        sol_cobranca.valorNominal = data["valorNominal"]
        sol_cobranca.dataVencimento = data["dataVencimento"]
        sol_cobranca.numDiasAgenda = data["numDiasAgenda"]
        sol_cobranca.pagador = pagador
        if "descontos" in data:
            sol_cobranca.descontos = [
                Desconto(**desconto) for desconto in data["descontos"]
            ]
        if multa_data:
            sol_cobranca.multa = Multa(**multa_data)
        if mora_data:
            sol_cobranca.mora = Mora(**mora_data)
        sol_cobranca.mensagem = (
            Message(**mensagem_data) if mensagem_data is not None else None
        )
        sol_cobranca.beneficiarioFinal = beneficiario_final

        return SolicitacaoEmitirCobranca(sol_cobranca)
