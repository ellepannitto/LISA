#!/usr/bin/python
# coding= utf-8

class AssociazioniFiller:
	def __init__(self, file_associazioni):
		self.listaAssociazioni={}
		self.leggi(file_associazioni)
		
	def leggi(self, file_associazioni):
		with open(file_associazioni, 'r') as f:
			f.readline()
			for line in f:
				self.addDependency(line.split())
				
				
	def addDependency(self, lista):
		lemma=lista[2].split('-')[0]
		chiave=tuple([lemma]+[lista[1].split('_')[0]]+[lista[0].split('-')[0]])
		
		d = Dependency(lista)
		self.listaAssociazioni[chiave] = d
		#~ print "[Associazioni Filler] aggiunto nuovo elemento:", chiave, "=>", d.lemma_dipendente, d.PoS_dipendente, d.frequenza_relativa, d.log_likelihood, d.normalizedLL, d.scaledLL, d.ranking
		#~ m = raw_input ()
		
		
class Dependency:
	def __init__(self, lista):
		self.lemma=lista[2].split('-')[0]
		
		split_tipo=lista[1].split('_')
		
		self.tipo=split_tipo[0]
		self.preposizone=split_tipo[1] if len(split_tipo) >1 else 'X'
		
		dipendente=lista[0].split('-')
		self.lemma_dipendente=dipendente[0]
		self.PoS_dipendente=dipendente[1]
		self.frequenza_relativa=float(lista[3])
		self.log_likelihood=float(lista[4])
		self.normalizedLL=float(lista[5])
		self.scaledLL=float(lista[6]) 
		self.ranking=int(lista[7])
