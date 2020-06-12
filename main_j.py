from metricas import *
from request import *
from database import *
import pandas as pd
import random
import json
import time

from model import *

def evaluation():
    qtdTrocas = int(input("Trocar quantos caracteres de cada palavra? "))
    qtdAmostrasBD = int(input("Quantidade de amostras do banco? "))
    qtdAmostrasAPI = input("Quantidade de amostras da API? ")
    metodoAPI = input("Metodo de consulta da API(ws/s/lk/eq), se for mais de um colocar espaço, máximo 2? ").lower()
    inicio = time.time()
    lista_metodos = metodoAPI.split(' ')
    query = obter_query(qtdAmostrasBD+100)
    rows = get_database_rows(query)
    df = pd.DataFrame(rows)
    lista_1 = []
    lista_2 = []
    tempos_1 = []
    tempos_2 = []
    tempos_geral = []
    tempos_processamento = []
    for i in df.index:
        nome = df[0][i]
        #print('Termo de original: '+nome + ', posição:' + str(i))
        cnome, pnome, unome = quebra_nome(nome.strip(), qtdTrocas)
        #print('Termo de busca: '+cnome)
        
        for b in lista_metodos:
            inicio_api = time.time()
            url = "http://localhost:8080/v3/inspector?name="+cnome+"&limit="+qtdAmostrasAPI+"&method="+b
            inicio_api = time.time()
            jsonstring = get_request_as_json(url)
            fim_api = time.time() - inicio_api
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
                if b == lista_metodos[0] and len(lista_1) < qtdAmostrasBD:
                    lista_1.append(m)
                    tempos_1.append(fim_api)
                elif b == lista_metodos[1] and len(lista_2) < qtdAmostrasBD:
                    lista_2.append(m)
                    tempos_2.append(fim_api)
                tempos_geral.append(fim_api)
                fim_processa = time.time() - inicio_api
                tempos_processamento.append(fim_processa)
        if len(lista_1) == qtdAmostrasBD and len(lista_2) == qtdAmostrasBD:
            break
    mrec_list_1 = obter_recal(lista_1)
    mpr_list_1 = obter_prec(lista_1)
    media_1 = media_avg(lista_1)
    print("-> Quantidade Registros(1): ", len(lista_1))
    print("-> Média AvgPrec(1):  ", media_1)
    inf = info(media_1, mrec_list_1, mpr_list_1, lista_1)
    #convert to JSON string
    with open('base_'+lista_metodos[0]+'.json', 'w') as outfile:
        js = inf.toJSON()
        outfile.write(js)
    if len(lista_metodos) == 2:
        mrec_list_2 = obter_recal(lista_2)
        mpr_list_2 = obter_prec(lista_2)
        media_2 = media_avg(lista_2)
    
        print("-> Quantidade Registros(2):  ", len(lista_2))
        print("-> Média AvgPrec(2):  ", media_2)
        inf = info(media_2, mrec_list_2, mpr_list_2, lista_2)
        #convert to JSON string
        with open('base_'+lista_metodos[1]+'.json', 'w') as outfile:
            js = inf.toJSON()
            outfile.write(js)
        plot_curve_j2(mpr_list_1, mrec_list_1, mpr_list_2, mrec_list_2, lista_metodos[0], lista_metodos[1])
    else:
        plot_curve_j1(mpr_list_1, mrec_list_1, lista_metodos[0])
    fim = time.time()
    print("Tempo de execução Total: " + str(fim - inicio) + " segundos")
    print("Tempo médio de execução das requisições "+lista_metodos[0]+": " + str(sum(tempos_1) / len(tempos_1)) + " segundos")
    print("Tempo médio de execução das requisições "+lista_metodos[1]+": " + str(sum(tempos_2) / len(tempos_2)) + " segundos")
    print("Tempo médio de execução geral "+lista_metodos[0]+" e "+lista_metodos[1]+": " + str(sum(tempos_geral) / len(tempos_geral)) + " segundos")
    print("Tempo médio de processamento de cada requisição: " + str(sum(tempos_processamento) / len(tempos_processamento)) + " segundos")
    

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
    
def obter_query(qtdAmostra:int):
    return 'SELECT nome FROM annotation.inspetor LIMIT '+str(qtdAmostra)+';'

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
def calcula_media_tempos():
    f_t_s = open("tempos_s.txt", "r")
    f_t_ws = open("tempos_ws.txt", "r")
    t_s = f_t_s.read().strip().split(';')
    t_s = [int(x) for x in t_s if x != '']
    t_ws = f_t_ws.read().strip().split(';')
    t_ws = [int(x) for x in t_ws if x != '']
    t_g = t_s + t_ws
    print("Tempo médio de execução das requisições ws: "+str(sum(t_ws)/len(t_ws))+"ms")
    print("Tempo médio de execução das requisições s: "+str(sum(t_s)/len(t_s))+"ms")
    print("Tempo médio de execução de todas as requisições: "+str(sum(t_g)/len(t_g))+"ms")
def main():
    option = int(input("O que deseja fazer? 1 - realizar os testes; 2 - calcular os tempos; "))
    if option == 1:
        evaluation()
    elif option == 2:
        calcula_media_tempos()


if __name__ == '__main__':
    main()