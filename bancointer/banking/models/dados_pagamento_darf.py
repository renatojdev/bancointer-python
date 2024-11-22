# dados_pagamento_darf.py


from dataclasses import asdict, dataclass
from typing import Dict, Any

from bancointer.banking.models.status_pagamento import StatusPagamento


@dataclass()
class DadosPagamentoDarf(object):

    codigoSolicitacao: str
    tipoDarf: str
    valor: float
    valorMulta: float
    valorJuros: float
    valorTotal: float
    tipo: str
    periodoApuracao: str
    dataPagamento: str
    referencia: str
    dataVencimento: str
    codigoReceita: str
    statusPagamento: StatusPagamento
    dataInclusao: str
    cnpjCpf: str
    aprovacoesNecessarias: int = None
    aprovacoesRealizadas: int = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}
