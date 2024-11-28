# criar_cobranca_imediata.py


from decouple import config

from bancointer.pix.cob.cria_cobranca_imediata import CriaCobrancaImediata
from bancointer.pix.models.calendario import Calendario
from bancointer.pix.models.devedor_cobranca_imediata import DevedorCobrancaImediata
from bancointer.pix.models.info_adicional_cobranca_imediata import (
    InfoAdicionalCobrancaImediata,
)
from bancointer.pix.models.solicitacao_cobranca_imediata import (
    SolicitacaoCobrancaImediata,
)
from bancointer.pix.models.valor_cobranca_imediata import ValorCobrancaImediata
from bancointer.utils.environment import Environment

dir_base_ssl = config("SSL_DIR_BASE")
cert = (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2"))
client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")
conta_corrente = config("X_INTER_CONTA_CORRENTE")

# Environment SANDBOX or PRODUCTION
app_env_name = config("APP_ENV")
env = Environment.get_environment_by_value(app_env_name.upper())

# Create immediate cob
calendario = Calendario(3600)

devedor_cobranca_imediata = DevedorCobrancaImediata("João da Silva", cpf="12345678901")

valor_cobranca_imediata = ValorCobrancaImediata("46.17")

info_adic_cobranca_imediata = InfoAdicionalCobrancaImediata(
    "Campo 1", "Informação Adicional1 do PSP-Recebedor"
)

solicitacao_cob_imediata = SolicitacaoCobrancaImediata(
    calendario,
    valor_cobranca_imediata,
    "+5551983334490",
    devedor_cobranca_imediata,
    solicitacaoPagador="Serviço realizado.",
    infoAdicionais=info_adic_cobranca_imediata,
)

cria_cobranca_imediata = CriaCobrancaImediata(
    env, client_id, client_secret, cert, conta_corrente
)

response = cria_cobranca_imediata.criar(solicitacao_cob_imediata)

print(f"Response from API: {response}")
