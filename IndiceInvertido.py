import sys
import os
import math

from collections import defaultdict

class IndiceInvertido:
    """docstring for IndiceInvertido"""
    def __init__(self):
        self.documentos = []
        self.qnt_documentos = 0
        self.postings    = defaultdict(dict)
        self.dicionario  = set()
        self.df = defaultdict(dict)
        self.idf = defaultdict(dict)

    def carregarHTML(self, arquivo):
        """Carregar HTML e remover tags"""
        from bs4 import BeautifulSoup

        # Remove HTML tags
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

    def removeStopwords(self, palavras):
        """Remover Stopwords"""
        import codecs
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

        terms = self.removeStopwords( texto.split() )

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


    def calcDF(self):
        """Calculo da frequência de cada termo"""
        for termo in self.dicionario:
            self.df[termo] = len(self.postings[termo])


    def calcIDF(self):
        """Calcular a frequencia invertida"""
        for termo in self.dicionario:
            self.idf = math.log(qnt_documentos/self.df[termo], 10)

    def calcDFIDF(self):
        pass