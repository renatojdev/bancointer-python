# buscar_pagamentos.py


from decouple import config

from bancointer.banking.pagamento.busca_pagamento import BuscaPagamento
from bancointer.utils.environment import Environment

dir_base_ssl = config("SSL_DIR_BASE")
cert = (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2"))
client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")
conta_corrente = config("X_INTER_CONTA_CORRENTE")

# Environment SANDBOX or PRODUCTION
app_env_name = config("APP_ENV")
env = Environment.get_environment_by_value(app_env_name.upper())

busca_pagamento = BuscaPagamento(env, client_id, client_secret, cert, conta_corrente)

response = busca_pagamento.buscar(
    {
        # "codBarraLinhaDigitavel": "03395988500000666539201493990000372830030102",
        # "codigoTransacao": "ac72024e-6961-44ff-9f3a-bbc722c869f1",
        "dataInicio": "2024-11-01",
        "dataFim": "2024-11-22",
        "filtrarDataPor": "INCLUSAO",  #  Enum: "INCLUSAO" "PAGAMENTO" "VENCIMENTO"
    }
)

print(f"Response from API: {response}")
