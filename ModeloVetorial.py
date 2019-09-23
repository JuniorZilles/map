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
        self.consulta = set()
        self.frequencia_consulta = defaultdict(dict)
        self.w_consulta = defaultdict(dict)
        self.similaridade = defaultdict(dict)
        self.alpha = alpha

    def mostrarIndiceInvertido(self):
        for termo in self.dicionario:
            print(termo, ": ", self.postings[termo])

    def carregarHTML(self, arquivo):
        """Carregar HTML e remover tags"""
        texto = open(arquivo, "rb")
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
                    #print(self.dfidf[termo][doc])
                else:
                    self.dfidf[termo] = 0

    def calcularSimilaridade(self, termos):
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
            for doc in self.documentos:
                if self.frequencia_consulta[termo] == 0:
                    self.w_consulta[termo][doc] = 0
                else:
                    self.w_consulta[termo][doc] = (self.alpha + \
                        ((((1 - self.alpha) * self.frequencia_consulta[termo])\
                        /max_freq))*self.idf[termo])
                print("freq: ", self.frequencia_consulta[termo])
                print("max_freq ", max_freq)
                print(self.w_consulta[termo])        

        # Calcular similaridade



    def pesquisar(self, busca):
        termos = self.tokenize(busca)
        for termo in termos:
            if termo not in self.dicionario:
                termos.remove(termo)

        busca_unica = set(termos)
        self.consulta = self.consulta.union(busca_unica)
        self.calcularSimilaridade(termos)


    def ranquear(self):
        pass