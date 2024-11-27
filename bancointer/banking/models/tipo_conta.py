# tipo_conta.py

from enum import Enum


class TipoConta(Enum):
    CONTA_CORRENTE = "CONTA_CORRENTE"
    CONTA_POUPANCA = "CONTA_POUPANCA"
    CONTA_SALARIO = "CONTA_SALARIO"
    CONTA_PAGAMENTO = "CONTA_PAGAMENTO"
