# resposta_busca_pagamento_darf.py


from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List

from bancointer.banking.models.dados_pagamento_darf import DadosPagamentoDarf


@dataclass()
class RespostaBuscaPagamentoDarf(object):
    """Classe resposta da busca de pagamentos."""

    pagamentos: List[Dict[str, DadosPagamentoDarf]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}
