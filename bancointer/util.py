# util.py

import os
import sys
import requests
import json
import codecs
from datetime import datetime, timedelta
from decouple import config

from bancointer.deprecated import deprecated


@deprecated("Use Class HttpUtils instead")
class Util(object):
    _TOKEN_FILE_PATH = (
        os.path.dirname(os.path.realpath(__file__)) + os.sep + "token.json"
    )
    _X_CONTA_CORRENTE = config("X_INTER_CONTA_CORRENTE")

    def __init__(self, base_url, base_url_token, client_id, client_secret, cert):
        self.client_id = client_id
        self.client_secret = client_secret
        self.cert = cert
        self.url = base_url
        self.base_url_token = base_url_token
        self.headers = {"Content-Type": "application/json"}
        self.bearer_token = {}

    def add_header_authorization(self, value):
        self.headers["Authorization"] = f"Bearer {value}"
        self.headers["x-conta-corrente"] = self._X_CONTA_CORRENTE

    def make_request_with_token(self, method, path, _json=None, **kwargs):
        self.add_header_authorization(self.__get_token()["access_token"])
        return self.make_request(
            method=method, path=path, _json=_json, cert=self.cert, **kwargs
        )

    def make_request(self, method, path, _json, **kwargs):
        """Executa as requisicoes na API do Banco Inter conforme os parametros de entrada.

        Args:
            method (str): Metodo de requisicao GET / POST.
            path (str): URL / endpoint para a requisicao
            _json (dict): Json para ser enviado no POST.

        Returns:
            dict or int: Retorna json response caso exista ou status code do response.
        """
        endpoint = f"{self.url}{path}"

        if method == "get" or _json is None:
            response = requests.request(
                method=method,
                url=endpoint,
                headers=self.headers,
                **kwargs,
            )
            response.raise_for_status()
            return response

        response = requests.request(
            method=method,
            url=endpoint,
            headers=self.headers,
            json=_json,
            **kwargs,
        )
        try:
            return response.json()
        except ValueError:  # empty response
            return response.status_code

    def __get_api_token(self):
        """Get a new token from Banco Inter Cobranca API V2"""

        payload = (
            "grant_type=client_credentials&client_id="
            + self.client_id
            + "&client_secret="
            + self.client_secret
            + "&scope=boleto-cobranca.read%20boleto-cobranca.write"
        )

        headers = {
            # "Accept": "application/json",
            "x-conta-corrente": str(self._X_CONTA_CORRENTE),
            "Content-Type": "application/x-www-form-urlencoded",
        }

        try:
            response = requests.post(
                self.base_url_token, data=payload, headers=headers, cert=self.cert
            )

            response.raise_for_status()

            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTPError ERROR: {e}")
            sys.exit(1)
        except requests.exceptions.SSLError as e:
            print(f"SSL ERROR: {e}")
            sys.exit(1)

    def __read_token_from_file(self):
        """Read a token value and return a dict from file"""
        try:
            # Opening JSON file
            f = open(self._TOKEN_FILE_PATH)
            # returns JSON object as
            # a dictionary
            data = json.load(f)
            # Closing file
            f.close()
        except Exception as e:
            print("bancointer.read_token.Except: ", e)
            return {}
        return data

    def __get_token(self):
        """Get token if valid from file or get new token from API.
        Token is valid if current date less then token expires at.
        """
        token_data = self.__read_token_from_file()
        if token_data == {}:
            token_data = self.__get_api_token()
            if token_data != {}:
                self.bearer_token = token_data
                self.__save_token(token_data=token_data)
            else:
                return {}

        current_date = datetime.now()
        if current_date > datetime.fromisoformat(token_data["expires_at"]):
            token_data = self.__get_api_token()
            self.__save_token(token_data=token_data)

        return token_data

    def __save_token(self, token_data=None):
        """Save a token to file. Add expires_at token, value date now + expires in seconds"""
        if token_data is not None:
            expires_at = datetime.now() + timedelta(seconds=token_data["expires_in"])
            token_data["expires_at"] = str(expires_at)
        else:
            pass

        # Directly from dictionary
        with open(self._TOKEN_FILE_PATH, "w+") as outfile:
            json.dump(token_data, outfile)
        outfile.close()

    @staticmethod
    def file_save(response, file_path):
        """Method to file save to disk"""
        if hasattr(response, "content") and response.content is not None:
            content = json.loads(response.content)
        else:
            content = response

        pdf = bytes(content["pdf"], "UTF-8")

        try:
            with open(file_path, "wb") as out_file:
                out_file.write(codecs.decode(pdf, "base64"))
        except Exception as e:
            print("bancointer.file_save.Except: ", str(e))
            return False
        return True
