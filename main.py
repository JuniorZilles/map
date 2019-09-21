#!/usr/bin/env python3
import os

from Indice import *

indice = Indice()

textos_diretorio = os.path.join(str(os.getcwd()), "textos\\PPGComp_1.html")

doc = indice.carregarHTML(textos_diretorio)

indice.criarIndice()
# if __name__ == "__main__":
#     main()


def calcSimilaridade(df, idf, docfreq):
	pass



def consulta(termo, ):
	pass