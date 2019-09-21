import sys
import os


class IndiceInvertido(object):
	"""docstring for IndiceInvertido"""
	def __init__(self, arg):
		super(IndiceInvertido, self).__init__()
		self.arg = arg


	def readHTML(self):
		from bs4 import BeautifulSoup
		textos_diretorio = os.path.join(str(os.getcwd()), "textos")

		textos = []

		# Remove HTML tags
		for arquivo in os.walk(textos_diretorio):
			texto = open(arquivo, "r")
			texto = BeautifulSoup(texto)
			textos.append(texto)
