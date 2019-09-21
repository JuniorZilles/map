import sys
import os


class IndiceInvertido:
    """docstring for IndiceInvertido"""
    def __init__(self, arg):
        #super(IndiceInvertido, self).__init__()
        #self.words = words
        pass

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
        
        return text

    def tokenize(self, texto):
        pass

    def criarIndice(self):
        textos_diretorio = os.path.join(str(os.getcwd()), "textos")
        

    def removeStopwords(self, caminho):
        stopwords = open(caminho, "r")
        stopwords = stopwords.split()
