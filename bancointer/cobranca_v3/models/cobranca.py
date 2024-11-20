# cobranca.py

import json
from json import JSONEncoder
from numbers import Number

from bancointer.cobranca_v3.models.desconto import Desconto
from bancointer.cobranca_v3.models.message import Message
from bancointer.cobranca_v3.models.mora import Mora
from bancointer.cobranca_v3.models.multa import Multa
from bancointer.cobranca_v3.models.pessoa import Pessoa
from bancointer.utils.bancointer_validations import BancoInterValidations
from bancointer.utils.exceptions import Erro, BancoInterException


class Cobranca(object):

    def __init__(
        self,
        seuNumero: str = None,
        valorNominal: Number = None,
        dataEmissao: str = None,
        dataVencimento: str = None,
        numDiasAgenda: int = 60,
        pagador: Pessoa = None,
        desconto: Desconto = None,
        descontos: list[Desconto] = [],
        multa: Multa = None,
        mora: Mora = None,
        mensagem: Message = None,
        beneficiarioFinal: Pessoa = None,
        arquivada: bool = False,
        tipoCobranca: str = None,
        situacao: str = None,
        dataSituacao: str = None,
        valorTotalRecebido: str = None,
    ):
        self.seuNumero = seuNumero
        self.valorNominal = valorNominal
        self.dataEmissao = dataEmissao
        self.dataVencimento = dataVencimento
        self.numDiasAgenda = numDiasAgenda
        self.pagador = pagador
        self.desconto = desconto
        self.descontos = descontos
        self.multa = multa
        self.mora = mora
        self.mensagem = mensagem
        self.beneficiarioFinal = beneficiarioFinal
        self.arquivada = arquivada
        self.tipoCobranca = tipoCobranca
        self.situacao = situacao
        self.dataSituacao = dataSituacao
        self.valorTotalRecebido = valorTotalRecebido

    @classmethod
    def criar_sobranca_simples(cls, seuNumero, valorNominal, dataVencimento, pagador):
        return cls(seuNumero, valorNominal, None, dataVencimento, 60, pagador)

    def __eq__(self, other):
        if not isinstance(other, Cobranca):
            return NotImplemented
        return (
            self.seuNumero == other.seuNumero
            and self.dataEmissao == other.dataEmissao
            and self.dataVencimento == other.dataVencimento
            and self.valorNominal == other.valorNominal
        )

    def to_dict(self):
        # validations
        required_fields = ["seuNumero", "valorNominal", "dataVencimento", "pagador"]
        for campo in required_fields:
            campo_value = getattr(self, campo)
            if not hasattr(self, campo) or campo_value is None:
                erro = Erro(404, f"O atributo 'cobranca.{campo}' é obrigatório.")
                raise BancoInterException("", erro)

        if not BancoInterValidations.validate_string_range(
            self.seuNumero, max_chars=15
        ):
            erro = Erro(
                502,
                f"O atributo 'cobranca.seuNumero' é inválido. (de 1 a 15)",
            )
            raise BancoInterException("Erro de validação", erro)

        if not BancoInterValidations.is_valid_valor_nominal(self.valorNominal):
            erro = Erro(
                502,
                f"O atributo 'cobranca.valorNominal' é inválido. (de 2.5 até 99999999.99)",
            )
            raise BancoInterException("Erro de validação", erro)

        if not BancoInterValidations.validate_date(self.dataVencimento):
            erro = Erro(
                502,
                f"O atributo 'cobranca.dataVencimento' é inválido. Formato aceito: YYYY-MM-DD",
            )
            raise BancoInterException("", erro)

        if not BancoInterValidations.is_valid_num_dias_agenda(self.numDiasAgenda):
            erro = Erro(
                502, f"O atributo 'cobranca.numDiasAgenda' é inválido. (de 0 até 60)"
            )
            raise BancoInterException("", erro)

        result = {
            "seuNumero": self.seuNumero,
            "dataEmissao": self.dataEmissao,
            "dataVencimento": self.dataVencimento,
            "valorNominal": self.valorNominal,
            "numDiasAgenda": self.numDiasAgenda,
            "tipoCobranca": self.tipoCobranca,
            "situacao": self.situacao,
            "dataSituacao": self.situacao,
            "valorTotalRecebido": self.valorTotalRecebido,
            "arquivada": self.arquivada,
            "pagador": self.pagador.to_dict(),
        }

        if len(self.descontos) > 0:
            result["descontos"] = [desconto.to_dict() for desconto in self.descontos]
        if self.desconto:
            result["desconto"] = self.desconto.to_dict()
        if self.multa:
            result["multa"] = self.multa.to_dict()
        if self.mora:
            result["mora"] = self.mora.to_dict()
        if self.mensagem:
            result["mensagem"] = self.mensagem.to_dict()
        if self.beneficiarioFinal:
            result["beneficiarioFinal"] = self.beneficiarioFinal.to_dict()

        return result

    def to_json(self):
        return json.dumps(self, cls=CobrancaEncoder)

    @staticmethod
    def from_json(json_discount):
        data = json.loads(json_discount)
        return Cobranca(**data)


class CobrancaEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Cobranca):
            return o.to_dict()
        return super().default(o)
