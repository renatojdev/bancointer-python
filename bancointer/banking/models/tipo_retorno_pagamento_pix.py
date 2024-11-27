# tipo_retorno_pagamento_pix.py


from enum import Enum


class TipoRetornoPagamentoPix(Enum):

    APROVACAO = "APROVACAO"
    PROCESSADO = "PROCESSADO"
    AGENDADO = "AGENDADO"
