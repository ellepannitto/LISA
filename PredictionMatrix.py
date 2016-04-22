#!/usr/bin/python
# coding= utf-8

class PredictionMatrix:
	def __init__(self, identificatori, tag):
		
		self.gold={}
		self.prediction={}
		self.presence={}
		
		
		for i in range(len(identificatori)):
			self.gold[identificatori[i]]=tag[i]


	def add_fold(self, predicted, ide, k):
		
		for i in range(len(ide)):
			el=ide[i]
			self.prediction[el]=predicted[i]
			self.presence[el]=k

	def stampa_errori(self, file_output):
		
		mappa={1:'ABSTRACT', 2:'ANIMATE', 3:'OBJECT', 4:'LOCATION', 5:'EVENT', 6:'O'}
		
		file_output.write( "ID\tGOLD\tPREDICTED\n" )
		
		for el in self.gold:
			if mappa[self.prediction[el]]!=self.gold[el]:
				file_output.write( el+"\t"+self.gold[el]+"\t"+mappa[self.prediction[el]]+"\n" )
			

