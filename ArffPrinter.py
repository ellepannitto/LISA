#!/usr/bin/python
# coding= utf-8

import time

class ArffPrinter:
	
	file_intestazione=open("intestazione.arff", "w")
	file_dati=open("provaout.arff", "w")
	intestazione="% 1. Title: LSO SuperSense Tagging\n%\n% 2. Sources:\n% \ta. Corpus:\n% \tb. Date: "+time.strftime("%d-%m-%y")+"\n%\n%\n@relation: LSO\n\n"
	
	
	def __init__(self):
		pass
		
	def stampaIntestazione(self, lista_con_tipi, versione):
		
		ArffPrinter.file_intestazione.write(ArffPrinter.intestazione)
		
		for lista in lista_con_tipi:
			for tupla in lista:
				nome='|'.join(tupla[0])
				tipo="{"+','.join(tupla[1])+"}"
				s="@attribute "+nome+" "+tipo+"\n"
				ArffPrinter.file_intestazione.write(s)


	def produci_arff(self, versione, lista_features, lista_istanze):
		self.stampaIntestazione(lista_features, versione)
		ArffPrinter.file_dati.write("@data\n")
		for istanza in lista_istanze:
			#~ print "nuova istanza!"
			features=[]
			for lista in lista_features:
				features.extend(self.recuperaFeature(lista, istanza))
			#~ print ret
			#~ m=raw_input()
	
			stringa=','.join(features)		
			ArffPrinter.file_dati.write(stringa+"\n")
	
	#RIFARE	
	#NON HA SENSO, MODADJ DEVO RECUPERARLO UNA VOLTA SOLA
	def recuperaFeature(self, lista_features, istanza):
		nome=lista_features[0][0]
		
		ret=[]
		
		base=getattr(istanza, nome[0])
		#~ print base
		#~ print lista_features
		for tupla in lista_features:
			nome=tupla[0]
			#~ print nome
			#~ m=raw_input()
			f=base
			if len(nome)>1:
				#~ print nome[1]
				if nome[1] not in f:
					f=0
				else:
					f=base[nome[1]]
					if len(nome)>2:
						if nome[2] not in f:
							base=0
						else:
							f=f[nome[2]]

			ret.append(str(f))
			#~ print ret
		return ret
						
		
