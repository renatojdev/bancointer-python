# requisicao_pagamento_darf.py

from dataclasses import dataclass, asdict
from numbers import Number
from typing import Any, Dict

from bancointer.utils.bancointer_validations import BancoInterValidations
from bancointer.utils.exceptions import Erro, BancoInterException


@dataclass()
class RequisicaoPagamentoDarf(object):
    """Classe requisicao para incluir pagamentos DARF"""

    cnpjCpf: str  # req
    codigoReceita: str  # req string = 4 characters
    dataVencimento: str  # req string <date>
    descricao: str  # req <= 1000 characters
    nomeEmpresa: str  # req <= 100 characters
    periodoApuracao: str  # req <date>
    valorPrincipal: Number  # req number
    referencia: str  # req string <= 30 characters  [0-9]
    telefoneEmpresa: str = None  # string <= 50 characters
    valorMulta: Number = None  # number
    valorJuros: Number = None  # number

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""

        # validations
        required_fields = [
            "cnpjCpf",
            "codigoReceita",
            "dataVencimento",
            "descricao",
            "nomeEmpresa",
            "periodoApuracao",
            "valorPrincipal",
            "referencia",
        ]
        for campo in required_fields:
            campo_value = getattr(self, campo)
            if not hasattr(self, campo) or campo_value is None:
                erro = Erro(
                    404, f"O atributo 'requisicaoPagamentoDarf.{campo}' é obrigatório."
                )
                raise BancoInterException("Erro de validação", erro)

        if not BancoInterValidations.validate_cpf_cnpj(self.cnpjCpf):
            erro = Erro(
                502,
                f"O atributo 'requisicaoPagamentoDarf.cnpjCpf' é inválido. (string [11 .. 20] characters)",
            )
            raise BancoInterException("Erro de validação", erro)

        if not BancoInterValidations.validate_string_range(self.codigoReceita, 4, 4):
            erro = Erro(
                502,
                f"O atributo 'requisicaoPagamentoDarf.codigoReceita' é inválido. (=4 characters)",
            )
            raise BancoInterException("Erro de validação", erro)

        if not BancoInterValidations.validate_date(self.dataVencimento):
            erro = Erro(
                502,
                f"O atributo 'requisicaoPagamentoDarf.dataVencimento' é inválido. Formato aceito: YYYY-MM-DD",
            )
            raise BancoInterException("", erro)

        if not BancoInterValidations.validate_string_range(
            self.descricao, max_chars=1000
        ):
            erro = Erro(
                502,
                f"O atributo 'requisicaoPagamentoDarf.descricao' é inválido. Formato aceito: (<= 1000 characters)",
            )
            raise BancoInterException("", erro)

        if not BancoInterValidations.validate_string_range(
            self.nomeEmpresa, max_chars=100
        ):
            erro = Erro(
                502,
                f"O atributo 'requisicaoPagamentoDarf.nomeEmpresa' é inválido. Formato aceito: (<= 100 characters)",
            )
            raise BancoInterException("", erro)

        if not BancoInterValidations.validate_date(self.periodoApuracao):
            erro = Erro(
                502,
                f"O atributo 'requisicaoPagamentoDarf.periodoApuracao' é inválido. Formato aceito: YYYY-MM-DD",
            )
            raise BancoInterException("", erro)

        if not BancoInterValidations.is_valid_valor_nominal(self.valorPrincipal):
            erro = Erro(
                502,
                f"O atributo 'requisicaoPagamentoDarf.valorPrincipal' é inválido. Formato aceito: (de 2.5 até 99999999.99)",
            )
            raise BancoInterException("", erro)

        if not BancoInterValidations.validate_string_range(
            self.referencia, max_chars=30
        ):
            erro = Erro(
                502,
                f"O atributo 'requisicaoPagamentoDarf.referencia' é inválido. Formato aceito: (<= 30 characters)",
            )
            raise BancoInterException("", erro)

        if (
            self.telefoneEmpresa is not None
            and not BancoInterValidations.validate_string_range(
                self.telefoneEmpresa, max_chars=50
            )
        ):
            erro = Erro(
                502,
                f"O atributo 'requisicaoPagamentoDarf.telefoneEmpresa' é inválido. Formato aceito: (<= 50 characters)",
            )
            raise BancoInterException("", erro)

        return {k: v for k, v in asdict(self).items() if v is not None}
