import math

from collections import defaultdict

class Frequencia(object):
    """docstring for Frequencia"""
    def __init__(self):
        self.df = defaultdict(dict)
        self.idf = defaultdict(dict)
        self.tf_idf = defaultdict(dict)


    def getIDF(self):
        return self.idf


    def getTFIDF(self):
        return self.tf_idf


    def calcularDF(self, dicionario, postings):
        """Calculo da frequência de cada termo"""
        for termo in dicionario:
            self.df[termo] = len(postings[termo])
        

    def calcularIDF(self, dicionario, qnt_documentos):
        """Calcular a frequencia invertida"""
        for termo in dicionario:
            if self.df[termo] != 0:
                self.idf[termo] = math.log(qnt_documentos/self.df[termo], 10)
            else:
                self.idf[termo] = 0


    def calcularTFIDF(self, documentos, dicionario, postings):
        qnt_documentos = len(documentos)

        self.calcularDF(dicionario, postings)
        self.calcularIDF(dicionario, qnt_documentos)

        for doc in documentos:
            max_freq = 0
            for termo in dicionario:
                if doc in postings[termo]:
                    if postings[termo][doc] > max_freq:
                        max_freq = postings[termo][doc]
            
            for termo in dicionario:
                if termo in dicionario and doc in postings[termo] \
                and max_freq != 0:
                    self.tf_idf[termo][doc] = (postings[termo][doc]/max_freq) \
                        * self.idf[termo]
                else:
                    self.tf_idf[termo][doc] = 0

        return self.tf_idf