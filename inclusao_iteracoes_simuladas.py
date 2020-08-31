from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import ImproperlyConfigured, ElasticsearchException, TransportError
import os
import json
import datetime
import random
import requests

def update_single_document(client, index, id, jsondata: str):
    try:
        return client.update(index=index,  id=id, body=jsondata)
    except ImproperlyConfigured as i:
        raise Exception(
            "Elasticsearch -> index_single_document -> config error:" + str(i) + "\n entrada: "+jsondata)
    except TransportError as t:
        raise Exception("Elasticsearch -> index_single_document -> transport error:" +
                        str(t.error) + "\n entrada: "+jsondata)
    except ElasticsearchException as e:
        raise Exception(
            "Elasticsearch -> index_single_document -> exception error:" + str(e) + "\n entrada: "+jsondata)

def index_single_document(client, index, id, jsondata: str):
    try:
        return client.index(index=index,  id=id, body=jsondata, doc_type='_doc')
    except ImproperlyConfigured as i:
        raise Exception(
            "Elasticsearch -> index_single_document -> config error:" + str(i) + "\n entrada: "+jsondata)
    except TransportError as t:
        raise Exception("Elasticsearch -> index_single_document -> transport error:" +
                        str(t.error) + "\n entrada: "+jsondata)
    except ElasticsearchException as e:
        raise Exception(
            "Elasticsearch -> index_single_document -> exception error:" + str(e) + "\n entrada: "+jsondata)

def get_consult(query: str, method: str, limit:str, offset:str, documents_id: list):
    jsondata = json.dumps({
        'query': query,
        'method': method,
        'limit': limit,
        'offset': offset,
        'documents': documents_id
    })
    headers = requests.utils.default_headers()
    headers.update(
        {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
            'content-type': 'application/json'
        }
    )
    response = requests.post(url='http://172.17.0.2:31227/search', data=jsondata, headers = headers)
    return response.json()


def get_document(client, index, id):
    try:
        return client.get(index=index,  id=id)
    except ImproperlyConfigured as i:
        raise Exception(
            "Elasticsearch -> get_document -> config error:" + str(i))
    except TransportError as t:
        raise Exception("Elasticsearch -> get_document -> transport error:" +
                        str(t.error))
    except ElasticsearchException as e:
        raise Exception(
            "Elasticsearch -> get_document -> exception error:" + str(e))

authentication = (os.getenv('ELASTICSEARCH_USER', 'elastic'), os.getenv(
    'ELASTICSEARCH_PASSWORD', ''))
hosts = os.getenv('ELASTICSEARCH_HOST', [
    'http://172.17.0.2:30003/'])
scheme = os.getenv('ELASTICSEARCH_SCHEME', 'http')
index = os.getenv('ELASTICSEARCH_INDEX', 'interacoes')
client = Elasticsearch(
    hosts=hosts, http_auth=authentication, scheme=scheme, request_timeout=5000, connection_timeout=5000, timeout=5000, max_retries=10, retry_on_timeout=True)

methods = [
        "equality",
        "phrase_single_line",
        "phrase_multiple_lines",
        "prefix",
        "proximity",
        "similarity",
        "substring"
    ]

querys = ['borges', 'WELTON', 'PAPA', 'American', 'Batteries', 'levantamento', 'energia']
operacao = ['visualizou', 'baixou xfdf', 'baixou jpg']
documents = ["ed863078-463c-4302-bd6a-e6ef7db89778", 
"e770e245-5688-422b-8965-1fc181f3edc8",
"b60b729d-fb42-413c-8c0f-66d0402e1b8a", 
"52949a92-948d-4cbc-b5d2-aafef3569f12", 
"37c5f60e-b044-4fa9-8582-f2e115af2501", 
"9cee72fd-835a-440b-a09b-a2a2c4777509", 
"6b597709-ced2-42d9-b899-ef9d983785de", 
"dbaa0eab-345c-405e-b3c4-d5311234b202", 
"09227de0-9017-4a14-bb4a-d46f053ee49e", 
"5e194287-117a-4db3-bd75-39c25fdad19a", 
"7bdfcea9-34d5-4fe5-9662-1d02d6d4de27", 
"5ffbe027-4c61-4651-bd6c-8308705e69f7", 
"009d00ce-0375-47c9-9843-accfdd03f3dc", 
"3c55fcee-ed0f-4b32-bd50-b197585b467e",
"0da8e1df-c5df-4a9c-b66a-7f5173d8ac44"]

for a in range(0,10):
  posmeth = random.randint(0, 6)
  posquer = random.randint(0, 6)
  search = get_consult(querys[posquer], methods[posmeth], '20', '0', documents)
  
  jsonstr = {
      "query": querys[posquer], "metodo": methods[posmeth], "timestamp": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),"limit":20, "offset":0, "documents": documents, "interacao":[]
  }
  strjson = json.dumps(jsonstr)
  index_single_document(client, index, a, strjson)
  qtd = len(search['hits'])-1
  for b in range(0, 10):
    posicao = random.randint(0, qtd)
    posoper = random.randint(0, 2)
    jsonstr1 = {
        "script": {
        "source": "ctx._source.interacao.add(params.interacao)",
        "lang": "painless",
        "params": {
          "interacao": {"timestamp":datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), 'id_documento': search['hits'][posicao]['file_id'], 'page': search['hits'][posicao]['page'],"posicao":posicao, "operação":operacao[posoper]}
        }
      }
    }
    # jsonstr2 = {
    #     "script": {
    #     "source": "ctx._source.offset = params.offset",
    #     "lang": "painless",
    #     "params": {
    #       "offset": 40
    #     }
    #   }
    # }
    
    strjson1 = json.dumps(jsonstr1)
    # strjson2 = json.dumps(jsonstr2)
    
    update_single_document(client, index, a, strjson1)
    # update_single_document(client, index, a, strjson2)
#print(get_document(client, index, 3))

get = {
  "query": {
    "bool": {
      "must": [
        {
          "match": {"metodo": "subcadeia"}
          
        },
        {
          "match": {
            "interacao.operação": "click124"
          }
        }
      ]
    }
  }
}