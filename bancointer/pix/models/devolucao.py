# devolucao.py


from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, Any

from bancointer.pix.models.horario_devolucao import HorarioDevolucao


class NaturezaDevolucao(Enum):
    ORIGINAL = "ORIGINAL"
    RETIRADA = "RETIRADA"


@dataclass  # Devolucao Pix
class Devolucao(object):
    id: str  # req string (Id da Devolução) [a-zA-Z0-9]{1,35}
    rtrId: str  # req string (RtrId) = 32 characters [a-zA-Z0-9]{32}
    valor: str  # req string (Valor a devolver.) \d{1,10}\.\d{2}
    horario: HorarioDevolucao  # req
    status: str  #  req Enum: "EM_PROCESSAMENTO" "DEVOLVIDO" "NAO_REALIZADO"
    motivo: str = None  # string (Descrição do status.) <= 140 characters
    natureza: NaturezaDevolucao = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}
