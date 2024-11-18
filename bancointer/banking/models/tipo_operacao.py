# tipo_operacao.py

from enum import Enum


class TipoOperacao(Enum):
    D = "DEBITO"  # saida
    C = "CREDITO"  # entrada
