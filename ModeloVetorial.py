import sys
import os
import math

from collections import defaultdict

from ProcessaHTML import carregarHTML, tokenize

class ModeloVetorial:
    """docstring for IndiceInvertido"""
    def __init__(self):
        self.documentos = []
        self.qnt_documentos = 0
        self.postings    = defaultdict(dict)
        self.dicionario  = set()


    def getDicionario(self):
        return self.dicionario


    def getDocumentos(self):
        return self.documentos

    def getPostings(self):
        return self.postings

    def mostrarIndiceInvertido(self):
        print(" ")
        print("Questão 1 - ÍNDICE")
        print(" ")
        for termo in self.dicionario:
            print(termo, ": ", self.df[termo], " -> ", self.postings[termo])


    def criarIndice(self, local = "textos"):
        pasta_textos = os.path.join(os.getcwd(), local)
        for root, dirs, files in os.walk(pasta_textos):
            self.documentos = files
            for file in files:
                abs_file = os.path.join(root, file)
                
                texto  = carregarHTML(abs_file)
                termos = tokenize(texto)
                self.qnt_documentos += 1
                termos_unicos = set(termos)
                self.dicionario = self.dicionario.union(termos_unicos)

                for termo in termos_unicos:
                    self.postings[termo][file] = termos.count(termo)