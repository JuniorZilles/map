#!/usr/bin/env python3
import os

from ModeloVetorial import *
from Consulta import Consulta
from Frequencia import Frequencia

indice = ModeloVetorial()
indice.criarIndice()
freq = Frequencia()
freq.calcularTFIDF(indice.getDocumentos(), indice.getDicionario(), indice.getPostings())

consulta = Consulta(indice.getDocumentos(), indice.getDicionario(), freq.getIDF(), freq.getTFIDF())
b = consulta.pesquisar("rei cavalo")
print(b)





##### Observações do Eduardo
# -> Separação em classe:
# --> Documento
# --> Consulta (criar uma variável de Documentos)
# --> Indice
# --> 

# -> Trabalhar com os número e não passa-lôs para palavras
# -> Deve trabalhar com documentos simples
