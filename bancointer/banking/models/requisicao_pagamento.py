# requisicao_pagamento.py

from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass()
class RequisicaoPagamento(object):
    """Classe requisicao para incluir pagamentos com codigo de barras"""

    codBarraLinhaDigitavel: str  # req
    valorPagar: str  # req
    dataVencimento: str  # req
    cpfCnpjBeneficiario: str
    dataPagamento: str = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}
