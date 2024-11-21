# resposta_requisicao_pagamento_darf.py


from dataclasses import dataclass, asdict
from typing import Any, Dict

from bancointer.banking.models.tipo_retorno import TipoRetorno


@dataclass()
class RespostaRequisicaoPagamentoDarf(object):
    """Classe requisicao para incluir pagamentos com codigo de barras"""

    autenticacao: str
    dataPagamento: str
    tipoRetorno: TipoRetorno
    codigoSolicitacao: str
    quantidadeAprovadores: int = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}
