from bancointer.bancointer import BancoInter
from decouple import config


API_VERSION = 2
dir_base_ssl = config("SSL_DIR_BASE")

cert = (dir_base_ssl + config("PUBLIC_KEY_V"+ str(API_VERSION)), dir_base_ssl + config("PRIVATE_KEY_V"+ str(API_VERSION)))

bi = BancoInter(config("CPFCNPJ_BENEF"), config("X-INTER-CONTA-CORRENTE"), cert)

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

if API_VERSION == 1:
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

MULTA = {"codigoMulta": "PERCENTUAL", "valor": 0, "taxa": 2.0, "data": "2022-05-12"}

MORA = {"codigoMora": "TAXAMENSAL", "valor": 0, "taxa": 1.0, "data": "2022-05-12"}

bi.set_multa(multa=MULTA)

bi.set_mora(mora=MORA)

reponse = bi.boleto(
    pagador=pagador,
    mensagem=mensagem,
    dataEmissao="2022-05-02",
    dataVencimento="2022-05-11",
    seuNumero="00001",
    valorNominal=9.9,
)

print(reponse)
