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


def get_separate(lista):
    ordened = sorted(lista, reverse=True)
    avgl = []
    cont = []
    for a in ordened:
        index = -1
        if a in avgl:
            index = avgl.index(a)
        if index >= 0:
            cont[index] = 1 + cont[index]
        else:
            avgl.append(a)
            cont.append(1)
    return avgl, cont


def get_positions_from_interactions(interactions: list):
    position = []
    for x in interactions:
        doc = Document(x['id_documento'], x['posicao'], x['page'])
        if found(position, doc):
            position.append(doc)
    return position


def getall_interactions(limit: int, offset: int):

    response = requests.post(url='http://DESKTOP-PJQJQM5:5050/interactions/all?limit={limit}&offser={offset}', auth=('junior', 'hello'),
                             headers={'content-type': 'application/json'})
    return response.json()


def get_interactions(start: str, finish: str, limit: int, offset: int):
    jsonbody = json.dumps({
        'start': start,
        'finish': finish,
        'limit': limit,
        'offset': offset
    })
    response = requests.post(url='http://DESKTOP-PJQJQM5:5050/interactions', auth=('junior', 'hello'),
                             data=jsonbody, headers={'content-type': 'application/json'})
    return response.json()


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


def filterfuntion(lista, method):
    return [x for x in lista if x.method == method]


def run_experiment():
    methods = [
        "equality",
        "phrase_single_line",
        "phrase_multiple_lines",
        "prefix",
        "proximity",
        "similarity",
        "substring"
    ]
    result = get_interactions('17/10/2020', '17/11/2020', 100, 0)
    times_search = []
    avglist = []
    for res in result['hits']:
        query = res['query']
        method = res['metodo']
        limit = res['limit']
        offset = res['offset']
        timestamp = res['timestamp']
        documents = res['documents']
        interactions = res['interacao']
        interactionssorted = sorted(interactions, key=lambda k: k['posicao'])
        positions = get_positions_from_interactions(interactionssorted)
        retrieved = []
        relevant = []
        pos = 0
        count = 1
        #amount = 0
        #qtd = limit
        # while amount < qtd:
        inicio = time.time()
        search = get_consult(query, method, limit, offset, documents)
        tempo_gasto = time.time() - inicio
        times_search.append(tempo_gasto)
        #qtd = search['hits_amount']
        retrieved = []
        relevant = []
        if 'hits' in search:
            for x in search['hits']:
                doc = Document(x['file_id'], pos, x['page'])
                retrieved.append(count)
                if not found(positions, doc):
                    relevant.append(count)
                count += 1
                pos += 1
            #amount += 20
        avg = average_precision(retrieved, relevant)
        #avglist.append(round(avg, 4))
        avglist.append(avg)
    media_itera = media_avg2(avglist)
    print("-> Quantidade Registros: ", len(avglist))
    print("-> Média AvgPrec: ", media_itera)
    with open('interacoes.json', 'w') as outfile:
        js = json.dumps({"list": avglist})
        outfile.write(js)
    #avgfilter, cont = get_separate(avglist)
    #plot_search_avrg(cont, avgfilter)
    histogram_search_avrg_plot(avglist)


def main():
    inicio = time.time()
    run_experiment()
    tempo_gasto = time.time() - inicio
    print("Tempo de execução Total: " + str(tempo_gasto) + " segundos")


main()
