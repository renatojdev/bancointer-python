# resposta_consulta_pagamento_pix.py


from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List

from bancointer.banking.models.status_transaco_pix import StatusTransacaoPix
from bancointer.banking.models.transacao_pix import TransacaoPix


@dataclass()
class RespostaConsultaPagamentoPix(object):
    """Classe resposta da busca de pagamentos."""

    transacaoPix: TransacaoPix
    historico: List[Dict[StatusTransacaoPix, str]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}
