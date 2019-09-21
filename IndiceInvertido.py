import sys
import os


class IndiceInvertido:
    """docstring for IndiceInvertido"""
    def __init__(self, arg):
        #super(IndiceInvertido, self).__init__()
        self.termos = {}
        

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
        pontuacao = " .,-!#$%^&*();:\n\t\\\"|/?!\{\}[]<>+©"
        for i in range(0, len(texto)):
            for j in range(0, len(pontuacao)):
                if texto[i] == pontuacao[j]:
                    texto = texto.replace(pontuacao[j], " ") 

        terms = self.removeStopwords( texto.split() )

        #self.termos = {t.strip(pontuacao) for t in term}
        return terms

    def criarIndice(self):
        textos_diretorio = os.path.join(str(os.getcwd()), "textos")
        for root, dire, file in os.walk(textos_diretorio):
            print(file)
            f = open(file)




