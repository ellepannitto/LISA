#!/usr/bin/python
# coding= utf-8

import time

class ArffPrinter:
	
	#~ file_intestazione=open("../arff/intestazione.arff", "w")
	#~ file_dati=open("../arff/provaout.arff", "w")
	
	
	def __init__(self, versione):
		self.intestazione="% 1. Title: LSO SuperSense Tagging\n%\n"+\
						"% 2. Sources:\n% \ta. Corpus:\n% \tb. Date: "+time.strftime("%d-%m-%y")+"\n"+\
						"% 3. Version: "+versione+"\n%\n"+\
						"@relation LSO\n\n"
						
		self.file_intestazione=open("../arff/"+versione+"_intestazione.arff", "w")
		self.file_dati=open("../arff/"+versione+".arff", "w")
		self.file_id=open("../arff/"+versione+"_ide.arff", "w")
	
	
		
	def stampaIntestazione(self, lista_con_tipi, versione):
		
		self.file_intestazione.write(self.intestazione)
		
		for lista in lista_con_tipi:
			for tupla in lista:
				nome='|'.join(tupla[0])
				#correggere numeric
				tipo="{"+','.join(tupla[1])+"}"
				s="@attribute "+nome+" "+tipo+"\n"
				self.file_intestazione.write(s)


	def produci_arff(self, versione, lista_features, lista_istanze):
		print "[ArffPrinter] stampo versione:",versione
		
		self.stampaIntestazione(lista_features, versione)
		self.file_dati.write("@data\n")
		for istanza in lista_istanze:
			#~ print "nuova istanza!"
			features=[]
			for lista in lista_features:
				features.extend(self.recuperaFeature(lista, istanza))
			
			stringa=','.join(features)		
			self.file_dati.write(stringa+"\n")
			self.file_id.write(getattr(istanza, "id")+"\n")
			
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

			ret.append(str(f))

		return ret
						
		
