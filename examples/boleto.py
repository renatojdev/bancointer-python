from bancointer.bancointer import BancoInter
from decouple import config

dir_base_ssl = config("SSL_DIR_BASE")

dir_base_ssl = config("SSL_DIR_BASE")

bi = BancoInter(
    config("API_URL_COBRA_V2"),
    config("API_URL_TOKEN_V2"),
    config("CLIENT_ID"),
    config("CLIENT_SECRET"),
    (
        dir_base_ssl + config("PUBLIC_KEY_V2"),
        dir_base_ssl + config("PRIVATE_KEY_V2")
    )
)

pagador = {
    "cpfCnpj": "19103298000",
    "nome": "Nome do Pagador",
    "email": "pagador@gmail.com",
    "telefone": "999999999",
    "cep": "99999999",
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

reponse = bi.boleto(
    pagador=pagador,
    mensagem=mensagem,
    dataEmissao="2022-05-03",
    dataVencimento="2022-05-10",
    seuNumero="00001",
    valorNominal=5,
)

print(reponse)
