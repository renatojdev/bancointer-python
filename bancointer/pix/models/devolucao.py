# devolucao.py


from dataclasses import dataclass
from bancointer.pix.models.horario_devolucao import HorarioDevolucao


@dataclass  # Devolucao Pix
class Devolucao(object):
    id: str  # req string (Id da Devolução) [a-zA-Z0-9]{1,35}
    rtrId: str  # req string (RtrId) = 32 characters [a-zA-Z0-9]{32}
    valor: str  # req string (Valor a devolver.) \d{1,10}\.\d{2}
    horario: HorarioDevolucao  # req
    status: str  #  req Enum: "EM_PROCESSAMENTO" "DEVOLVIDO" "NAO_REALIZADO"
    motivo: str = None  # string (Descrição do status.) <= 140 characters
