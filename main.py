#!/usr/bin/env python3
import os
import sys
import argparse
from collections import defaultdict

from Indice import Indice
from Consulta import Consulta


def main():
    # local de dos textos html
    # nome do arquivo stopwords
    parser = argparse.ArgumentParser(description="Criação de indice invertido \
        e busca texto por similaridade.")
    parser.add_argument("-d", help = "Define diretório dos textos html")
    parser.add_argument("-s", help = "Define arquivo contendo stopwords")
    parser.add_argument("-b", help = "Busca por palavras. NECESSÁRIO USO DE ASPAS")

    args = parser.parse_args()
    local_documentos  = args.__dict__["d"] if args.__dict__["d"] else "textos"
    arquivo_stopwords = args.__dict__["s"] if args.__dict__["s"] else "stopwords.txt"
    busca             = args.__dict__["b"] 

    # Criação do indice invertido e visualização
    indice = Indice()
    indice.criarIndice(local_documentos, arquivo_stopwords)
    indice.calcularTFIDF()
    indice.mostrarIndice()

    indice.mostrarTFIDF()

    # Inicialização da consulta com os dados calculados
    consulta = Consulta(documentos = indice.getDocumentos(), \
                        dicionario = indice.getDicionario(), \
                        idf        = indice.getIDF(), \
                        tf_idf     = indice.getTFIDF(), \
                        stopwords  = arquivo_stopwords)

    b = consulta.pesquisar(busca)

    consulta.mostrarSimilaridade()

    print(" ")
    print("Questão 2 - TFxIDF")
    print(" ")
    consulta_ranqueada = consulta.ranquear()
    print(consulta_ranqueada)
    for c in consulta_ranqueada:
        print(c[0], "  ", c[1])



if __name__ == '__main__':
    main()
