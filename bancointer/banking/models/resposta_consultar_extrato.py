# resposta_consultar_extrato.py

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List

from bancointer.banking.models.transacao_simples import TransacaoSimples


@dataclass
class RespostaConsultarExtrato(object):
    """
    Código Solicitação Nosso Número, atribuído automaticamente pelo banco na emissão do título.
    """

    transacoes: List[Dict[str, TransacaoSimples]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}
