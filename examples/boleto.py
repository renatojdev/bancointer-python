# boleto.py

from bancointer.bancointer import BancoInter
from decouple import config
from datetime import datetime, timedelta


# Due Date
data_act = datetime.now()
# Add 10 days
new_date = data_act + timedelta(days=10)
due_date = new_date.strftime("%Y-%m-%d")


dir_base_ssl = config("SSL_DIR_BASE")

bi = BancoInter(
    config("API_SBX_COBRA_V3"),
    config("API_SBX_TOKEN_V2"),
    config("CLIENT_ID"),
    config("CLIENT_SECRET"),
    (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2")),
)

pagador = {
    "cpfCnpj": "19103298000",
    "nome": "Nome do Pagador",
    "email": "pagador@gmail.com",
    "telefone": "999999999",
    "cep": "80030000",
    "numero": "00",
    "complemento": "proximo ao pagador",
    "bairro": "Bairro do Pagador",
    "cidade": "Cidade do Pagador",
    "uf": "PR",
    "endereco": "Logradouro do Pagador",
    "ddd": "99",
    "tipoPessoa": "FISICA",
}

mensagem = {
    "linha1": "mensagem da linha1",
    "linha2": "mensagem da linha2",
    "linha3": "mensagem da linha3",
    "linha4": "mensagem da linha4",
    "linha5": "mensagem da linha5",
}

# Ver emitir_cobranca.py

reponse = bi.boleto(
    pagador=pagador,
    mensagem=mensagem,
    dataEmissao=None,
    dataVencimento=due_date,
    seuNumero="00001",
    valorNominal=5,
)

print(reponse)
