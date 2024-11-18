# bancointer.py

import os
import warnings

from bancointer.cobranca_v3.models.tipo_baixa import TipoBaixa
from bancointer.deprecated import deprecated
from bancointer.util import Util


@deprecated(
    "Use Classes EmiteCobranca, RecuperaCobranca, RecuperaCobrancaPDF and CancelaCobranca instead"
)
class BancoInter(object):
    """Classe para transacoes (emissao, baixa, download) de boletos na API do Banco Inter PJ.
    Na emissao de boletos o padrao inicial e sem desconto, multa e juros de mora.
    """

    # Class attributes
    _SEM_DESCONTO = {
        "codigo": "PERCENTUALDATAINFORMADA",
        "taxa": 0,
        "valor": 0,
        "quantidadeDias": 0,
        "data": "2024-11-17",
    }
    _ISENTO_MULTA = {"codigo": "VALORFIXO", "valor": 0, "taxa": 0}
    _ISENTO_MORA = {"codigo": "TAXAMENSAL", "valor": 0, "taxa": 0}

    def __init__(self, base_url, base_url_token, client_id, client_secret, cert):
        """Metodo construtor da classe.

        Args:
            base_url (str): URL base da api de cobranca.
            base_url_token (str): URL base da api de cobranca para gerar o token de acesso.
            client_id (str): Client Id obtido no detalhe da tela de aplicações no IB.
            client_secret (str): Client Secret obtido no detalhe da tela de aplicações no IB.
            cert (tuple): (cert_file_path, key_file_path) PEM path do certificado digital e PEM path da chave publica.
        """
        self.base_url = base_url
        self._API_VERSION = 3
        self.desconto = self._SEM_DESCONTO
        self.multa = self._ISENTO_MULTA
        self.mora = self._ISENTO_MORA
        self.client_id = client_id
        self.client_secret = client_secret
        self.util = Util(
            base_url=base_url,
            base_url_token=base_url_token,
            client_id=client_id,
            client_secret=client_secret,
            cert=cert,
        )

    @property
    def api_version(self):
        return self._API_VERSION

    # def set_base_url(self, value):
    #     self.base_url = value

    # def set_base_url_token(self, value):
    #     self.base_url_token = value

    def set_api_version(self, api_version=3):
        """Set API version, DEFAULT is API version 3."""
        self._API_VERSION = api_version

    def _get_url(self, path):
        return f"{self.base_url}{path}"

    def set_desconto(self, desconto):
        """Dict para desconto no boleto.
        Código de Desconto do título.

        NAOTEMDESCONTO - Não tem desconto.
        VALORFIXODATAINFORMADA - Valor fixo até data informada.
        PERCENTUALDATAINFORMADA - Percentual até data informada.
        VALORANTECIPACAODIACORRIDO - Valor por antecipação (dia corrido).
        VALORANTECIPACAODIAUTIL - Valor por antecipação (dia útil).
        PERCENTUALVALORNOMINALDIACORRIDO - Percentual sobre o valor nominal por dia corrido.
        PERCENTUALVALORNOMINALDIAUTIL - Percentual sobre o valor nominal por dia útil.
        desconto = {
            "codigoDesconto": "ISENTO",
            "valor": 0,
            "taxa": 0
        }

        Args:
            desconto (dict): Dict de desconto a ser aplicado no boleto.
        """
        self.desconto = desconto

    def set_multa(self, multa):
        """Codigo de Multa do título.

        NAOTEMMULTA - Não tem multa
        VALORFIXO – Valor Fixo
        PERCENTUAL - Percentual

        Args:
            multa (dict): Dict para configuracao de multa
        """
        self.multa = multa

    def set_mora(self, mora):
        """Codigo de Mora do titulo.

        VALORDIA - Valor ao dia
        TAXAMENSAL - Taxa mensal
        ISENTO - Não há mora

        Args:
            mora (dict): Dict para configuracao de juros de mora
        """
        self.mora = mora

    def boleto(
        self, pagador, mensagem, dataEmissao, dataVencimento, seuNumero, valorNominal
    ):
        warnings.warn(
            "This method has been deprecated and will be removed in future versions. "
            "Use EmiteCobranca.emitir(SolicitacaoEmitirCobranca)",
            DeprecationWarning,
        )
        """Metodo para emissao de boletos bancarios na API do Banco Inter.

           Saiba mais em: https://developers.inter.co/references/token

        Args:
            pagador (dict): {
                "cpfCnpj": "99999999999", # valido
                "nome": "NOME DO PAGADOR",
                "email": "email@pagador.com",
                "telefone": "999999999",
                "cep": "99999999",
                "numero": "9999",
                "complemento": "",
                "bairro": "BAIRRO DO PAGADOR",
                "endereco": "ENDERECO DO PAGADOR",
                "cidade": "CURITIBA",
                "uf": "PR",
                "ddd": "99",
                "tipoPessoa": "JURIDICA" # OU FISICA
            }
            mensagem (dict): {
                "linha1": "linha1",
                "linha2": "linha2",
                "linha3": "linha3",
                "linha4": "linha4",
                "linha5": "linha5",
            }
            dataVencimento (str): "Y-m-d"
            seuNumero (str): seu numero de controle do documentp
            valorNominal (float): valor do boleto, ex: 100.50

        Returns:
            response: Corpo do response retornado pela API.
        """

        path = "cobrancas"

        payload = {
            "seuNumero": seuNumero,
            "valorNominal": valorNominal,
            "dataVencimento": dataVencimento,
            "numDiasAgenda": 30,
            "pagador": pagador,
            "desconto": self.desconto,
            "multa": self.multa,
            "mora": self.mora,
            "mensagem": mensagem,
        }

        response = self.util.make_request_with_token(
            method="post", path=path, _json=payload
        )

        return response

    def download(self, codigo_solicitacao, download_path):
        warnings.warn(
            "This method has been deprecated and will be removed in future versions. "
            "Use RecuperaCobrancaPDF.recuperar_pdf(codigo_solicitacao, download_path) instead",
            DeprecationWarning,
        )
        """Metodo para download de boletos emitidos.

        Args:
            codigo_solicitacao (string <uuid>): Codigo unico da cobrança
            download_path (str): Path completo para salvar o boleto. Ex: `/tmp/downloads`

        Returns:
            (bool): True em caso de sucesso ou False caso contrario.
        """
        path = f"cobrancas/{codigo_solicitacao}/pdf"

        json = None

        response = self.util.make_request_with_token(method="get", path=path, json=json)

        file_path = download_path + os.sep + codigo_solicitacao + ".pdf"

        return self.util.file_save(response, file_path)

    def baixa(self, codigo_solicitacao, motivo_cancelamento: TipoBaixa):
        warnings.warn(
            "This method has been deprecated and will be removed in future versions. "
            "Use CancelaCobranca.cancela(codigo_solicitacao, motivo_cancelamento) instead",
            DeprecationWarning,
        )
        """Metodo para baixa (Cancelamento) de boleto emitido.
        Dominio que descreve o tipo de baixa sendo solicitado.

        ACERTOS - Baixa por acertos
        PROTESTADO - Baixado por ter sido protestado
        DEVOLUCAO - Baixado para devolução
        PROTESTOAPOSBAIXA - Baixado por protesto após baixa
        PAGODIRETOAOCLIENTE - Baixado, pago direto ao cliente
        SUBISTITUICAO - Baixado por substituição
        FALTADESOLUCAO - Baixado por falta de solução
        APEDIDODOCLIENTE - Baixado a pedido do cliente

        Args:
            codigo_solicitacao (string <uuid>): Codigo unico da cobrança
            motivo_cancelamento (string <= 50 characters): 	Motivo pelo qual a cobrança está sendo cancelada
        Returns:
            Response code (string): Response da requisicao. 202 se foi cancelada.
        """
        act = "cancelar"
        payload = {"motivoCancelamento": motivo_cancelamento.value}

        path = f"cobrancas/{codigo_solicitacao}/{act}"

        response = self.util.make_request_with_token(
            method="post", path=path, _json=payload
        )

        return response

    def consulta(self, codigo_solicitacao):
        warnings.warn(
            "This method has been deprecated and will be removed in future versions. "
            "Use RecuperaCobranca.recuperar(codigo_solicitacao) instead",
            DeprecationWarning,
        )
        """Recupera as informações detalhadas de um boleto através do `nosso_numero`.

        Args:
            codigo_solicitacao (string <uuid>): Codigo unico da cobrança.

        Returns:
            dict: json-encoded of a response, `response.json()` dict com os dados do boleto.
        """
        path = f"cobrancas/{codigo_solicitacao}"

        response = self.util.make_request_with_token(
            method="get", path=path, _json=None
        )

        return response.json()
