#!/usr/bin/python
# coding= utf-8

class Repubblica:
	
	def __init__(self, file_frequenze):
		self.massima_frequenza=0
		self.dizionario_frequenze={}
		self.dizionario_cumulato={}
		self.calcola_frequenze (file_frequenze)
		


	def calcola_frequenze(self, file_frequenze):
		with open(file_frequenze, 'r') as f:
			for line in f:
				l=line.split("\t")
				tupla=tuple([l[0]]+[l[1]])
				self.dizionario_frequenze[tupla]=int(l[2])
				self.dizionario_cumulato[l[0]]=int(l[2]) if not l[0] in self.dizionario_cumulato else self.dizionario_cumulato[l[0]]+int(l[2])
				
				if self.dizionario_cumulato[l[0]]>self.massima_frequenza:
					self.massima_frequenza=self.dizionario_cumulato[l[0]]
		
