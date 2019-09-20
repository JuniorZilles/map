import sys
import os

from bs4 import BeautifulSoup


class Documento(object):
	"""docstring for Documento"""
	def __init__(self, arg):
		super(Documento, self).__init__()
		self.arg = arg


	def readHTML(self):
		textos_diretorio = os.path.join(os.getcwd(), "textos")

		textos = []

		# Remove HTML tags
		for arquivo in os.walk(textos_diretorio):
			texto = open(arquivo, "r")
			texto = BeautifulSoup(texto)
			textos.append(texto)
