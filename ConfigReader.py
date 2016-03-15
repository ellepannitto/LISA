#!/usr/bin/python
# coding= utf-8

class ConfigReader:
	"""
	Legge un file di configurazione per capire quali feature vanno stampate (e il tipo corrispondente) e le memorizza
	"""
	
	def __init__(self, file_configurazione):
		"""
		Costruttore di default:
		 memorizza le features leggendole dal file passate come parametro
		"""
		self.versione=''
		self.features_scelte=[]
		self.leggi(file_configurazione)
	
	
	def leggi(self, file_configurazione):
		"""
		Aggiunge alla lista di feature quelle lette dal file passate come parametro
		"""
		with open(file_configurazione, 'r') as f:
			intestazione=f.readline().split("\t")
			self.versione=intestazione[0]
		
			for line in f:
				lista=line.split("\t")
				if lista[0].lower()=='x':
					tupla=tuple([lista[1]]+[lista[2]])
					self.addFeature(tupla)
	
	
	def addFeature(self, tupla):
		"""
		Aggiunge una singola feature, passata come parametro.
		 la feature è una tupla (nome,tipo), con nome e tipo stringhe
		"""
		self.features_scelte.append(tupla)
		
	def dump(self):
		"""
		Stampa le lette, utile per il debug
		"""
		print vars(self)
