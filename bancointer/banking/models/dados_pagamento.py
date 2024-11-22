# dados_pagamento.py


from dataclasses import asdict, dataclass
from typing import Dict, Any

from bancointer.banking.models.status_pagamento import StatusPagamento


@dataclass()
class DadosPagamento(object):

    codigoTransacao: str
    codigoBarra: str
    tipo: str
    dataVencimentoDigitada: str
    dataVencimentoTitulo: str
    dataInclusao: str
    dataPagamento: str
    valorPago: float
    valorNominal: float
    statusPagamento: StatusPagamento
    cpfCnpjBeneficiario: str
    nomeBeneficiario: str
    autenticacao: str
    aprovacoesNecessarias: int = None
    aprovacoesRealizadas: int = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}
