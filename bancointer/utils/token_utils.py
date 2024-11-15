# token_utils.py

import json
import os
import http.client
from pathlib import Path

import certifi
import ssl
from datetime import datetime, timedelta
from decouple import config

from bancointer.utils.constants import (
    HOST_SANDBOX,
    PATH_TOKEN,
    ESCOPO_BOLETO_COBRANCA_READ,
    ESCOPO_BOLETO_COBRANCA_WRITE,
)


def token_file_is_exist():
    token_file_path = Path(TokenUtils.TOKEN_FILE_PATH)

    if token_file_path.exists():
        """Checks if the token file exists, returns True and if the content is invalid, returns False"""
        print(f"O arquivo TOKEN existe!")
        with token_file_path.open(mode='r', encoding='utf-8') as token_file:
            conteudo: str = token_file.read()
            if conteudo == 'null':
                return False
            else:
                data = json.loads(conteudo)
                try:
                    if data['expires_in']:
                        return True
                except KeyError as ke:
                    print(f"token_file_is_exist.Exception: {ke}")
                    return False
        return True
    print("O arquivo TOKEN não existe.")
    return False


class TokenUtils(object):
    TOKEN_FILE_PATH = (
        os.path.dirname(os.path.realpath(__file__)) + os.sep + "token.json"
    )
    X_CONTA_CORRENTE = config("X_INTER_CONTA_CORRENTE")

    def __init__(self, client_id, client_secret, cert):
        self.client_id = client_id
        self.client_secret = client_secret
        self.cert = cert

    def __request_api_token(self):
        """Get a new token from Banco Inter API"""

        payload = (
            "grant_type=client_credentials&client_id="
            + self.client_id
            + "&client_secret="
            + self.client_secret
            + f"&scope={ESCOPO_BOLETO_COBRANCA_READ}%20{ESCOPO_BOLETO_COBRANCA_WRITE}"
        )

        headers = {
            "x-conta-corrente": str(self.X_CONTA_CORRENTE),
            "Content-Type": "application/x-www-form-urlencoded",
        }

        try:
            # Define the client certificate settings for https connection
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.load_verify_locations(certifi.where())
            context.load_cert_chain(certfile=self.cert[0], keyfile=self.cert[1])

            # Create a connection to submit HTTP requests
            connection = http.client.HTTPSConnection(
                HOST_SANDBOX, port=443, context=context
            )
            # Use connection to submit a HTTP POST request
            connection.request(
                method="POST", url=PATH_TOKEN, headers=headers, body=payload
            )
            # return self.http_util.make_request(PATH_TOKEN, payload, headers)
            # Print the HTTP response from the IOT service endpoint
            response = connection.getresponse()
            print(response.status, response.reason)
            token_data = response.read()

            decoded_data = token_data.decode("utf-8")
            token_data_dict = json.loads(decoded_data)
            connection.close()
            return token_data_dict
        except Exception as e:
            print(f"REQUEST TOKEN ERROR: {e}")
            # sys.exit(1)

    def __read_token_from_file(self):
        """Read a token value and return a dict from file"""
        try:
            # Opening JSON file
            f = open(self.TOKEN_FILE_PATH)
            # returns JSON object as
            # a dictionary
            data = json.load(f)
            # Closing file
            f.close()
        except Exception as e:
            print("bancointer.read_token.Except: ", e)
            return {}
        return data

    def save_token_to_file(self, token_data=None):
        """Save a token to file. Add expires_at token, value date now + expires in seconds"""
        if token_data is not None:
            expires_at = datetime.now() + timedelta(seconds=token_data["expires_in"])
            token_data["expires_at"] = str(expires_at)
        else:
            pass

        # Directly from dictionary
        with open(self.TOKEN_FILE_PATH, "w+") as outfile:
            json.dump(token_data, outfile)
        outfile.close()

    def get_api_token(self):
        """Get token if valid from file or get new token from API.
        Token is valid if current date less then token expires at.
        """
        token_data = self.__read_token_from_file()

        if token_data is None or token_data == {}:
            token_data = self.__request_api_token()
            if token_data != {}:
                # self.bearer_token = token_data
                self.save_token_to_file(token_data=token_data)
            else:
                return {}

        current_date = datetime.now()
        if current_date > datetime.fromisoformat(token_data["expires_at"]):
            token_data = self.__request_api_token()
            self.save_token_to_file(token_data=token_data)

        return token_data["access_token"]