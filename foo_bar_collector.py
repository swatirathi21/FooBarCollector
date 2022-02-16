import requests
import oauth2 as oauth
import time
import json
import os
import logging
import logging.config
import sys

from oath_sha256 import SignatureMethod_HMAC_SHA256


class FooBarCollector:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def _url(self, path=None):
        return self.endpoint + ("" if path is None else path)

    def get_response(self):
        request_url = self._url()
        http_method = "GET"
        result = self.send_request(http_method, request_url)
        return result

    def send_request(self, http_method, request_url):
        params = {
            'oauth_version': "1.0",
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': str(int(time.time()))
        }
        req = oauth.Request(method=http_method, url=request_url, parameters=params)
        #signature_method = SignatureMethod_HMAC_SHA256()
        #req.sign_request(signature_method, self.consumer, self.token)
        header = req.to_header()
        ascii_header = header['Authorization'].encode('ascii', 'ignore')
        headers = {"Authorization": ascii_header, "Content-Type": "application/json"}
        response = requests.get(request_url, headers=headers)
        if not response.ok:
            print("Load operation was not OK. The response is: " + response.text)
            logging.error("Load operation was not OK. The response is: " + response.text)
        return response.json()

if __name__ == '__main__':
    logging.basicConfig(filename='errors.log', level=logging.ERROR)
    # url = os.getenv('url')
    #url = sys.argv[1]
    url = "http://127.0.0.1:9999/stats"

    print("Request for: " + url)
    logging.error("Fetching records with URL: {}".format(url))

    fooBarCollector = FooBarCollector(url)
    log = fooBarCollector.get_response()
    with open('Response' + '.json', 'w') as outfile:
        json.dump(log, outfile)
    print('Created Response.json')
