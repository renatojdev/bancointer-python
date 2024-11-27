# incluir_pagamento_pix.py


from bancointer.banking.models.destinatario_pagamento_pix import (
    DestinatarioPagamentoPix,
)
from bancointer.banking.models.instituicao_financeira import InstituicaoFinanceira
from bancointer.banking.models.requisicao_pagamento_pix import RequisicaoPagamentoPix
from bancointer.banking.models.tipo_conta import TipoConta
from bancointer.banking.models.tipo_destinatario_pagamento_pix import (
    TipoDestinatarioPagamentoPix,
)
from decouple import config

from bancointer.banking.pix_pagamento.inclui_pagamento_pix import IncluiPagamentoPix
from bancointer.utils.environment import Environment

dir_base_ssl = config("SSL_DIR_BASE")
cert = (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2"))
client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")
conta_corrente = config("X_INTER_CONTA_CORRENTE")

# Environment SANDBOX or PRODUCTION
app_env_name = config("APP_ENV")
env = Environment.get_environment_by_value(app_env_name.upper())

# Destinatario Pagamento via PIX  - Chave
TEL = "+5541943339900"
EMAIL = "chave@email.com"
EVP = "123e4567-e12b-12d1-a456-426655440000"
destinatario_chave = DestinatarioPagamentoPix(
    TipoDestinatarioPagamentoPix.CHAVE, chave=TEL
)

# Destinatario Pagamento via PIX - Dados Bancarios
destinatario_dados_bancarios = DestinatarioPagamentoPix(
    TipoDestinatarioPagamentoPix.DADOS_BANCARIOS,
    contaCorrente="4321",
    tipoConta=TipoConta.CONTA_PAGAMENTO,
    cpfCnpj="42342342312",
    agencia="0001",
    nome="João Fonseca",
    instituicaoFinanceira=InstituicaoFinanceira(
        "28326000"  # ISPB (8 dig): 28326000 - C6Bank
    ),
)

# Destinatario Pagamento via PIX - Pix copia e cola
destinatario_pix_copia_e_cola = DestinatarioPagamentoPix(
    TipoDestinatarioPagamentoPix.PIX_COPIA_E_COLA, pixCopiaECola="pixCopiaEColaString"
)

requisicao_pagamento_pix = RequisicaoPagamentoPix(46.17, destinatario_chave)

inclui_pagamento_pix = IncluiPagamentoPix(
    env,
    client_id,
    client_secret,
    cert,
    conta_corrente,
    "6ee857c9-e147-4a0f-a85a-cca1b39d8e1b",
)

response = inclui_pagamento_pix.incluir(requisicao_pagamento_pix)

print(f"Response from API: {response}")
