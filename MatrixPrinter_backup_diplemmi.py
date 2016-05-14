#!/usr/bin/python
# coding= utf-8

import numpy as np

class MatrixPrinter:
	
	def __init__(self, versione):
		self.versione=versione
		self.intestazione=[]
		
		#~ self.dati=None
		self.dati=[]
		self.dati_diplemmi=[]
		self.tags=[]
		self.identifiers=[]
	
	def calcolaIntestazione(self, lista_con_tipi):
		ret={}
		colonna=0
		for lista in lista_con_tipi:
			for tupla in lista:
				nome='|'.join(tupla[0])
				tipo=tupla[1]
				if not isinstance(tupla[1], str):
					tipo="{"+','.join(tupla[1])+"}"
					
				ret[nome]=colonna
				colonna+=1	

		return ret


	def produci_matrice(self, versione, lista_features, lista_istanze):
		print "[MatrixPrinter] produco versione:",versione
		
		#~ self.calcolaIntestazione(lista_features)
		self.intestazione=lista_features
		
		for istanza in lista_istanze:
			#~ print "DEBUG: cambio token"
			features=[]
			features_dip_lemmi=[]
			for lista in lista_features:
				if lista[0][0][0]=="Dip_lemmi":
					features_dip_lemmi.extend(getattr(istanza, "Dip_lemmi").keys())
					#~ print "DEBUG: non aggiungo ",lista[0][0][0]
				else:
					features.extend(self.recuperaFeature(lista, istanza))
					#~ print "DEBUG: aggiungo ",lista[0][0][0]
			
			self.dati.append(features)
			self.dati_diplemmi.append(features_dip_lemmi)
			#~ print self.dati
			#~ m=raw_input()
			self.identifiers.append(istanza.id)
			self.tags.append(self.recuperaLSO(istanza))
			
			
	def comprimi_dati(self):
		self.dati=np.array(self.dati)
			
	def recuperaLSO(self, istanza):
		
		ret=getattr(istanza, "LSO")
		
		return ret
		
	def recuperaFeature(self, lista_features, istanza):
		nome=lista_features[0][0]
		ret=[]
		
		
		base=getattr(istanza, nome[0])
		#~ print nome[0], base
		for tupla in lista_features:

			nome=tupla[0]
			f=base
			#~ print nome, f
			if len(nome)>1:

				if nome[1] not in f:
					f=0
				else:
					f=base[nome[1]]
					if len(nome)>2:
						if nome[2] not in f:
							f=0
						else:
							f=f[nome[2]]

			ret.append(f)

		return ret
