#!/usr/bin/env python3
import os

from IndiceInvertido import *

indice = IndiceInvertido(1)

textos_diretorio = os.path.join(str(os.getcwd()), "textos\\PPGComp_1.html")

indice.carregarHTML(textos_diretorio)

print(indice)

# if __name__ == "__main__":
#     main()