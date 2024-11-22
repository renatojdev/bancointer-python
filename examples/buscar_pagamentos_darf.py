# buscar_pagamentos_darf.py


from decouple import config

from bancointer.banking.pagamento.busca_pagamento_darf import BuscaPagamentoDarf
from bancointer.utils.environment import Environment

dir_base_ssl = config("SSL_DIR_BASE")
cert = (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2"))
client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")
conta_corrente = config("X_INTER_CONTA_CORRENTE")

# Environment SANDBOX or PRODUCTION
app_env_name = config("APP_ENV")
env = Environment.get_environment_by_value(app_env_name.upper())

busca_pagamento_darf = BuscaPagamentoDarf(
    env, client_id, client_secret, cert, conta_corrente
)

response = busca_pagamento_darf.buscar(
    {
        # "codigoSolicitacao": "9e392015-c8a0-45c6-9dee-054f33e90ffa",
        "codigoReceita": "0220",
        "dataInicio": "2024-11-01",
        "dataFim": "2024-11-22",
    }
)

print(f"Response from API: {response}")
