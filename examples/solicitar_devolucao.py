# solicitar_devolucao.py


from decouple import config

from bancointer.pix.pix.solicita_devolucao import SolicitaDevolucao
from bancointer.utils.environment import Environment

dir_base_ssl = config("SSL_DIR_BASE")
cert = (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2"))
client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")
conta_corrente = config("X_INTER_CONTA_CORRENTE")

# Environment SANDBOX or PRODUCTION
app_env_name = config("APP_ENV")
env = Environment.get_environment_by_value(app_env_name.upper())

sol_devolucao = SolicitaDevolucao(env, client_id, client_secret, cert, conta_corrente)

response = sol_devolucao.solicitar("E00416968202412061443oJmW8hQsV3b", "11", "20.00")

print(f"Response from API: {response}")
