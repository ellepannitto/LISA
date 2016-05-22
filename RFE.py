#!/usr/bin/python
#coding: utf-8 

import copy
import random
import scipy.sparse
import numpy as np

from multiprocessing.pool import ThreadPool
import threading

import Statistics as ST
import Classifier as CL
import Dumper

def normalizza(tags):
	mappa_sensi={'ABSTRACT':1, 'ANIMATE':2, 'OBJECT':3, 'LOCATION':4, 'EVENT':5, 'O':6}
	
	ret=[]
	
	for el in tags:
		ret.append(mappa_sensi[el])
		
	return np.array(ret)
		
		
def salva_stato (file_start_from, indici_feature_utilizzate, ultimo_indice_rimosso, row, matrix=None):
	with open (file_start_from, "w") as fout:
		prima_riga = "\t".join ( [str(i) for i in indici_feature_utilizzate])
		seconda_riga = str (ultimo_indice_rimosso)
		fout.write (prima_riga + "\n")
		fout.write (seconda_riga + "\n")
	
	Dumper.binary_dump (row, file_start_from+"_statistics_row")
	if matrix is not None: 
		Dumper.binary_dump (matrix, file_start_from+"_statistics_matrix")

class RFE:
	
	def __init__(self, target, identifiers, file_start_from=None):
		self.target = normalizza(target)
		self.ide = identifiers
		self.nomi_feature=[]
		self.gruppi_feature=[]
		self.file_start_from = file_start_from

	def get_nomi_feature (self, indici):
		ret = [ self.nomi_feature[i] for i in indici ]
		#~ print "valore restituito", ret
		
		return ret

	def perform_classification ( self, gruppi_feature ):
		
		matrice = scipy.sparse.hstack(gruppi_feature)
		clf = CL.Classifier (matrice, self.target, self.ide)
		scores = clf.perform()
		
		return scores
	
	def get_classifier_for_groups ( self, gruppi_feature ):
		
		matrice = scipy.sparse.hstack(gruppi_feature)
		target = copy.deepcopy (self.target)
		ide = copy.deepcopy (self.ide)
		
		clf = CL.Classifier (matrice, target, ide)
		
		return clf
	
	def perform_dict (self, dict_gruppi):
		
		self.nomi_feature=[]
		self.gruppi_feature=[]
		
		
		for el in dict_gruppi:
			self.nomi_feature.append (el)
			self.gruppi_feature.append (dict_gruppi[el])		
		
		res = self.perform_rfe( self.gruppi_feature )
			
	def perform_rfe (self, gruppi_feature, numero_rimanenti=1):

		tutte_le_feature = range (len(gruppi_feature))
				
		#se è stato specificato un file per riprendere la computazione da dve era stata interrotta, ricalcolo lo stato
		if self.file_start_from is None:
			indici_feature_utilizzate = tutte_le_feature
			
			#se bisogna riniziare da capo, fa la prima classificazione con tutte le feature
			
			#~ print "eseguo prima classificazione"
			#~ gruppi_per_classificazione = [ gruppi_feature[i] for i in indici_feature_utilizzate ]
			#~ res = self.perform_classification ( gruppi_per_classificazione )
			res = [0.74468663,0.74623218,0.75037339,0.74818336,0.74662139]
			print "prima classificazione - risultato:", res
			statistica = ST.Statistic (self.get_nomi_feature (indici_feature_utilizzate), res)
		
			indice_da_rimuovere = -1
		
			self.statistics_matrix = [[statistica]]
			
		else:
			with open ( self.file_start_from ) as fin:
				prima_riga = fin.readline ()
				indici_feature_utilizzate = [ int (i) for i in prima_riga.split ("\t") ]
				seconda_riga = fin.readline ()
				i = int (seconda_riga)
				posizione_ultimo_indice_rimosso = indici_feature_utilizzate.index(i)
				indice_da_rimuovere = indici_feature_utilizzate [ posizione_ultimo_indice_rimosso + 1 ] if posizione_ultimo_indice_rimosso < len(indici_feature_utilizzate)-1 else -1
				print "DEBUG: riparto con feature", indici_feature_utilizzate, "rimuovendo", indice_da_rimuovere
				print "che si chiama (a meno che non sia -1)", self.nomi_feature[indice_da_rimuovere]
				
				#ricarica le statistiche delle classificazioni avvenute prima di interrompere RFE
				statistics_row = Dumper.binary_load ( self.file_start_from + "_statistics_row" )
				self.statistics_matrix = Dumper.binary_load ( self.file_start_from + "_statistics_matrix" )
		

		indici_feature_rimosse = list ( set(tutte_le_feature)- set (indici_feature_utilizzate) )
		
		if numero_rimanenti <= 0:
			numero_rimanenti = len (gruppi_feature)/2
		
		while len(indici_feature_utilizzate) > numero_rimanenti:
			
			
			if indice_da_rimuovere == -1 :
				print "nuovo ciclo - \n\tfeat utilizzate:", [self.nomi_feature[i] for i in indici_feature_utilizzate]
				print "\tfeat non utilizzate:", [self.nomi_feature[i] for i in indici_feature_rimosse]

				statistics_row = []
			
			#~ pool = ThreadPool (processes=len(indici_feature_utilizzate))
			pool = ThreadPool (processes=8)
			future_results = []
			classifiers = []
			
			
			start = 0 if indice_da_rimuovere == -1 else indici_feature_utilizzate.index (indice_da_rimuovere)
			end = len (indici_feature_utilizzate)
			
			#lancia un thread per ogni indice da eliminare
			for i in range (start, end):
				
				indice = indici_feature_utilizzate [i]
				
				indici_feature_per_classificazione = copy.deepcopy (indici_feature_utilizzate)
				indici_feature_per_classificazione.remove (indice)
				
				gruppi_per_classificazione = [ gruppi_feature[i] for i in indici_feature_per_classificazione ]
				
				C = self.get_classifier_for_groups ( gruppi_per_classificazione )
				
				print "starting thread for",self.nomi_feature[indice]
				async_result = pool.apply_async ( C.perform_dummy )
				future_results.append (async_result)
				
			
			#recupera i risultati delle computazioni
			j=0
			for i in range (start, end):
				
				indice = indici_feature_utilizzate [i]
				
				print "getting result for",self.nomi_feature[indice]
				res = future_results[j].get()
				j+=1
				print "rimuovo", self.nomi_feature[indice], "risultato", res				
				
				statistica = ST.Statistic (self.get_nomi_feature (indici_feature_per_classificazione), res)
				statistics_row.append ( statistica )
				
				salva_stato ("start_from", indici_feature_utilizzate, indice, statistics_row)

			
			#~ print "statistiche:", statistiche
			
			indice_da_rimuovere = indici_feature_utilizzate[ST.find_better_result_index (statistics_row)]
			indici_feature_utilizzate.remove (indice_da_rimuovere)
			
			self.statistics_matrix.append (statistics_row)
			
			indici_feature_rimosse.append(indice_da_rimuovere)
			#~ print "rimuovo",indice_da_rimuovere
			#~ m = raw_input ()
			
			ultimo = indici_feature_utilizzate [-1]
			
			salva_stato ("start_from", indici_feature_utilizzate, ultimo, statistics_row, self.statistics_matrix)
			
			indice_da_rimuovere = -1
			
			
