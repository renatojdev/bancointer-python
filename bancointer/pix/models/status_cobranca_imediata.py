# status_cobranca_imediata.py


from enum import Enum


class StatusCobrancaImediata(Enum):
    ATIVA = "ATIVA"
    CONCLUIDA = "CONCLUIDA"
    REMOVIDA_PELO_USUARIO_RECEBEDOR = "REMOVIDA_PELO_USUARIO_RECEBEDOR"
    REMOVIDA_PELO_PSP = "REMOVIDA_PELO_PSP"
