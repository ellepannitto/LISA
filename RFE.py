
import copy
import random

def perform_classification ( gruppi_feature ):
	return random.randint (0,100)

def perform_rfe (gruppi_feature, numero_rimanenti=0):
	
	indici_feature_utilizzate = range (len(gruppi_feature))
	
	if numero_rimanenti <= 0:
		numero_rimanenti = len (gruppi_feature)/2
	
	while len(indici_feature_utilizzate) > numero_rimanenti:
		
		#~ print "nuovo ciclo - feat utilizzate;", indici_feature_utilizzate
		#~ print "che corrisponde a",[ gruppi_feature[i] for i in indici_feature_utilizzate ]
		statistiche = []
		
		for indice in indici_feature_utilizzate:
			indici_feature_per_classificazione = copy.deepcopy (indici_feature_utilizzate)
			indici_feature_per_classificazione.remove (indice)
			
			
			gruppi_per_classificazione = [ gruppi_feature[i] for i in indici_feature_per_classificazione ]
			
			res = perform_classification ( gruppi_per_classificazione )
			
			#~ print "rimuovo", indice, "uso", gruppi_per_classificazione, "risultato", res
			
			statistiche.append (res)
		
		#~ print "statistiche:", statistiche
		
		massimo = max (statistiche)
		indice_da_rimuovere = statistiche.index (massimo)
		indici_feature_utilizzate.remove (indice_da_rimuovere)
		
		#~ print "rimuovo",indice_da_rimuovere
		#~ m = raw_input ()
		
		
gruppi = ['a','b','c','d','e','f','g']
perform_rfe (gruppi)
