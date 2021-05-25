from metricas import *
from request import *
from database import *
from utils import *
import pandas as pd
import random
import json
import time

from model import *
def evaluation():
    qtdTrocas = int(input("Trocar quantos caracteres de cada palavra? "))
    qtdAmostrasBD = int(input("Quantidade de amostras do banco? "))
    qtdAmostrasAPI = input("Quantidade de amostras da API? ")
    metodoAPI = input("Metodo de consulta da API(lv/sws/ws/s/lk/eq), se for mais de um colocar espaço, máximo 5? ").lower()
    inicio = time.time()
    lista_metodos = metodoAPI.split(' ')
    query = obter_query(qtdAmostrasBD+1000)
    rows = get_database_rows(query)
    df = pd.DataFrame(rows)
    dic1 = { x:[] for x in lista_metodos}
    tempos_geral = []
    tempos_processamento = []
    for o in range(2,qtdTrocas+1):
        dic = { x:[[], [], False] for x in lista_metodos}
        for i in df.index:
            nome = df[0][i]
            #print('Termo de original: '+nome + ', posição:' + str(i))
            cnome, pnome, unome = quebra_nome(nome.strip(), o)
            #print('Termo de busca: '+cnome)
            
            for b in lista_metodos:
                inicio_api = time.time()
                url = "http://localhost:8080/inspector?name="+cnome+"&limit="+qtdAmostrasAPI+"&method="+b
                inicio_api = time.time()
                jsonstring = get_request_as_json(url)
                fim_api = time.time() - inicio_api
                retrieved = []
                relevant = []
                count = 1
                #print(jsonstring)
                if 'inspetor' in jsonstring:
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
                
                if len(dic[b][0]) < qtdAmostrasBD:
                    dic[b][0].append(m)
                    dic[b][1].append(fim_api)
                    dic1[b].append(fim_api)
                else:
                    dic[b][2] = True
                tempos_geral.append(fim_api)
                fim_processa = time.time() - inicio_api
                tempos_processamento.append(fim_processa)
            count = 0
            for k in dic:
                if dic[k][2]:
                    count += 1
            if count == len(lista_metodos):
                break
        list_exe = []
        for k in dic:
            mrec_list_1 = obter_recal(dic[k][0])
            mpr_list_1 = obter_prec(dic[k][0])
            media_1 = media_avg(dic[k][0])
            print("-> Método: ", k)
            print("-> Quantidade Registros: ", len(dic[k][0]))
            print("-> Média AvgPrec:  ", media_1)
            print("Tempo médio de execução das requisições: " + str(sum(dic[k][1]) / len(dic[k][1])) + " segundos")
            inf = info(media_1, mrec_list_1, mpr_list_1, dic[k][0], k)
            list_exe.append(inf)
            #convert to JSON string
            with open('proc_'+k+'_2.json', 'w') as outfile:
                js = inf.toJSON()
                outfile.write(js)
        plot_curve_j3(list_exe, str(o))
        dic = None
    for l in dic1:
        print("-> Método: ", l)
        print("Tempo médio de execução das requisições: " + str(sum(dic1[l]) / len(dic1[l])) + " segundos")
    fim = time.time()
    print("Tempo de execução Total: " + str(fim - inicio) + " segundos")
    print("Tempo médio de execução geral: " + str(sum(tempos_geral) / len(tempos_geral)) + " segundos")
    print("Tempo médio de processamento de cada requisição: " + str(sum(tempos_processamento) / len(tempos_processamento)) + " segundos")
    
def geraGrafico():
    list_exe = []
    trc = int(input("Gráfico de quantas trocas? "))
    with open("proc_lv_"+str(trc)+".json") as json_file:
        data = json.load(json_file)
        inf = info(data['media_avg'], data['media_recal'], data['media_precision'], None, data['method'])
        list_exe.append(inf)
    with open("proc_sws_"+str(trc)+".json") as json_file:
        data = json.load(json_file)
        inf = info(data['media_avg'], data['media_recal'], data['media_precision'], None, data['method'])
        list_exe.append(inf)
    with open("proc_ws_"+str(trc)+".json") as json_file:
        data = json.load(json_file)
        inf = info(data['media_avg'], data['media_recal'], data['media_precision'], None, data['method'])
        list_exe.append(inf)
    with open("proc_s_"+str(trc)+".json") as json_file:
        data = json.load(json_file)
        inf = info(data['media_avg'], data['media_recal'], data['media_precision'], None, data['method'])
        list_exe.append(inf)
    plot_curve_j3(list_exe, str(trc))
    
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
    f_t_s = open("register_s.txt", "r")
    f_t_ws = open("register_ws.txt", "r")
    f_t_sws = open("register_sws.txt", "r")
    f_t_lv = open("register_lv.txt", "r")
    t_s = f_t_s.read().strip().split(';')
    t_s = [int(x) for x in t_s if x != '']
    t_ws = f_t_ws.read().strip().split(';')
    t_ws = [int(x) for x in t_ws if x != '']
    t_sws = f_t_sws.read().strip().split(';')
    t_sws = [int(x) for x in t_sws if x != '']
    t_lv = f_t_lv.read().strip().split(';')
    t_lv = [int(x) for x in t_lv if x != '']
    t_g = t_s + t_ws + t_sws + t_lv
    print("Tempo médio de execução das requisições ws: "+str(sum(t_ws)/len(t_ws))+"ms")
    print("Tempo médio de execução das requisições s: "+str(sum(t_s)/len(t_s))+"ms")
    print("Tempo médio de execução das requisições lv: "+str(sum(t_lv)/len(t_lv))+"ms")
    print("Tempo médio de execução das requisições sws: "+str(sum(t_sws)/len(t_sws))+"ms")
    print("Tempo médio de execução de todas as requisições: "+str(sum(t_g)/len(t_g))+"ms")
def main():
    option = int(input("O que deseja fazer? 1 - realizar os testes; 2 - calcular os tempos; 3 - gerar gráfico; "))
    if option == 1:
        evaluation()
    elif option == 2:
        calcula_media_tempos()
    elif option == 3:
        geraGrafico()


if __name__ == '__main__':
    main()