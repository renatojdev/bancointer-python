# requisicao_pagamento.py

from dataclasses import dataclass, asdict
from typing import Any, Dict

from bancointer.banking.models.status_pagamento import StatusPagamento


@dataclass()
class RespostaRequisicaoPagamento(object):
    """Classe requisicao para incluir pagamentos com codigo de barras"""

    quantidadeAprovadores: int
    statusPagamento: StatusPagamento  # req
    codigoTransacao: str
    dataAgendamento: str = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}
