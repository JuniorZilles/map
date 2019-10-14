import math
from collections import defaultdict

from ProcessaHTML import tokenize

class Consulta:
    """docstring for Consulta"""
    def __init__(self, documentos, dicionario, idf, tf_idf, stopwords, alpha = 0.5):
        self.frequencia_consulta = defaultdict(dict)
        self.w_consulta = defaultdict(dict)
        self.similaridade = defaultdict(dict)
        self.alpha = alpha

        self.documentos = documentos
        self.arquivo_stopwords = stopwords
        self.dicionario = dicionario
        self.idf        = idf
        self.tf_idf     = tf_idf


    def mostrarSimilaridade(self):
        print(" ")
        print("Questão 3 - SIMILARIDADE DA CONSULTA")
        print(" ")
        for doc in self.documentos:
            print(doc, " -> ", self.similaridade[doc])
        print("\n" * 2)


    def calcularW(self, termos, consulta):
        # Calculo da frequencia de cada palavra na consulta
        for termo in consulta:
            if termo in self.dicionario:
                self.frequencia_consulta[termo] = termos.count(termo)
            else:
                self.frequencia_consulta[termo] = 0

        for termo in consulta:
            # Calculo do peso máximo de cada palavra na pesquisa
            max_freq = 0
            if termo in consulta and termo in self.dicionario:
                if self.frequencia_consulta[termo] > max_freq:
                    max_freq = self.frequencia_consulta[termo]

        # Calculo do peso de cada palavra
        for termo in consulta: 
            if self.frequencia_consulta[termo] == 0:
                self.w_consulta[termo] = 0
            else:
                self.w_consulta[termo] = (self.alpha + \
                    ((((1 - self.alpha) * self.frequencia_consulta[termo])\
                    /max_freq)) * self.idf[termo])


    def calcularSimilaridade(self, consulta):
        for doc in self.documentos:
            soma    = 0
            w_tfidf = 0
            w_cons  = 0
            for termo in consulta:
                soma   += (self.w_consulta[termo] * self.tf_idf[termo][doc])
                w_cons += (self.w_consulta[termo] * self.w_consulta[termo])

            for termo in self.tf_idf:
                w_tfidf += self.tf_idf[termo][doc] * self.tf_idf[termo][doc]

            self.similaridade[doc] = soma/(math.sqrt(w_tfidf) * math.sqrt(w_cons))



    def pesquisar(self, busca):
        consulta = set()
        termos = tokenize(busca, self.arquivo_stopwords)

        termos_no_dicionario = [t for t in termos if t in self.dicionario]

        busca_unica = set(termos_no_dicionario)
        consulta = consulta.union(busca_unica)
        if len(consulta) == 0:
            raise Exception("Busca não consta nos documentos.")

        self.calcularW(termos, consulta)
        self.calcularSimilaridade(consulta)

        return [arq for arq, val in self.similaridade.items() if self.similaridade[arq] != 0]


    def ranquear(self):
        return sorted(self.similaridade.items(), key=lambda k_v: k_v[1], reverse=True)

