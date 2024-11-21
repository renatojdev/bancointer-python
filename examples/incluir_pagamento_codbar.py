# incluir_pagamento_codbar.py


from bancointer.banking.models.requisicao_pagamento import RequisicaoPagamento
from bancointer.banking.pagamento.inclui_pagamento_codbar import IncluiPagamentoCodBar
from decouple import config

from bancointer.utils.environment import Environment

dir_base_ssl = config("SSL_DIR_BASE")
cert = (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2"))
client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")
conta_corrente = config("X_INTER_CONTA_CORRENTE")

# Environment SANDBOX or PRODUCTION
app_env_name = config("APP_ENV")
env = Environment.get_environment_by_value(app_env_name.upper())

# payment info
CODBAR = "03395988500000666539201493990000372830030102"
VALOR = 2.5
VENCIMENTO = "2024-11-21"
CPF_CNPJ_BENEF = "9" * 14
DATA_PAGAMENTO = VENCIMENTO

requisicao_pagamento = RequisicaoPagamento(
    CODBAR, VALOR, VENCIMENTO, CPF_CNPJ_BENEF, DATA_PAGAMENTO
)

inclui_pagamento = IncluiPagamentoCodBar(
    env, client_id, client_secret, cert, conta_corrente
)

response = inclui_pagamento.incluir(requisicao_pagamento)

print(f"Response from API: {response}")
