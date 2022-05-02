from bancointer.bancointer import BancoInter
from decouple import config

API_VERSION = 2
dir_base_ssl = config("SSL_DIR_BASE")

cert = (dir_base_ssl + config("PUBLIC_KEY_V"+ str(API_VERSION)), dir_base_ssl + config("PRIVATE_KEY_V"+ str(API_VERSION)))

if API_VERSION == 1:
    bi = BancoInter(config("CPFCNPJ_BENEF"), config("X-INTER-CONTA-CORRENTE"), cert)

    bi.set_api_version(API_VERSION)

    pagador = {
        "cnpjCpf": "19103298000",
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
        dataEmissao="2022-05-02",
        dataVencimento="2022-05-09",
        seuNumero="00001",
        valorNominal=5.9,
    )

    print(reponse)

elif API_VERSION == 2:
    bi.set_client_id(value=config("CLIENT_ID"))
    bi.set_client_secret(value=config("CLIENT_SECRET"))
    bi.set_base_url(value=config("API_URL_COBRA_V2"))
    bi.set_base_url_token(value=config("API_URL_TOKEN_V2"))

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
        dataEmissao="2022-05-02",
        dataVencimento="2022-05-09",
        seuNumero="00001",
        valorNominal=5,
    )

    print(reponse)
