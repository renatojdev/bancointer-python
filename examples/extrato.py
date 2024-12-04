# extrato.py


from decouple import config

dir_base_ssl = config("SSL_DIR_BASE")

cert = (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2"))

url = "https://cdpj.partners.bancointer.com.br/banking/v2/extrato?dataInicio=2022-05-01&dataFim=2022-05-03"

# Gerar certificado com permissao de ler extrato e token com escopo 'extrato.read'
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer 4ca89e20-fa9d-4e68-9a1b-f4a432d341d5",
}

escopos = ["extrato.read", "boleto.read", "boleto.write"]

escopos.remove("extrato.read")

str_escopos = " ".join(escopos)

print(str_escopos)

# response = requests.get(url, headers=headers, cert=cert)

# response = response.raise_for_status()

# print(response.status_code, response.text)
