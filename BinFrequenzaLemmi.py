#!/usr/bin/python
# coding= utf-8

import math

import Repubblica as R

_NBIN = 10

def log(n):
	return int(round(math.log(n, 10)))

def dividi_bin(lista_ord, d):
	indici=[]
	
	i=0
	while i<len(lista_ord): 
		sp=0
		while sp < d and i<len(lista_ord):
			#~ print sort_sostantivi[i]
			#~ m=raw_input()
			sp+=lista_ord[i][1]
			i+=1
			
		indici.append(i-1)
		
	print indici

	#~ for i in range(len(indici)):
		
		#~ idx = indici[i]
		
		#~ print sort_sostantivi[idx]
		
		#~ while lista_ord[idx][1]==lista_ord[idx-1][1]:
			#~ idx-=1
			
		#~ indici[i]=idx


	print indici
	
	breakpoint_frequenze=[]
	
	#~ for i in range(len(indici)):
		#~ a=indici[i-1]
		#~ b=indici[i] if i < len(indici) else len(lista_ord)
		
		#~ print sum([el[1] for el in lista_ord[a:b]])
	
	for idx in indici:	
		f = lista_ord[idx][1]
		
		breakpoint_frequenze.append(f)
	
	#~ print breakpoint_frequenze
	
	return breakpoint_frequenze
	

def main():
	file_repubblica = "../dati/repubblicaFreqs/sorted.repubblica.sensitive.lemmasAndPos"
	
	frequenze = R.Repubblica(file_repubblica)
	
	frequenze_sostantivi = {}
	frequenze_dip = {}
	frequenze_aggettivi = {}
	
	for el,v in frequenze.dizionario_frequenze.items():
		pos = el[1]
		
		if v>100:
			if pos[0]=="S":
				frequenze_sostantivi[el]=v
				frequenze_dip[el]=v
				
			if pos[0]=="V":
				frequenze_dip[el]=v
			
			if pos[0]=="A":
				frequenze_aggettivi[el]=v
	
	sort_sostantivi = sorted(frequenze_sostantivi.items(), key= lambda x: x[1], reverse=True)
	sort_dip = sorted(frequenze_dip.items(), key= lambda x: x[1], reverse=True)
	sort_aggettivi = sorted(frequenze_aggettivi.items(), key= lambda x: x[1], reverse=True)

	dimensione_bin_sostantivi = sum([v for el,v in frequenze_sostantivi.items()])/_NBIN
	dimensione_bin_dip = sum([v for el,v in frequenze_dip.items()])/_NBIN
	dimensione_bin_aggettivi = sum([v for el,v in frequenze_dip.items()])/_NBIN
	
	bp_sostantivi = dividi_bin(sort_sostantivi, dimensione_bin_sostantivi)
	bp_dip = dividi_bin(sort_dip, dimensione_bin_dip)
	
	
	print bp_sostantivi
	print bp_dip
		
main()
