#!/usr/bin/env python3
import argparse
import os
import sys

from collections import defaultdict

from consulta import Consulta
from indice import Indice


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
        busca = input("Digite a busca: ")
        b = consulta.pesquisar(busca)
        consulta.mostrar_similaridade()

        print(" ")
        print("Questão 4 - RANKING")
        print("--> Pesquisa: ", busca)
        consulta_ranqueada = consulta.ranquear()
        for cons in consulta_ranqueada:
            print(cons[0], "  ", cons[1])


if __name__ == '__main__':
    main()    
