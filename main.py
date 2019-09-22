#!/usr/bin/env python3
import os

from ModeloVetorial import *

indice = ModeloVetorial()

# textos_diretorio = os.path.join(str(os.getcwd()), "textos\\PPGComp_1.html")


indice.criarIndice()
indice.pesquisar("ppgcomp c3 ppgcomp")
# if __name__ == "__main__":
#     main()
