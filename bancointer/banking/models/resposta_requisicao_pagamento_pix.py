# resposta_requisicao_pagamento_pix.py

from dataclasses import dataclass, asdict
from typing import Any, Dict

from bancointer.banking.models.tipo_retorno_pagamento_pix import TipoRetornoPagamentoPix


@dataclass()
class RespostaRequisicaoPagamentoPix(object):
    """Classe requisicao para incluir pagamentos com codigo de barras"""

    tipoRetorno: TipoRetornoPagamentoPix
    codigoSolicitacao: str
    dataPagamento: str
    dataOperacao: str

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}
