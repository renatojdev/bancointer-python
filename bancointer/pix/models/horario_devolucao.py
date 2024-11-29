# horario_devolucao.py


from dataclasses import dataclass


@dataclass
class HorarioDevolucao(object):
    solicitacao: str  # string <date-time> (Horário da solicitacao)
    liquidacao: str  # string <date-time> (Horário de liquidacao)
