# incluir_pagamento_darf.py


from bancointer.banking.models.requisicao_pagamento_darf import RequisicaoPagamentoDarf
from decouple import config

from bancointer.banking.pagamento.inclui_pagamento_darf import IncluiPagamentoDarf
from bancointer.utils.environment import Environment

dir_base_ssl = config("SSL_DIR_BASE")
cert = (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2"))
client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")
conta_corrente = config("X_INTER_CONTA_CORRENTE")

# Environment SANDBOX or PRODUCTION
app_env_name = config("APP_ENV")
env = Environment.get_environment_by_value(app_env_name.upper())

# object request
requisicao_pagamento_darf = RequisicaoPagamentoDarf(
    "90022400664",
    "0220",
    "2024-11-30",
    "Pagamento DARF Janeiro",
    "Minha Empresa",
    "2024-10-31",
    47.14,
    "13609400849201739",
)

inclui_pagamento_darf = IncluiPagamentoDarf(
    env, client_id, client_secret, cert, conta_corrente
)

response = inclui_pagamento_darf.incluir(requisicao_pagamento_darf)

print(f"Response from API: {response}")
