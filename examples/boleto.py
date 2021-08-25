from bancointer.bancointer import BancoInter
from decouple import config


cert = (config("PUBLIC_KEY"), config("PRIVATE_KEY"))

bi = BancoInter(config("CPFCNPJ_BENEF"), config("X-INTER-CONTA-CORRENTE"), cert)

pagador = {
    "cnpjCpf":"99999999999",
    "nome":"Nome do Pagador",
    "email":"pagador@gmail.com",
    "telefone":"999999999",
    "cep":"99999999",
    "numero":"00",
    "complemento":"proximo ao pagador",
    "bairro":"Bairro do Pagador",
    "cidade":"Cidade do Pagador",
    "uf":"MG",
    "endereco":"Logradouro do Pagador",
    "ddd":"99",
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
    dataEmissao="2021-08-19",
    dataVencimento="2021-08-23",
    seuNumero="00001",
    valorNominal=9.9,
)

print(reponse)
