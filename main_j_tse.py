from elastic_client import Elastic_client
import requests
import time
import json
from metricas import *
from model import *
from utils import *
class Document:
    def __init__(self, doc_id, posicao):
        self.doc_id = doc_id
        self.pos = posicao

def found(lista, doc):
    if len(lista) == 0:
        return True
    elif len(lista) > 0:
        if lista[0].doc_id == doc.doc_id and lista[0].pos == doc.pos:
            return False
        else:
            return found(lista[1:], doc)


def get_documents_and_positions_from_interactions(interactions: list):
    documents_id = []
    position = []
    atual_pos = -1
    doc_atual = ''
    for x in interactions:
        if x['id_documento'] not in documents_id:
            documents_id.append(x['id_documento'])
        doc = Document(x['id_documento'], x['posicao'])
        if found(position, doc):
            position.append(doc)
    return documents_id, position


def get_consult(query: str, method: str, limit:int, offset:int, documents_id: list):
    jsonbody = json.dumps({
        'query': query,
        'method': method,
        'limit': limit,
        'offset': offset,
        'documents': documents_id
    })
    response = requests.post(url='http://172.17.0.2:31227/search', data=jsonbody, headers = {'content-type': 'application/json'})
    return response.json()

def filterfuntion(lista, method):
    return [x for x in lista if x.method == method]

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
    iteration_list = []
    for res in result['hits']['hits']:
        query = res['_source']['query']
        method = res['_source']['metodo']
        limit = res['_source']['limit']
        offset = res['_source']['offset']
        timestamp = res['_source']['timestamp']
        interactions = res['_source']['interacao']
        interactionssorted = sorted(interactions, key=lambda k: k['posicao'])
        documents_id, positions = get_documents_and_positions_from_interactions(interactionssorted)
        inicio = time.time()
        search = get_consult(query, method, limit, offset, documents_id)
        tempo_gasto = time.time() - inicio
        times_search.append(tempo_gasto)
        qtd = search['hits_amount']
        retrieved = []
        relevant = []
        pos = 0
        count = 1
        for x in search['hits']:
            doc = Document(x['file_id'], pos)
            retrieved.append(count)
            if found(positions, doc):
                relevant.append(count)
            count += 1
        qtd_retornado = str(len(retrieved))
        avg = average_precision(retrieved, relevant)

        recall_list =  recall_at_k(retrieved, relevant)
        precision_list = precision_at_k(retrieved, relevant)
        m = model(res, search, qtd_retornado, avg, relevant, precision_list, recall_list, method)
        iteration_list.append(m)
    list_plot = []
    for y in methods:
        method_list = filterfuntion(iteration_list, y)
        if len(method_list) > 0:
            mrec_iterac_list = obter_recal(method_list)
            mpr_iterac_list = obter_prec(method_list)
            media_itera = media_avg(method_list)
            print("-> Quantidade Registros ", y, ": ", len(method_list))
            print("-> Média AvgPrec ", y, ": ", media_itera)
            inf = info(media_itera, mrec_iterac_list, mpr_iterac_list, method_list, y)
            list_plot.append(inf)
            with open('interacoes'+y+'.json', 'w') as outfile:
                js = inf.toJSON()
                outfile.write(js)
    plot_curve_j3(list_plot)
def main():
    inicio = time.time()
    get_interactions()
    tempo_gasto = time.time() - inicio
    print("Tempo de execução Total: " + str(tempo_gasto) + " segundos")


main()
