from elastic_client import Elastic_client
import requests
import time
import json
from metricas import *
from model import *
from utils import *


class Document:
    def __init__(self, doc_id, posicao, page):
        self.doc_id = doc_id
        self.pos = posicao
        self.page = page


def found(lista, doc):
    if len(lista) == 0:
        return True
    elif len(lista) > 0:
        if lista[0].doc_id == doc.doc_id and lista[0].pos == doc.pos and lista[0].page == doc.page:
            return False
        else:
            return found(lista[1:], doc)


def get_positions_from_interactions(interactions: list):
    position = []
    atual_pos = -1
    doc_atual = ''
    for x in interactions:
        doc = Document(x['id_documento'], x['posicao'], x['page'])
        if found(position, doc):
            position.append(doc)
    return position


def get_consult(query: str, method: str, limit: int, offset: int, documents_id: list):
    jsonbody = json.dumps({
        'query': query,
        'method': method,
        'limit': limit,
        'offset': offset,
        'documents': documents_id
    })
    response = requests.post(url='http://tot.cloud.c3.furg.br/api/tse/search',
                             data=jsonbody, headers={'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
                                                     'x-tot-auth': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MzE3MTE3MjYsInVzZXJuYW1lIjoidG90YWRtaW4ifQ.mYy3vOAW8v--5CJBC-nltBzUIzuf06KurqkJmoF_Ul8'})
    return response.json()


def getxy(hits: list, x: list, y: list):
    for a in hits:
        if a['score'] not in x:
            x.append(float(a['score']))
            y.append(float(1))
        else:
            y[-1] = y[-1] + 1
    return x, y


def get_scores_from_interactions(interactions: list, hits: list):
    score = []
    for x in interactions:
        if x['posicao'] < len(hits):
            if hits[x['posicao']]['page'] == x['page']:
                score.append(hits[x['posicao']]['score'])
    return score


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
    times_search = []
    for res in result['hits']['hits']:
        score_list = []
        interaction_score_list = []
        x, y = [], []
        query = res['_source']['query']
        print(query)
        method = res['_source']['metodo']
        print(method)
        limit = res['_source']['limit']
        offset = res['_source']['offset']
        timestamp = res['_source']['timestamp']
        documents = res['_source']['documents']
        interactions = res['_source']['interacao']
        interactionssorted = sorted(interactions, key=lambda k: k['posicao'])
        #positions = get_positions_from_interactions(interactionssorted)
        inicio = time.time()
        search = get_consult(query, method, limit, offset, documents)
        tempo_gasto = time.time() - inicio
        times_search.append(tempo_gasto)
        intescor = get_scores_from_interactions(
            interactionssorted, search['hits'])
        interaction_score_list += intescor
        qtd = search['hits_amount']
        print(qtd)
        x, y = getxy(search['hits'], x, y)
        scores_temp = [x['score'] for x in search['hits']]
        score_list += scores_temp
        count = 20
        while count <= qtd:
            inicio = time.time()
            search = get_consult(query, method, 20, count, documents)
            tempo_gasto = time.time() - inicio
            times_search.append(tempo_gasto)
            x, y = getxy(search['hits'], x, y)
            intescor = get_scores_from_interactions(
                interactionssorted, search['hits'])
            interaction_score_list += intescor
            scores_temp = [x['score'] for x in search['hits']]
            score_list += scores_temp
            offset = count
            count += 20
        # histogram_plot(score_list)
        histogram_plot_v3([score_list, interaction_score_list])


def main():
    inicio = time.time()
    get_interactions()
    tempo_gasto = time.time() - inicio
    print("Tempo de execução Total: " + str(tempo_gasto) + " segundos")


main()
