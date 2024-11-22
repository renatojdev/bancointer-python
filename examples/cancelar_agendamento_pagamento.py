# cancelar_agendamento_pagamento.py

import sys

from decouple import config

from bancointer.banking.pagamento.cancela_agendamento_pagamento import (
    CancelaAgendamentoPagamento,
)
from bancointer.utils.environment import Environment

dir_base_ssl = config("SSL_DIR_BASE")
cert = (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2"))
client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")
conta_corrente = config("X_INTER_CONTA_CORRENTE")

# Environment SANDBOX or PRODUCTION
app_env_name = config("APP_ENV")
env = Environment.get_environment_by_value(app_env_name.upper())

transaction_code = "72324a7f-0703-431f-a85a-97794f94e360"

args = sys.argv

request_code_param = None
if len(sys.argv) > 1:
    request_code_param = args[1]

if request_code_param is not None:
    transaction_code = request_code_param

cancela_agendamento_pagamento = CancelaAgendamentoPagamento(
    env, client_id, client_secret, cert, conta_corrente
)

response = cancela_agendamento_pagamento.cancelar(transaction_code)

print(f"Response from API: {response}")
