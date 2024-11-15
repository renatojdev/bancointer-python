# emitir_cobranca.py

from datetime import datetime, timedelta

from bancointer.cobranca_v3.cobranca import EmiteCobranca
from bancointer.cobranca_v3.models.solicitacao_emitir_cobranca import (
    SolicitacaoEmitirCobranca,
)

from bancointer.cobranca_v3.models.cobranca import Cobranca
from bancointer.cobranca_v3.models.desconto import Desconto
from bancointer.cobranca_v3.models.message import Message
from bancointer.cobranca_v3.models.mora import Mora
from bancointer.cobranca_v3.models.multa import Multa
from bancointer.cobranca_v3.models.pessoa import Pessoa
from bancointer.cobranca_v3.models.tipo_pessoa import PersonType
from decouple import config

dir_base_ssl = config("SSL_DIR_BASE")
cert = (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2"))
client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")

# Due Date
data_act = datetime.now()
# Add 10 days
new_date = data_act + timedelta(days=10)
due_date = new_date.strftime("%Y-%m-%d")

payer = Pessoa(
    "9" * 11,  # valido
    PersonType.FISICA,
    "NOME DO PAGADOR",
    "ENDERECO DO PAGADOR",
    "CIDADE DO PAGADOR",
    "PR",
    "80030000",
)  # OU FISICA
# Pagador

discount = Desconto("PERCENTUALDATAINFORMADA", 0, 1.2, 2)
multa = Multa("VALORFIXO", 0, 100)
mora = Mora("TAXAMENSAL", 0, 4.5)
message = Message("message 1", "message 2", "message 3", "", "message 5")

# Beneficiario final, mesmo que o pagador
beneficiario_final = Pessoa(
    "12345678901",
    PersonType.FISICA,
    "Nome do beneficiário",
    "Avenida Brasil, 1200",
    "Belo Horizonte",
    "MG",
    "30110000",
)

cobranca = Cobranca.criar_sobranca_simples("0001", 2.5, due_date, payer)
cobranca.multa = multa
cobranca.desconto = discount

sol_new_cobranca = SolicitacaoEmitirCobranca(cobranca)

emite_cobranca = EmiteCobranca(client_id, client_secret, cert)
resposta = emite_cobranca.emitir(sol_new_cobranca)
print(f"Response from API: {resposta}")
