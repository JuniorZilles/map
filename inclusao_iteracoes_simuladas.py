from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import ImproperlyConfigured, ElasticsearchException, TransportError
import os
import json
import datetime
import random
import requests
import uuid


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


def get_consult(query: str, method: str, limit: int, offset: int, documents_id: list):
    jsonbody = json.dumps({
        'query': query,
        'method': method,
        'limit': limit,
        'offset': offset,
        'documents': documents_id
    })
    response = requests.post(url='http://DESKTOP-PJQJQM5:5050/search', auth=('junior', 'hello'),
                             data=jsonbody, headers={'content-type': 'application/json'})
    return response.json()
# def get_consult(query: str, method: str, limit: str, offset: str, documents_id: list):
#     jsondata = json.dumps({
#         'query': query,
#         'method': method,
#         'limit': limit,
#         'offset': offset  # ,
#         # 'documents': documents_id
#     })
#     headers = requests.utils.default_headers()
#     headers.update(
#         {
#             'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
#             'x-tot-auth': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MzE3MTE3MjYsInVzZXJuYW1lIjoidG90YWRtaW4ifQ.mYy3vOAW8v--5CJBC-nltBzUIzuf06KurqkJmoF_Ul8',
#             'content-type': 'application/json'
#         }
#     )
#     response = requests.post(
#         url='https://tot.cloud.c3.furg.br/api/tse/search', data=jsondata, headers=headers)
#     return response.json()


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
    'http://192.168.56.101:30010/'])
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

querys = ['Valbruna', 'ADELCO', 'INSTALAÇÃO', 'SEÇÃO', 'WAGNER'
          'ANALYSIS', 'VOLUME', '61862', 'PETROBRAS', 'Cinisello', '08/04/2017']
operacao = ['1', '2', '3']
documents = [
    "f426787d-7ebd-4449-9ff3-d8ba64396051",
    "d0a07016-c5a2-4e25-9e07-9c9b1b86d4e4",
    "eff8b54e-ebc5-4a8a-a115-fee662162a8e",
    "e16f47fb-7831-4d87-b682-cfe104417845",
    "def2b6e5-7123-44ec-b4de-e29fe3808cfe",
    "d93d6909-2a94-4329-80e7-de4d1c7a1d29",
    "c9c2948e-6afb-424c-8f58-e90dc6ff23da",
    "a9f40b37-8f80-4054-8a9b-4bd9ee18e4cb",
    "cecda4cb-dc44-42d7-9a79-290df11a234f",
    "b2a62d28-cbeb-4157-a2e1-37bac434a695",
    "d5aebb04-a341-4ce5-a72a-c4bdb025a6b9",
    "cb83ba9f-fbfc-4ee7-95ef-4104a7246e03",
    "c70db2a1-f98a-4ec9-8af1-6781a67a423f",
    "8935a3ee-315a-498a-bf18-385ec4d09a69",
    "bcc65cba-8327-4e05-896a-20296c5ee747",
    "7032b6dc-6705-4135-95e3-6f888b065e56",
    "05298d72-1b4c-4dfb-ba89-a70dc07f6f50",
    "1294eda7-794a-4679-914f-78b3119fa94d",
    "7a7ef0ff-744f-477b-bced-3bf2871c664f",
    "893d0254-0253-46f5-acfc-f63edc072c5f",
    "8ab8ebb9-0edb-48b1-9531-b513463330cd",
    "620f0455-5fc8-4475-b627-fdaaf24f08ce",
    "1ca7a9ae-cae8-4994-9e2d-264f6b36aea1",
    "61f7521b-abe6-4fb4-9a74-ab42dfa481e8",
    "36fb5cac-b33d-459a-836a-7e8e3cb4ee26",
    "317cb92b-a3cb-436e-8eff-a3fa9cf0a212",
    "53f0a3bc-6013-4e57-aa87-e933faa969cb",
    "8ed959d0-088b-4bbd-8f3c-9f3732acf7e1",
    "28fe3cea-4afe-46d6-b78d-fd97f0a2942b",
    "22df19bb-ac89-4246-9833-9a771a76baac",
    "7d1c9c89-f39f-4fbe-b8ee-abc8142f1c1a",
    "015efcb1-e5bc-4899-b107-7ec8f02d9be3",
    "1e9c2359-634e-45be-bb26-df30632423cd",
    "1fe3e31a-196a-4372-9e36-e5fbe3b6d978",
    "7a6083f6-5051-4797-bf47-c7ca8029e01f",
    "1b85af69-7f0a-4632-b7c3-5eb08d832626",
    "0a7b5db2-a21b-454e-88b6-6cf4e26a87bc",
    "90a374b2-e299-405f-b74e-0d75937aa256",
    "2355f15a-61f2-4891-8ea2-79eb9d135fb0",
    "8194c13a-4cfa-4fd7-9436-677e20813c54",
    "6280d477-5aee-49c8-a5e7-266b94f8f07a"]
for a in querys:
    for b in methods:
        uid = uuid.uuid1()
        # posmeth = random.randint(0, 6)
        # posquer = random.randint(0, 9)
        # search = get_consult(
        #     querys[posquer], methods[posmeth], '20', '0', documents)
        search = get_consult(
            a, b, '20', '0', documents)
        if 'hits' in search:
            # jsonstr = {
            #     "query": querys[posquer], "metodo": methods[posmeth], "timestamp": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), "limit": 20, "offset": 0, "documents": documents, "interacao": []
            # }
            jsonstr = {
                "query": a, "metodo": b, "timestamp": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), "limit": 20, "offset": 0, "documents": documents, "interacao": []
            }
            strjson = json.dumps(jsonstr)
            index_single_document(client, index, uid, strjson)
            qtd = len(search['hits'])-1
            for b in range(0, 10):
                posicao = random.randint(0, qtd)
                posoper = random.randint(0, 2)
                jsonstr1 = {
                    "script": {
                        "source": "ctx._source.interacao.add(params.interacao)",
                        "lang": "painless",
                        "params": {
                            "interacao": {"timestamp": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), 'id_documento': search['hits'][posicao]['file_id'], 'page': search['hits'][posicao]['page'], "posicao": posicao, "operação": operacao[posoper]}
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

                update_single_document(client, index, uid, strjson1)
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
