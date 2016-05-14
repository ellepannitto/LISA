#!/usr/bin/python
#coding: utf-8


file_repeated = "../dati/adjClasses/adjs2WNclusters-repeated.txt"
_NBIN = 5.0

def leggi_frequenze (d, m):
	
	freq_cluster = {}
	
	for t, v in d.items():
		pos = t[1]
		
		if t[1][0] == "A" and v>100:
			if t[0] in m:
				
				cluster = m[t[0]]
				
				x = (v*1.0)/len(cluster)
				
				for c in cluster:
					if c in freq_cluster:
						freq_cluster[c]+=x
					else:
						freq_cluster[c]=x
			
	return freq_cluster
	
	
def leggi_mappa (file_input):
	
	mappa={}
	
	with open(file_input) as f:
		for line in f:
			lista=line.split("\t")
			agg=lista[0].split('-')[0]
			clusters=[el.replace("cluster:", '').replace("\n", '') for el in lista[1].split('·')]
			
			
		
			mappa[agg]=clusters


	return mappa


class FiltroCluster:
	def __init__ (self, frequenze):
		mappa = leggi_mappa (file_repeated)
	
		diz = frequenze.dizionario_frequenze

		frequenze_cluster = leggi_frequenze (diz, mappa)

		lista_ordinata = sorted(frequenze_cluster.items(), key=lambda x:x[1])
		
		dim_bin = sum([v for k, v in frequenze_cluster.items()])/_NBIN
		
		bp = []
		
		i=0
		while i<len(lista_ordinata):
			sp =0
			while sp < dim_bin and i<len(lista_ordinata):
				sp+=lista_ordinata[i][1]
				i+=1
				
			#~ print "Dimensione BIN", sp
			bp.append(lista_ordinata[i-1][1])
		
		self.dizionario_frequenze = frequenze_cluster
		
		#~ print self.dizionario_frequenze
		
		self.breakpoint = bp
		
		#~ print bp
