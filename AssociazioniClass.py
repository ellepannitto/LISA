#!/usr/bin/python
# coding= utf-8

class Associazioni:
	def __init__(self, file_associazioni):
		self.listaAssociazioni={}
		self.leggi(file_associazioni)

	def leggi(self, file_associazioni):
		with open(depclass_ass, 'r') as f:
		f.readline()
		for line in f:
			ogg.addDependency(line.split())
	
	def addDependency(self, lista):
		chiave=tuple([lista[1].split('_')[0]]+[lista[0].split('-')[0]])
		if not chiave in self.listaAssociazioni:
			self.listaAssociazioni[chiave]=[]
		self.listaAssociazioni[chiave].append(Dependency(lista))
		
class Dependency:
	def __init__(self, lista):
		split_tipo=lista[1].split('_')
		self.tipo=split_tipo[0]
		self.preposizone=split_tipo[1] if len(split_tipo) >1 else 'X'
		
		ascendente=lista[0].split('-')
		self.lemma_ascendente=ascendente[0]
		self.PoS_ascendente=ascendente[1]
		
		self.LSO=lista[2]
		
		self.frequenza=float(lista[3])
		self.frequenza_relativa=float(lista[4])
