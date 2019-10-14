import sys
import os
import math
import codecs
from bs4 import BeautifulSoup
from collections import defaultdict

class ModeloVetorial:
    """docstring for IndiceInvertido"""
    def __init__(self, alpha = 0.5):
        self.documentos = []
        self.qnt_documentos = 0
        self.postings    = defaultdict(dict)
        self.dicionario  = set()
        self.df = defaultdict(dict)
        self.idf = defaultdict(dict)
        self.tfidf = defaultdict(dict)
        self.consulta = set()
        self.frequencia_consulta = defaultdict(dict)
        self.w_consulta = defaultdict(dict)
        self.similaridade = defaultdict(dict)
        self.alpha = alpha

    def mostrarIndiceInvertido(self):
        print(" ")
        print("Questão 1 - ÍNDICE")
        print(" ")
        for termo in self.dicionario:
            print(termo, ": ", self.df[termo], " -> ", self.postings[termo])

    def carregarHTML(self, arquivo):
        """Carregar HTML e remover tags"""
        with open(arquivo, "rb") as arq:
            texto = arq.read()

        texto_bs = BeautifulSoup(texto, "html.parser")

        # Remove js scripts
        for script in texto_bs(["script", "style"]):
            script.decompose()
        
        texto = texto_bs.text
        # break into lines and remove leading and trailing space on each
        linhas = (linha.strip() for linha in texto.splitlines())
        # break multi-headlines into a line each
        pedacos = (frase.strip() for linha in linhas for frase in linha.split(" "))
        # drop blank lines
        texto = '\n'.join(pedaco for pedaco in pedacos if pedaco)

        #print(text)
        return texto.lower()

    def removerStopwords(self, palavras, stopwords_arquivo):
        """Remover Stopwords"""
        with codecs.open(stopwords_arquivo, "r", encoding="utf-8") as stopwords:
            sw = stopwords.read()
        
        stopwords_lista = sw.split()

        for stopword in stopwords_lista:
            for palavra in palavras:
                if stopword == palavra:
                    palavras.remove(stopword)
            
        return palavras

    def tokenize(self, texto):
        """Tokenização"""
        pontuacao = " .,-!#$%^&*();:\n\t\\\"|/?!\{\}[]<>+©"
        for i in range(0, len(texto)):
            for j in range(0, len(pontuacao)):
                if texto[i] == pontuacao[j]:
                    texto = texto.replace(pontuacao[j], " ") 

        terms = self.removerStopwords( texto.split(), "stopwords.txt" )

        return terms

    def criarIndice(self):
        pasta_textos = os.path.join(os.getcwd(), "textos")
        for root, dirs, files in os.walk(pasta_textos):
            self.documentos = files
            for file in files:
                abs_file = os.path.join(root, file)
                
                texto  = self.carregarHTML(abs_file)
                termos = self.tokenize(texto)
                self.qnt_documentos += 1
                termos_unicos = set(termos)
                self.dicionario = self.dicionario.union(termos_unicos)

                for termo in termos_unicos:
                    self.postings[termo][file] = termos.count(termo)

        self.calcularDF()
        self.calcularIDF()
        #self.mostrarIndiceInvertido()
        self.calcularTFIDF()

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
        #print(" ")
        #print("Questão 2 - TFIDF")

        for doc in self.documentos:
            max_freq = 0
            for termo in self.dicionario:
                if doc in self.postings[termo]:
                    if self.postings[termo][doc] > max_freq:
                        max_freq = self.postings[termo][doc]
            
            for termo in self.dicionario:
                if termo in self.dicionario and doc in self.postings[termo] \
                and max_freq != 0:
                    self.tfidf[termo][doc] = (self.postings[termo][doc]/max_freq) \
                        * self.idf[termo]
                else:
                    self.tfidf[termo][doc] = 0


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
                    /max_freq))*self.idf[termo])


    def calcularSimilaridade(self):
        for doc in self.documentos:
            soma    = 0
            w_tfidf = 0
            w_cons  = 0
            for termo in self.consulta:
                soma   += (self.w_consulta[termo] * self.tfidf[termo][doc])
                w_cons += (self.w_consulta[termo] * self.w_consulta[termo])

            for termo in self.tfidf:
                w_tfidf += self.tfidf[termo][doc] * self.tfidf[termo][doc]

            self.similaridade[doc] = soma/(math.sqrt(w_tfidf) * math.sqrt(w_cons))

        print(self.similaridade)


    def pesquisar(self, busca):
        termos = self.tokenize(busca)
        for termo in termos:
            if termo not in self.dicionario:
                termos.remove(termo)

        busca_unica = set(termos)
        self.consulta = self.consulta.union(busca_unica)
        self.calcularW(termos)
        self.calcularSimilaridade()


    def ranquear(self):
        pass
