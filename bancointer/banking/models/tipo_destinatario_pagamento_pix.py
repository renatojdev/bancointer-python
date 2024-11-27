# tipo_destinatario_pagamento_pix.py

from enum import Enum


class TipoDestinatarioPagamentoPix(Enum):

    CHAVE = "CHAVE"
    DADOS_BANCARIOS = "DADOS_BANCARIOS"
    PIX_COPIA_E_COLA = "PIX_COPIA_E_COLA"
