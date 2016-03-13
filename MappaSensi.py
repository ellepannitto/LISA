#!/usr/bin/python
# coding= utf-8

class MappaSensi:
	
	def __init__(self, file_mappa):
		self.mappa={}
		self.leggi(file_mappa)
		
	def leggi(self, file_mappa):
		with open(file_mappa, 'r') as f:
		
			for line in f:
				l=line.split("\t")
				lemma=l[0][:-2]
				lso=l[1][:-1].split("·")
				self.mappa[lemma]=lso
