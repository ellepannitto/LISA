#!/usr/bin/python
# coding= utf-8

import Dumper

class Filtro:
	
	#~ frequenze = Dumper.binary_load ("")
	_NBIN = 10.0
	_LIM = 100
	
	
	def __init__(self, lista_pos, hasher, frequenze):
		
		self.hasher = hasher
		
		f = frequenze.dizionario_frequenze
		
		self.dizionario_frequenze, self.tot = self.filtra(f, lista_pos)
		
		self.breakpoint = self.calcola_bp()
		
		
	def filtra (self, diz, pos):
		
		# 0 hasha "MISSING VALUE" e 1 hasha "sp" in Hasher
		ret = {0:Filtro._LIM+1,1:Filtro._LIM+1}
		
		tot = 0
		
		for t, v in diz.items():
			pos_t = t[1]
			
			if pos_t[0] in pos and v>Filtro._LIM:
				h = self.hasher.hash(t[0])
				
				if h in ret:
					tot-=ret[h]
					ret[h]=max(ret[h],v)
				else:
					ret[h] = v
					
				tot+=ret[h]
				
		#~ print "Dizionario Filtrato"
		#~ for k,v in ret.items ():
			#~ print k,v
			
		return ret, tot
		
	def calcola_bp (self):
		
		dim_bin = self.tot/Filtro._NBIN
		
		lista_freq_ordinate = sorted(self.dizionario_frequenze.items(), key=lambda x: x[1])
		
		breakpoints=[]
		
		i=0
		while i<len(lista_freq_ordinate): 
			sp=0
			while sp < dim_bin and i<len(lista_freq_ordinate):
				sp+=lista_freq_ordinate[i][1]
				i+=1
				
			#~ print "elementi bin", i, "---", sp
			
			breakpoints.append(lista_freq_ordinate[i-1][1])
		
		#~ print "tot",self.tot
		#~ print "lista bp", breakpoints
		
		
		
		
		return breakpoints	
			
			
		
		
		
