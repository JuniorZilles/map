from elasticsearch import Elasticsearch, helpers
import os
import json


class Elastic_client:
    # initialize the client
    def __init__(self):
        authentication = (os.getenv('ELASTICSEARCH_USER', 'elastic'), os.getenv(
            'ELASTICSEARCH_PASSWORD', ''))
        hosts = os.getenv('ELASTICSEARCH_HOST', [
                          'http://172.17.0.2:30003/'])
        scheme = os.getenv('ELASTICSEARCH_SCHEME', 'http')
        self.index = os.getenv('ELASTICSEARCH_INDEX', 'interacaoes')
        self.client = Elasticsearch(
            hosts=hosts, http_auth=authentication, scheme=scheme, request_timeout=5000, connection_timeout=5000, timeout=5000, max_retries=10, retry_on_timeout=True)

    # input a json with the query and outputs the json with the result
    def get_documents(self):
        jsondata = json.dumps({
            "query": {
                "match_all": {}
            }
        })
        filter_path = ['hits.hits._source']
        return self.client.search(index=self.index, body=jsondata, filter_path=filter_path)
