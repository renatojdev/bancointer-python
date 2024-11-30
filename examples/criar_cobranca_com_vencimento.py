# criar_cobranca_com_vencimento.py


from decouple import config

from bancointer.pix.cobv.cria_cobranca_com_vencimento import CriaCobrancaComVencimento
from bancointer.pix.models.calendario import Calendario
from bancointer.pix.models.devedor_recebedor_cobranca import DevedorRecebedorCobranca
from bancointer.pix.models.info_adicional_cobranca_imediata import (
    InfoAdicionalCobrancaImediata,
)
from bancointer.pix.models.solicitacao_cobranca import (
    SolicitacaoCobranca,
)
from bancointer.pix.models.valor_cobranca_imediata import (
    ValorCobrancaImediata,
    Retirada,
    SaqueOuTroco,
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

# Create immediate cob
calendario = Calendario(dataDeVencimento="2024-12-31")  # expiracao default: 3600

devedor_cobranca_imediata = DevedorRecebedorCobranca("João da Silva", cpf="12345678901")

retirada = Retirada(saque=SaqueOuTroco("20.00", "AGPSS", "12345678"))

valor_cobranca_imediata = ValorCobrancaImediata("46.17", retirada)

info_adic_cobranca_imediata = InfoAdicionalCobrancaImediata(
    "Campo 1", "Informação Adicional1 do PSP-Recebedor"
)

solicitacao_cob = SolicitacaoCobranca(
    calendario,
    valor_cobranca_imediata,
    "+5551983334490",
    devedor_cobranca_imediata,
    solicitacaoPagador="Serviço realizado.",
    infoAdicionais=info_adic_cobranca_imediata,
)

cria_cobranca_com_vencimento = CriaCobrancaComVencimento(
    env, client_id, client_secret, cert, conta_corrente
)

response = cria_cobranca_com_vencimento.criar(
    solicitacao_cob, "OA3uMSCRI4sgWBaifS6mP2Fnrv8h6"
)

print(f"Response from API: {response}")
