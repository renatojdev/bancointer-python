# bancointer_fetcher.py

import certifi
import json
import http.client
import ssl


class BancoInterFetcher(object):

    def __init__(self, host, cert):
        """Method constructor"""
        self.host = host
        # Define the client certificate settings for https connection
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.context.load_verify_locations(certifi.where())
        self.context.load_cert_chain(certfile=cert[0], keyfile=cert[1])
        self.headers = {"Accept": "application/json"}

    def __create_connection(self):
        # Create a connection to submit HTTP requests
        self.connection = http.client.HTTPSConnection(
            self.host, port=443, context=self.context
        )

    def __close_connection(self):
        self.connection.close()  # close the active connection

    def fetch(self, method, path, payload, custom_headers_dict=None) -> dict:
        self.__create_connection()

        if custom_headers_dict is not None:
            self.headers.update(custom_headers_dict)

        # Use connection to submit a HTTP POST request
        self.connection.request(
            method=method, url=path, headers=self.headers, body=payload
        )

        # Print the HTTP response from the IOT service endpoint
        response = self.connection.getresponse()
        print(response.status, response.reason)
        data = response.read()
        # Convert bytes to JSON
        json_data = {}
        try:
            json_data = json.loads(
                data.decode("utf-8")
            )  # Decodes the bytes and loads them as JSON
            print(json_data)
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)

        self.__close_connection()
        return json_data
