# requisicao_pagamento_pix.py


from dataclasses import dataclass, asdict, field
from typing import Any, Dict

from bancointer.banking.models.destinatario_pagamento_pix import (
    DestinatarioPagamentoPix,
)
from bancointer.utils.bancointer_validations import BancoInterValidations
from bancointer.utils.exceptions import Erro, BancoInterException


@dataclass()
class RequisicaoPagamentoPix(object):
    """Classe requisicao para incluir pagamentos com codigo de barras"""

    valor: float  # req
    destinatario: DestinatarioPagamentoPix  # req
    dataPagamento: str = None
    descricao: str = None  # <= 140 characters

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""

        # validations
        required_fields = ["valor", "destinatario"]
        for campo in required_fields:
            campo_value = getattr(self, campo)
            if not hasattr(self, campo) or campo_value is None:
                erro = Erro(
                    404, f"O atributo 'requisicaoPagamentoPix.{campo}' é obrigatório."
                )
                raise BancoInterException("Erro de validação", erro)

        if not BancoInterValidations.is_valid_valor_nominal(self.valor):
            erro = Erro(
                502,
                f"O atributo 'requisicaoPagamentoPix.valor' é inválido. (de 2.5 até 99999999.99)",
            )
            raise BancoInterException("Erro de validação", erro)

        requisicao_pagamento_pix_dict = {
            k: v for k, v in asdict(self).items() if v is not None
        }
        requisicao_pagamento_pix_dict["destinatario"] = self.destinatario.to_dict()
        return requisicao_pagamento_pix_dict
