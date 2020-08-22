from elastic_client import Elastic_client
import requests
import time
import json


def get_documents_from_interactions(interactions: list):
    documents_id = []
    [documents_id.append(x['id_documento'])
     for x in interactions if x['id_documento'] not in documents_id]
    return documents_id


def get_consult(query: str, method: str, documents_id: list):
    jsonbody = json.dumps({
        'query': query,
        'method': method,
        'documents': documents_id
    })
    response = requests.post(url='http://0.0.0.0:5000/search', data=jsonbody, headers = {'content-type': 'application/json'})
    return response.json()


def get_interactions():
    methods = [
        "equality",
        "phrase_single_line",
        "phrase_multiple_lines",
        "prefix",
        "proximity",
        "similarity",
        "substring"
    ]
    client = Elastic_client()
    result = client.get_documents()

    for res in result['hits']['hits']:
        query = res['_source']['query']
        method = res['_source']['metodo']
        timestamp = res['_source']['timestamp']
        interactions = res['_source']['interacao']
        documents_id = get_documents_from_interactions(interactions)
        search = get_consult(query, method, documents_id)


def main():
    inicio = time.time()
    get_interactions()
    tempo_gasto = time.time() - inicio
    print("Tempo de execução Total: " + str(tempo_gasto) + " segundos")


main()
