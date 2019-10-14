import math

from collections import defaultdict

from ProcessaHTML import tokenize

class Consulta:
    """docstring for Consulta"""
    def __init__(self, documentos, dicionario, idf, tf_idf, alpha = 0.5):
        self.consulta = set()
        self.frequencia_consulta = defaultdict(dict)
        self.w_consulta = defaultdict(dict)
        self.similaridade = defaultdict(dict)
        self.alpha = alpha

        self.documentos = documentos
        self.dicionario = dicionario
        self.idf        = idf
        self.tf_idf     = tf_idf

    def calcularW(self, termos):
        # Calculo da frequencia de cada palavra na consulta
        for termo in self.consulta:
            if termo in self.dicionario:
                self.frequencia_consulta[termo] = termos.count(termo)
            else:
                self.frequencia_consulta[termo] = 0

        for termo in self.consulta:
            # Calculo do peso máximo de cada palavra na pesquisa
            max_freq = 0
            if termo in self.consulta and termo in self.dicionario:
                if self.frequencia_consulta[termo] > max_freq:
                    max_freq = self.frequencia_consulta[termo]

        # Calculo do peso de cada palavra
        for termo in self.consulta: 
            if self.frequencia_consulta[termo] == 0:
                self.w_consulta[termo] = 0
            else:
                self.w_consulta[termo] = (self.alpha + \
                    ((((1 - self.alpha) * self.frequencia_consulta[termo])\
                    /max_freq)) * self.idf[termo])


    def calcularSimilaridade(self):
        for doc in self.documentos:
            soma    = 0
            w_tfidf = 0
            w_cons  = 0
            for termo in self.consulta:
                soma   += (self.w_consulta[termo] * self.tf_idf[termo][doc])
                w_cons += (self.w_consulta[termo] * self.w_consulta[termo])

            for termo in self.tf_idf:
                w_tfidf += self.tf_idf[termo][doc] * self.tf_idf[termo][doc]

            self.similaridade[doc] = soma/(math.sqrt(w_tfidf) * math.sqrt(w_cons))

        print(self.similaridade)


    def pesquisar(self, busca):
        termos = tokenize(busca)

        termos_no_dicionario = [t for t in termos if t in self.dicionario]

        busca_unica = set(termos_no_dicionario)
        self.consulta = self.consulta.union(busca_unica)
        
        self.calcularW(termos)
        self.calcularSimilaridade()

        return [arq for arq, val in self.similaridade.items() if self.similaridade[arq] != 0]


    def ranquear(self):
        return [sorted(self.similaridade.items(), key=lambda k_v: k_v[1], reverse=True)]

