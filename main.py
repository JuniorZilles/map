#!/usr/bin/env python3
import argparse
import os
import sys

from collections import defaultdict

from consulta import Consulta
from indice import Indice
from metricas import *


def main():
    # local de dos textos html
    # nome do arquivo stopwords
    parser = argparse.ArgumentParser(description="Criação de indice invertido \
        e busca texto por similaridade.")
    parser.add_argument("-d", help = "Define diretório dos textos html")
    parser.add_argument("-s", help = "Define arquivo contendo stopwords")

    args = parser.parse_args()
    local_documentos  = args.__dict__["d"] if args.__dict__["d"] else "textos"
    arquivo_stopwords = args.__dict__["s"] if args.__dict__["s"] else "stopwords.txt"

    # Criação do indice invertido e visualização
    indice = Indice()
    indice.criar_indice(local_documentos, arquivo_stopwords)
    indice.calcular_tfidf()

    if input("Deseja mostrar o indice? ").lower() == "s":
        indice.mostrar_indice()

    # indice.mostrar_tfidf()

    # Inicialização da consulta com os dados calculados
    consulta = Consulta(documentos = indice.get_documentos(), \
                        dicionario = indice.get_dicionario(), \
                        idf        = indice.get_idf(), \
                        tf_idf     = indice.get_tfidf(), \
                        stopwords  = arquivo_stopwords)

    while True:
        busca = input("Digite a busca (\"e\" pra sair): ")
        if busca.lower() == "e":
            exit()
        
        b = consulta.pesquisar(busca)
        consulta.mostrar_similaridade()

        print(" ")
        print("Questão 4 - RANKING")
        print("--> Pesquisa: ", busca)
        consulta_ranqueada = consulta.ranquear()

        # Criação da lista de documentos recuperados 
        # e exibição dos mesmos
        retrieved = []
        count = 1
        for text, value in consulta_ranqueada:
            if value != 0:
                print(count, ":", text, "  ->  ", value) 
                retrieved.append(count)
                count += 1

        relevant = input("\nQuais relevantes? ").split()
        relevant = [int(rel) for rel in relevant]
        

        print("\n### Métricas")
        print("-> Precisão: ", precision(retrieved, relevant))
        print("-> Recall:   ", recall(retrieved, relevant))
        print("-> F1 :      ", f_measure(retrieved, relevant))
        print("-> AvgPrec:  ", average_precision(retrieved, relevant))

        # Calculo do recall e precision para cada pontos
        recall_list =  recall_at_k(retrieved, relevant)
        precision_list = precision_at_k(retrieved, relevant)
        plot_curve(precision_list, recall_list)


if __name__ == '__main__':
    main()    



# TESTE
# Busca:  boi cavalo peão xadrez
# Relevantes: 1 3 8 10 13 24