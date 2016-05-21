
import copy
import random
import scipy.sparse
import numpy as np

import Statistics as ST
import Classifier as CL

def normalizza(tags):
	mappa_sensi={'ABSTRACT':1, 'ANIMATE':2, 'OBJECT':3, 'LOCATION':4, 'EVENT':5, 'O':6}
	
	ret=[]
	
	for el in tags:
		ret.append(mappa_sensi[el])
		
	return np.array(ret)
		
class RFE:
	
	def __init__(self, target, identifiers):
		self.target = normalizza(target)
		self.ide = identifiers
		self.nomi_feature=[]
		self.gruppi_feature=[]

	def get_nomi_feature (self, indici):
		ret = [ self.nomi_feature[i] for i in indici ]
		#~ print "valore restituito", ret
		
		return ret

	def perform_classification ( self, gruppi_feature ):
		
		matrice = scipy.sparse.hstack(gruppi_feature)
		clf = CL.Classifier (matrice, self.target, self.ide)
		scores = clf.perform()
		
		return scores
		
	def perform_dict (self, dict_gruppi):
		
		self.nomi_feature=[]
		self.gruppi_feature=[]
		
		
		for el in dict_gruppi:
			self.nomi_feature.append (el)
			self.gruppi_feature.append (dict_gruppi[el])		
		
		
		res = self.perform_rfe( self.gruppi_feature )
		
	
	def perform_rfe (self, gruppi_feature, numero_rimanenti=1):
		
		indici_feature_utilizzate = range (len(gruppi_feature))
		indici_feature_rimosse = []
		
		if numero_rimanenti <= 0:
			numero_rimanenti = len (gruppi_feature)/2
		
		
		
		gruppi_per_classificazione = [ gruppi_feature[i] for i in indici_feature_utilizzate ]
		
		res = self.perform_classification ( gruppi_per_classificazione )
		
		#~ print "rimuovo", indice, "risultato", res
		
		print "prima classificazione - risultato:", res
		
		statistica = ST.Statistic (self.get_nomi_feature (indici_feature_utilizzate), res)
		
		self.statistics_matrix = [statistica]
		#~ self.statistics_matrix = []

		
		while len(indici_feature_utilizzate) > numero_rimanenti:
			
			print "nuovo ciclo - \n\tfeat utilizzate:", [self.nomi_feature[i] for i in indici_feature_utilizzate]
			print "\tfeat non utilizzate:", [self.nomi_feature[i] for i in indici_feature_rimosse]
			
			#~ print "che corrisponde a",[ gruppi_feature[i] for i in indici_feature_utilizzate ]
			statistics_row = []
			
			for indice in indici_feature_utilizzate:
				
				indici_feature_per_classificazione = copy.deepcopy (indici_feature_utilizzate)
				indici_feature_per_classificazione.remove (indice)
				
				
				gruppi_per_classificazione = [ gruppi_feature[i] for i in indici_feature_per_classificazione ]
				
				res = self.perform_classification ( gruppi_per_classificazione )
				
				print "rimuovo", self.nomi_feature[indice], "risultato", res
				
				statistica = ST.Statistic (self.get_nomi_feature (indici_feature_per_classificazione), res)
				
				statistics_row.append ( statistica )
			
			#~ print "statistiche:", statistiche
			
			indice_da_rimuovere = ST.find_better_result_index (statistics_row)
			indici_feature_utilizzate.remove (indice_da_rimuovere)
			
			self.statistics_matrix.append (statistics_row)
			
			indici_feature_rimosse.append(indice_da_rimuovere)
			
			#~ print "rimuovo",indice_da_rimuovere
			#~ m = raw_input ()
		
