#Foo and Bar stats Collector for running instances

from tokenize import String
import requests
import oauth2 as oauth
import json
import os
import logging
import sys
import time
import datetime

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

class FooBarCollector:
    def postToES(self, es_url, es_index, json_log):
        es_url = es_url + "/" + es_index + "/_doc"
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        try:
            post_output = requests.post(es_url, data=json.dumps(json_log), headers=headers)
        except UnicodeDecodeError:
            return False
        if not post_output.ok:
            logging.info("{} {}".format(post_output.text,post_output.json()))
            return False
        return True

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
        header = req.to_header()
        ascii_header = header['Authorization'].encode('ascii', 'ignore')
        headers = {"Authorization": ascii_header, "Content-Type": "application/json"}
        response = requests.get(request_url, headers=headers)
        if not response.ok:
            logging.error("Load operation was not OK. The response is: {}".format(response))
        return response.json()

#Method to collect the logs in json format for instance stats and write it to a json file to pass it to Elastic Search for visualization		
def get_log():
    if len(sys.argv) == 1:
        logging.info("Please provide instance urls to collect the stats.")
        logging.info("Usage : Script_Name \"url1\;url2;...;urln\" \"Elastic Search Url\"")
        exit(1)
    else:
        urls = sys.argv[1].split(';')
    es_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:9200"
    logging.info("Elastic Search URL : {}".format(es_url))
    es_index = "foo_bar"

    default_es_date_format = '%Y-%m-%dT%H:%M:%S%z'
    json_output_file = "response.json"
    if os.path.exists(json_output_file):
        os.remove(json_output_file)

    json_log = {}
    json_logs = []
    for url in urls:
        logging.info("Request for: {}".format(url))
        logging.info("Fetching data with URL: {}".format(url))
        fooBarCollector = FooBarCollector(url)
        json_log = fooBarCollector.get_response()
        json_log['url'] = url
        json_log['timestamp'] = datetime.datetime.now().strftime(default_es_date_format)
       
        json_logs.append(json_log)
                
    with open(json_output_file,'a') as file:
        json.dump(json_logs, file)
        logging.info('Created json file')

    with open(json_output_file) as file:
        json_data = json.load(file)
        logging.info('STARTED POSTING LOGS. TOTAL SIZE...{}'.format(str(len(json_data))))
		
    for json_log in json_data:
        fooBarCollector.postToES(es_url, es_index, json_log) 

if __name__ == '__main__':
	get_log()
    
      
