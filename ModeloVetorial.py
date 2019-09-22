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
        self.dfidf = defaultdict(dict)
        self.frequencia_consulta = defaultdict(dict)
        self.w_consulta = defaultdict(dict)
        self.alpha = 0.5

    def carregarHTML(self, arquivo):
        """Carregar HTML e remover tags"""
        texto = open(arquivo, "r")
        t = texto.read()
        texto.close()

        texto_bs = BeautifulSoup(t, "html.parser")
        # Remove js scripts
        for script in texto_bs(["script", "style"]):
            script.decompose()
        
        text = texto_bs.text
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        text = text.lower()

        return text

    def removerStopwords(self, palavras):
        """Remover Stopwords"""
        stopwords = codecs.open("stopwords.txt", "r", encoding="utf-8")
        f = stopwords.read()
        stopwords.close()
        stopwords = f.split()

        for stopword in stopwords:
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

        terms = self.removerStopwords( texto.split() )

        #self.termos = {t.strip(pontuacao) for t in term}
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
        self.calcularDFIDF()

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

    def calcularDFIDF(self):
        self.calcularDF()
        self.calcularIDF()

        for doc in self.documentos:
            max_freq = 0
            for termo in self.dicionario:
                if doc in self.postings[termo]:
                    if self.postings[termo][doc] > max_freq:
                        max_freq = self.postings[termo][doc]
            
            for termo in self.dicionario:
                if termo in self.dicionario and doc in self.documentos \
                and max_freq != 0:
                    self.dfidf[termo][doc] = (self.df[termo]/max_freq) \
                        * self.idf[termo]
                else:
                    self.dfidf[termo] = 0

        for termo in self.dicionario:
            for doc in self.documentos:
                print(self.dfidf[termo][doc])

    def calcularSimilaridade(df, idf, docfreq):
        pass


    def consulta(self, busca):
        busca = tokenize(busca)