#!/usr/bin/python
# coding= utf-8

class ConfigReader:
	
	def __init__(self, file_configurazione):
		self.versione=''
		self.features_scelte=[]
		self.leggi(file_configurazione)
	
	
	def leggi(file_configurazione):
		with open(file_configurazione, 'r') as f:
			intestazione=f.readline().split("\t")
			reader.versione=intestazione[0]
		
			for line in f:
				lista=line.split("\t")
				if lista[0].lower()=='x':
					tupla=tuple([lista[1]]+[lista[2]])
					self.addFeature(tupla, completo)
	
	
	def addFeature(self, stringa):
		self.features_scelte.append(stringa)
		
	def printa(self):
		print vars(self)
