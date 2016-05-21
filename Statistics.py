#!/usr/bin/python
#coding: utf-8 

class Statistic:
	
	def __init__ (self, feature_utilizzate, results ):
		
		self.feature_utilizzate = feature_utilizzate
		self.results = results
		
		#~ print "[STATISTICHE]Prova con feature:",sorted(feature_utilizzate)
		#~ print "[STATISTICHE] risultati:", results

	def get_result (self):
		
		return sum(self.results)/len(self.results)
	
	
def find_better_result_index ( stats_list ):
	''' data una lista di statistiche, restituisce l'indice di quella con risultato migliore '''
	
	idx = 0
	better = stats_list[0].get_result()
	#~ print better, idx
	
	for i in range (1,len(stats_list)): 
		
		#~ print stats_list[i].get_result(), i
		#~ print "corrente better", better
		
		if stats_list[i].get_result () > better:
			idx = i
			better = stats_list[i].get_result()
			
	
	return idx
	

#~ if __name__=="__main__":
	#~ l = []
	#~ l.append ( Statistic ([], [0.,0.,0.]) )
	#~ l.append ( Statistic ([], [10.,0.,0.]) )
	#~ l.append ( Statistic ([], [4.,4.,4.]) )
	#~ l.append ( Statistic ([], [1.,2.,0.]) )
	#~ l.append ( Statistic ([], [0.,0.,0.]) )
	
	#~ print find_better_result_index(l)
