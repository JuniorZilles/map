from metricas import *
from request import *
from database import *
import pandas as pd
import random
import json

from model import *

def main():
    qtdTrocas = int(input("Trocar quantos caracteres de cada palavra? "))
    qtdAmostrasBD = input("Quantidade de amostras do banco? ")
    qtdAmostrasAPI = input("Quantidade de amostras da API? ")
    query = obter_query(qtdAmostrasBD)
    rows = get_database_rows(query)
    df = pd.DataFrame(rows)
    lista = []
    for i in df.index:
        
        nome = df[0][i]
        #print('Termo de original: '+nome + ', posição:' + str(i))
        cnome, pnome, unome = quebra_nome(nome.strip(), qtdTrocas)
        #print('Termo de busca: '+cnome)
        url = "http://localhost:8080/v3/obterinspetor?nome="+cnome+"&limite="+qtdAmostrasAPI+"&metodo=ws"
        jsonstring = get_request_as_json(url)
        inspectors = jsonstring["inspetor"]
        retrieved = []
        relevant = []
        count = 1
        for insp in jsonstring["inspetor"]:
            rname = insp["nome"]
            #print(count, ":", rname, "  ->  ", insp["similaridade"]) 
            retrieved.append(count)
            if pnome in rname and unome in rname:
                relevant.append(count)
            count += 1
        qtd_retornado = str(len(retrieved))
        avg = average_precision(retrieved, relevant)
        #print("-> AvgPrec:  ", avg)

        # Calculo do recall e precision para cada pontos
        recall_list =  recall_at_k(retrieved, relevant)
        precision_list = precision_at_k(retrieved, relevant)
        m = model(nome, cnome, qtd_retornado, avg, relevant, precision_list, recall_list)
        if qtd_retornado == qtdAmostrasAPI:
            lista.append(m)
    mrec_list = obter_recal(lista)
    mpr_list = obter_prec(lista)
    media = media_avg(lista)
    print("-> Quantidade Registros:  ", len(lista))
    print("-> Média AvgPrec:  ", media)
    inf = info(media, mrec_list, mpr_list, lista)
    #convert to JSON string
    with open('base.json', 'w') as outfile:
        js = inf.toJSON()
        outfile.write(js)
    plot_curve_j(mpr_list, mrec_list)

def media_avg(lista:list):
    soma = 0.0
    qtd = len(lista)
    for b in range(0, qtd):
        soma += float(lista[b].avg)
    return soma/qtd

def obter_prec(lista:list):
    media = []
    for a in range(0, len(lista[0].precision_list)):
        soma = 0.0
        qtd = len(lista)
        for b in range(0, qtd):
            soma += lista[b].precision_list[a]
        media.append(soma/qtd)
    return media

def obter_recal(lista:list):
    media = []
    for a in range(0, len(lista[0].recal_list)):
        soma = 0.0
        qtd = len(lista)
        for b in range(0, qtd):
            soma += lista[b].recal_list[a]
        media.append(soma/qtd)
    return media
    
def obter_query(qtdAmostra:str):
    return 'SELECT nome FROM annotation.inspetor LIMIT '+qtdAmostra+';'

def quebra_nome(nome:str, qtdTrocas:int):
    lista = nome.split(' ')
    pnome = lista[0]
    unome = lista[-1]
    cnome = troca_letra(lista[0], qtdTrocas)+' '+troca_letra(lista[-1], qtdTrocas)
    return cnome, pnome, unome

def troca_letra(string:str, qtdTrocas:int):
    for a in range(0, qtdTrocas):
        posicao = random.randrange(0, len(string))
        letra = chr(random.randint(97, 122))
        string = string[:posicao] + letra + string[posicao+1:]
    return string


if __name__ == '__main__':
    main()