# requisicao_pagamento.py

from dataclasses import dataclass, asdict
from typing import Any, Dict

from bancointer.utils.bancointer_validations import BancoInterValidations
from bancointer.utils.exceptions import Erro, BancoInterException


@dataclass()
class RequisicaoPagamento(object):
    """Classe requisicao para incluir pagamentos com codigo de barras"""

    codBarraLinhaDigitavel: str  # req
    valorPagar: float  # req
    dataVencimento: str  # req
    cpfCnpjBeneficiario: str = None
    dataPagamento: str = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""

        # validations
        required_fields = ["codBarraLinhaDigitavel", "valorPagar", "dataVencimento"]
        for campo in required_fields:
            campo_value = getattr(self, campo)
            if not hasattr(self, campo) or campo_value is None:
                erro = Erro(
                    404, f"O atributo 'requisicaoPagamento.{campo}' é obrigatório."
                )
                raise BancoInterException("Erro de validação", erro)

        if not BancoInterValidations.is_valid_valor_nominal(self.valorPagar):
            erro = Erro(
                502,
                f"O atributo 'requisicaoPagamento.valorPagar' é inválido. (de 2.5 até 99999999.99)",
            )
            raise BancoInterException("Erro de validação", erro)

        if not BancoInterValidations.validate_date(self.dataVencimento):
            erro = Erro(
                502,
                f"O atributo 'requisicaoPagamento.dataVencimento' é inválido. Formato aceito: YYYY-MM-DD",
            )
            raise BancoInterException("", erro)

        if not BancoInterValidations.validate_cpf_cnpj(self.cpfCnpjBeneficiario):
            erro = Erro(
                502,
                f"O atributo 'requisicaoPagamento.cpfCnpjBeneficiario' é inválido. Formato aceito: 12345678912345",
            )
            raise BancoInterException("", erro)

        return {k: v for k, v in asdict(self).items() if v is not None}
