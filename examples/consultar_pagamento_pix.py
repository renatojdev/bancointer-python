# consultar_pagamento_pix.py


from decouple import config

from bancointer.banking.pix_pagamento.consulta_pagamento_pix import ConsultaPagamentoPix
from bancointer.utils.environment import Environment

dir_base_ssl = config("SSL_DIR_BASE")
cert = (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2"))
client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")
conta_corrente = config("X_INTER_CONTA_CORRENTE")

# Environment SANDBOX or PRODUCTION
app_env_name = config("APP_ENV")
env = Environment.get_environment_by_value(app_env_name.upper())

consulta_pagamento_pix = ConsultaPagamentoPix(
    env, client_id, client_secret, cert, conta_corrente
)

response = consulta_pagamento_pix.consultar("ad930c2f-3d68-927e-23f4-98fe41de18fe")

print(f"Response from API: {response}")
