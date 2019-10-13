#!/usr/bin/env python3
import os

from ModeloVetorial import *

indice = ModeloVetorial()

# textos_diretorio = os.path.join(str(os.getcwd()), "textos\\PPGComp_1.html")


indice.criarIndice()
indice.pesquisar("cavalo")
#indice.mostrarIndiceInvertido()
# if __name__ == "__main__":
#     main()



##### Observações do Eduardo
# -> Separação em classe:
# --> Documento
# --> Consulta (criar uma variável de Documentos)
# --> Indice
# --> 

# -> Trabalhar com os número e não passa-lôs para palavras
# -> Deve trabalhar com documentos simples
