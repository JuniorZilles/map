import os
import math
from collections import defaultdict

from ProcessaHTML import carregarHTML, tokenize

class Indice:
    """docstring for IndiceInvertido"""
    def __init__(self):
        self.documentos = []
        self.qnt_documentos = 0
        self.postings    = defaultdict(dict)
        self.dicionario  = set()

        self.df = defaultdict(dict)
        self.idf = defaultdict(dict)
        self.tf_idf = defaultdict(dict)


    def getDicionario(self):
        return self.dicionario


    def getDocumentos(self):
        return self.documentos


    def getPostings(self):
        return self.postings


    def getIDF(self):
        return self.idf


    def getTFIDF(self):
        return self.tf_idf

    def mostrarTFIDF(self):
        print(" ")
        print("Questão 2 - TFxIDF")
        print(" ")
        for termo in self.dicionario:
            print("--- ", termo, " ---",)
            for doc in self.documentos:
                print(doc, " ", self.tf_idf[termo][doc])
        print("\n" * 2)

        
    def mostrarIndice(self):
        print(" ")
        print("Questão 1 - ÍNDICE")
        print(" ")
        for termo in self.dicionario:
            print(termo, " -> ", self.postings[termo])
        print("\n" * 2)

    def criarIndice(self, local, arquivo_stopwords):
        pasta_textos = os.path.join(os.getcwd(), local)
        for root, dirs, files in os.walk(pasta_textos):
            self.documentos = files
            for file in files:
                abs_file = os.path.join(root, file)
                texto  = carregarHTML(abs_file)
                termos = tokenize(texto, arquivo_stopwords)
                termos_unicos = set(termos)
                self.dicionario = self.dicionario.union(termos_unicos)

                for termo in termos_unicos:
                    self.postings[termo][file] = termos.count(termo)

        self.qnt_documentos = len(self.documentos)

    def calcularDF(self):
        """Calculo da frequência de cada termo"""
        for termo in self.dicionario:
            self.df[termo] = len(self.postings[termo])
        

    def calcularIDF(self):
        """Calcular a frequencia invertida"""
        for termo in self.dicionario:
            if self.df[termo] != 0:
                self.idf[termo] = math.log(self.qnt_documentos/self.df[termo], 10)
            else:
                self.idf[termo] = 0


    def calcularTFIDF(self):
        if len(self.df) == 0:
            self.calcularDF()
        if len(self.idf) == 0:
            self.calcularIDF()

        for doc in self.documentos:
            max_freq = 0
            for termo in self.dicionario:
                if doc in self.postings[termo]:
                    if self.postings[termo][doc] > max_freq:
                        max_freq = self.postings[termo][doc]
            
            for termo in self.dicionario:
                if termo in self.dicionario and doc in self.postings[termo] \
                and max_freq != 0:
                    self.tf_idf[termo][doc] = (self.postings[termo][doc]/max_freq) \
                        * self.idf[termo]
                else:
                    self.tf_idf[termo][doc] = 0

        return self.tf_idf