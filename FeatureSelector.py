#!/usr/bin/python
#coding: utf-8 

import Dumper
import datetime

import Filtro as F
import FiltroCluster as FC

from sklearn import svm
from sklearn import preprocessing
from sklearn import cross_validation
from sklearn import metrics
from sklearn.feature_selection import RFECV
import scipy.sparse
import numpy as np
import matplotlib.pyplot as plt

_NFOLD=10
	

def index_generalizzato ( lista, valori ):
	'''
	 cerca dentro una lista alcuni valori e restituisce una lista di indici trovati
	 lista: [A,B,C,D] valori: [A,C]
	 valore restituito: [0,2]
	'''
	
	#~ print "Debug indice generalizzato"
	#~ print "valori",valori
	
	ret = map (lista.index, valori)
	#~ print "valore restituito", ret
	
	return ret


def index_generalizzato_prefisso ( lista, valori ):
	'''
	 cerca dentro una lista una stringa che hanno come prefisso alcuni valori e restituisce una lista di indici trovati
	 lista: [AZZZ,BZZZ,CZZZ,DZZZ] valori: [A,C]
	 valore restituito: [0,2]
	'''
	
	ret = []
	
	for pref in valori:
	
		for i in  range (len (lista)):
			el = lista[i]
			if el[0:len(pref)] == pref:
				ret.append (i)
	
	return ret
	

def converti_intestazione_in_indici ( intestazione ):
	'''
	 converte una lista di liste di tuple (come memorizzata in MatrixPrinter.intestazione) in una lista di nomi di features
	 parametro intestazione: l'intestazione da convertire [ [(["a"],l1,t),(["b"],l2,t)], [(["c"],l3,t)] ..., [(["w"],l20,t),(["z"],l21,t)] ]
	 valore restituito: la lista di nomi di feature corrispondenti: ["a", "b", "c", ... , "w", "z"] nella posizione occupata nella matrice
						la lista di liste di tutti i possibili valori assumibili da ogni feature: [l1,l2,l3...l20,l21]
	'''
	
	#~ print "DEBUG CONVERSIONE INTESTAZIONE IN INDICI"
	#~ print "intestazione:", intestazione
	
	ret_indici = []
	ret_possibili_valori = []
	
	for lista in intestazione:
		#lista: [(["a"],l,t),(["b"],l,t)]
		for tupla in lista:
			#tupla: (["a"],l,t)
			ret_indici.append (tupla[0][0])
			ret_possibili_valori.append (tupla[1])
	
	#~ print "ret_indici", ret_indici
	#~ print "ret_possibili_valori", ret_possibili_valori
	
	return ret_indici, ret_possibili_valori

def estrai_colonna (lista_indici, matrice):
	'''
	 data una matrice e una lista di indici, restituisce la matrice formata dalle colonne selezionate dagli indici
	 matrice: [ [1,2,3],
	            [4,5,6],
	            [7,8,9]]
	 lista_indici: [1,2]
	 
	 valore restituito: [ [2,3],
						  [5,6],
						  [8,9]]
	'''
	#~ print "DEBUG tipo della matrice:", type (matrice)
	
	ret = [ [matrice[r][i] for i in lista_indici] for r in range(len(matrice))]
	
	return ret

def estrai_colonna_scipy (lista_indici, matrice):
	'''
	 data una matrice sparsa memorizzata in una struttura dati scipy.sparse e una lista di indici, restituisce la matrice formata dalle colonne selezionate dagli indici
	 matrice: [ [0,2,0],
	            [4,5,0],
	            [0,0,0]]
	 lista_indici: [1,2]
	 
	 valore restituito: [ [2,0],
						  [5,0],
						  [0,0]]
	'''
		
	ret = []
	for j in lista_indici:
		#~ print "estraggo la colonna",j
		ret.append (matrice.getcol(j))
	
	matrice = scipy.sparse.hstack (ret)
	
	return matrice


def estrai_colonna_one_hot (lista_indici, matrice):
	'''
	 data una matrice e una lista di indici, estrae solo le colonne selezionate dagli indici e ne esegue il one_hot encoding
	'''
	
	matrice_categorical = estrai_colonna (lista_indici, matrice)
	enc = preprocessing.OneHotEncoder(dtype=np.int)
	sparsa = enc.fit_transform (matrice_categorical)
	sparsa_csc = scipy.sparse.csc_matrix( sparsa )
	return sparsa

def trova_classe (lista, n):
	
	i=0
	#~ print "DEBUG trova_classe per input",n
	#~ print "lista breakpoint",lista
	while i<len(lista) and n>lista[i]:
		#~ print "non è nella classe", i
		#~ print "limite:",lista[i]
		i+=1
	
	return i

def applica_filtro ( matrice, label, filtro ):
	'''
	 data una matrice M con le colonne etichettate e un filtro, restituisce una lista di insiemi di colonne LC tale che:
		l'unione di tutti gli elementi di LC sia M
		in ogni elemento di LC ci sia un raggruppamento di colonne le cui etichette hanno una frequenza stabilita dal filtro
	'''
	
	#~ print "numero label:",len(label)
	#~ print "numero colonne matrice",matrice.shape[1]
	#~ m = raw_input()
	
	frequenza = filtro.dizionario_frequenze
	bp = filtro.breakpoint
	
	indici = [[] for i in range(len(bp)+1)]
	ret = []
	
	#~ print "breakpoint:",bp
	#~ print "chiavi di frequenza:", frequenza.keys ()
	
	
	for i in range(len(label)):
		l=label[i]
		
		#~ print "cerco classe per la colonna:",i,"label:",l
		#~ if i%100 == 0:
			#~ m = raw_input ()
		
		try:
			f = frequenza[l]
			c = trova_classe(bp, f)

			
		except KeyError:
			#TODO: gestire gli errori se un lemma non era nel dizionario delle frequenze. Per ora tali lemmi vengono messi in una classe apposta da soli
			c = len(bp)
			#print "non trovato:",l
			#~ m = raw_input ()
			
		indici[c].append(i)
		
		#~ print "frequenza",f,"va in classe:", c
		#~ if i%100 == 0:
			#~ m=raw_input()
	
	for i in range(len(indici)):
		lista_indici = indici[i]
		#~ print "--- classe",i,"è grande",len(lista_indici)
		#~ m = raw_input ()
		ret.append( estrai_colonna_scipy ( lista_indici, matrice ) )
		
	return ret
	
def estrai_label ( intestazione, lab):
	ret = []
	
	for el in intestazione:
		for tup in el:
			#~ print tup
			nome = tup[0]
			if nome[0]==lab:
				#~ print nome
				ret.append(nome[1])
		#~ m=raw_input()	
	return ret
			

class FeatureSelector:
	
	def __init__(self, printer):
		
		now = datetime.datetime.now ()
		data = now.strftime ("%Y_%m_%d")
		
		
		
		#~ hasher_lemmi = Dumper.binary_load("../dump/hasher/lemmi.rawobject") 
		
		hasher_teste = Dumper.binary_load("../dump/hasher/antidipendenze.rawobject")
		hasher_dipendenze = Dumper.binary_load("../dump/hasher/dipendenze.rawobject")
		
		frequenze_repubblica = Dumper.binary_load("../dump/sorted.repubblica.sensitive.lemmasAndPos")
		
		#~ self.filtro_lemmi = F.Filtro ( ["S"], hasher_lemmi, frequenze_repubblica )
		
		self.filtro_antidip_lemmi = F.Filtro ( ["S", "V"], hasher_teste, frequenze_repubblica ) 
		self.filtro_cluster = FC.FiltroCluster (frequenze_repubblica)
		self.filtro_diplemmi = F.Filtro ( ["S", "V"], hasher_dipendenze, frequenze_repubblica )
		
		self.genera_gruppi (printer)
		#~ print self.gruppi.keys()
		
		#~ self.labels=[]
		
		#~ for el in printer.identifiers:
			#~ l=el.split(".")
			#~ self.labels.append(l[0][1:])
		
		#~ prima_matrice = self.encode (printer.dati, printer.intestazione)
		
						
		
		#~ matrice = scipy.sparse.hstack ([prima_matrice, seconda_matrice])
		
		#~ gold = printer.tags
		
		#~ self.recursiveSelection(matrice, gold)
	
	def genera_gruppi (self, printer):
		self.gruppi = {}
		
		lista_indici, lista_possibili_valori = converti_intestazione_in_indici (printer.intestazione)
		
		#~ print "lista indici",lista_indici
		
		indice_morfologia_genere = index_generalizzato (lista_indici, ["morfologia_genere"])
		indice_morfologia_numero = index_generalizzato (lista_indici, ["morfologia_numero"])
		
		indice_lemmi = index_generalizzato (lista_indici, ["lemma"])
		lista_possibili_lemmi = lista_possibili_valori [indice_lemmi[0]]
		
		indice_ner_one_hot = index_generalizzato (lista_indici, ["CPoSPrev","CPoSNext","PoSPrev","PoS","PoSNext"])
		indice_ner_normali = index_generalizzato (lista_indici, ["Hyphen","Capitalized","FirstWord","WordShape","WithinQuotes","SeqCap","CapNext","CapPrev","FrequenzaLemmaPoS_log","FrequenzaRelativaLemmaPoS"])
		indice_modnum = index_generalizzato (lista_indici, ["ModNum"])
		indice_det_def = index_generalizzato (lista_indici, ["Det_def"])
		indice_det_indef = index_generalizzato (lista_indici, ["Det_indef"])
		indice_modadj_pre = index_generalizzato (lista_indici, ["ModAdj_pre_b"])
		indice_modadj_post = index_generalizzato (lista_indici, ["ModAdj_post_b"])
		indice_modadj_cluster = index_generalizzato_prefisso (lista_indici, ["ModAdj_clusters"])
		indice_antidip_tipo = index_generalizzato (lista_indici, ["AntiDip_tipo"])
		
		indice_antidip_lemmi = index_generalizzato (lista_indici, ["AntiDip_lemmi"])
		lista_possibili_antidip_lemmi = lista_possibili_valori [indice_antidip_lemmi[0]]
		
		indice_antidip_pos = index_generalizzato (lista_indici, ["AntiDip_PoS"])
		indice_antidip_preposizione = index_generalizzato (lista_indici, ["AntiDip_preposizione"])
		indice_antidip_forza_associazione = index_generalizzato_prefisso (lista_indici, ["AntiDip_forzaassociazioni"])
		indice_antidip_classe_associazione = index_generalizzato_prefisso (lista_indici, ["AntiDip_classeassociazioni"])
		indice_dip = index_generalizzato_prefisso (lista_indici, ["Dip_b"])
		indice_dip_pos = index_generalizzato_prefisso (lista_indici, ["Dip_PoS"])
		indice_dip_preposizione = index_generalizzato_prefisso (lista_indici, ["Dip_preposizione"])
		
		self.gruppi["morfologia_genere"] = estrai_colonna_one_hot ( indice_morfologia_genere, printer.dati )
		self.gruppi["morfologia_numero"] = estrai_colonna_one_hot ( indice_morfologia_numero, printer.dati )
		
		self.gruppi["lemmi"]=estrai_colonna_one_hot ( indice_lemmi, printer.dati )
		
		#~ colonna_lemmi = estrai_colonna_one_hot ( indice_lemmi, printer.dati )
		
		
		#~ lista_gruppi_lemmi = applica_filtro ( colonna_lemmi, sorted(set(lista_possibili_lemmi)), self.filtro_lemmi )
		#~ for i in range(len(lista_gruppi_lemmi)):
			#~ self.gruppi["lemmi_"+str(i)] = lista_gruppi_lemmi[i]
		
		matrice_ner_one_hot = estrai_colonna_one_hot ( indice_ner_one_hot, printer.dati )
		matrice_ner_normali = estrai_colonna ( indice_ner_normali, printer.dati )
		
		#~ print matrice_ner_one_hot
		
		#~ print type(matrice_ner_one_hot)
		#~ print matrice_ner_one_hot.shape[0], matrice_ner_one_hot.shape[1]
		#~ print type(matrice_ner_normali)
		#~ print len(matrice_ner_normali), len(matrice_ner_normali[0])
		
		
		
		self.gruppi ["ner"] = scipy.sparse.hstack ([matrice_ner_one_hot,matrice_ner_normali])
				
		self.gruppi["modnum"] = estrai_colonna ( indice_modnum, printer.dati )
		self.gruppi["det_def"] = estrai_colonna ( indice_det_def, printer.dati )
		self.gruppi["det_indef"] = estrai_colonna ( indice_det_indef, printer.dati )
		self.gruppi["modadj_pre"] = estrai_colonna ( indice_modadj_pre, printer.dati )
		self.gruppi["modadj_post"] = estrai_colonna ( indice_modadj_post, printer.dati )
		
		colonna_modadj_cluster = estrai_colonna ( indice_modadj_cluster, printer.dati )
		colonna_modadj_cluster_sparsa = scipy.sparse.csc_matrix(colonna_modadj_cluster)
		
		self.gruppi["modadj_cluster"]= colonna_modadj_cluster_sparsa
		
		#~ lista_possibili_cluster = estrai_label (printer.intestazione, "ModAdj_clusters")
		
		#~ print lista_possibili_cluster
		#~ m=raw_input()
		
		#~ lista_gruppi_modadj_cluster = applica_filtro ( colonna_modadj_cluster_sparsa, lista_possibili_cluster, self.filtro_cluster )
		
		#~ for i in range(len(lista_gruppi_modadj_cluster)):
			#~ self.gruppi["modadj_cluster_"+str(i)] = lista_gruppi_modadj_cluster[i]
		
		self.gruppi["antidip_tipo"] = estrai_colonna_one_hot ( indice_antidip_tipo, printer.dati )
		
		colonna_antidip_lemmi = estrai_colonna_one_hot ( indice_antidip_lemmi, printer.dati )
		self.gruppi["antidip_lemmi"]=colonna_antidip_lemmi
		
		
		#~ lista_gruppi_antidip_lemmi = applica_filtro ( colonna_antidip_lemmi, sorted(set(lista_possibili_antidip_lemmi)), self.filtro_antidip_lemmi )
		#~ for i in range(len(lista_gruppi_antidip_lemmi)):
			#~ self.gruppi["antidip_lemmi_"+str(i)] = lista_gruppi_antidip_lemmi[i]
		
		self.gruppi["antidip_pos"] = estrai_colonna_one_hot ( indice_antidip_pos, printer.dati )
		self.gruppi["antidip_preposizione"] = estrai_colonna_one_hot ( indice_antidip_preposizione, printer.dati )
		self.gruppi["antidip_forza_associazione"] = estrai_colonna ( indice_antidip_forza_associazione, printer.dati )
		self.gruppi["antidip_classe_associazione"] = estrai_colonna ( indice_antidip_classe_associazione, printer.dati )
		self.gruppi["dip"] = estrai_colonna ( indice_dip, printer.dati )
		self.gruppi["dip_pos"] = estrai_colonna ( indice_dip_pos, printer.dati )
		self.gruppi["dip_preposizione"] = estrai_colonna ( indice_dip_preposizione, printer.dati )
		
		
		lista_possibili_diplemmi = printer.intestazione[-1][0][1]
		
		colonna_diplemmi = self.expand (printer.dati_diplemmi, lista_possibili_diplemmi)
		self.gruppi["diplemmi"]=colonna_diplemmi

		#~ lista_gruppi_diplemmi = applica_filtro ( colonna_diplemmi, sorted(set(lista_possibili_diplemmi)), self.filtro_diplemmi )
		#~ for i in range(len(lista_gruppi_diplemmi)):
			#~ self.gruppi["diplemmi_"+str(i)] = lista_gruppi_diplemmi[i]

		
	def expand (self, dati_diplemmi, lista_possibili_diplemmi):
		
		self.enc_diplemmi=preprocessing.OneHotEncoder(handle_unknown="ignore")
		
		massimo = max(lista_possibili_diplemmi)+1
		mockup = [ [el] for el in lista_possibili_diplemmi ]
		
		self.enc_diplemmi.fit( mockup )
		
		lista_di_liste=[]
		i=0
	
		#~ print "DEBUG: dati dip lemmi: ",dati_diplemmi
		
		tutti_vuoti=False
		while not tutti_vuoti:
			tutti_vuoti=True
			lista_i=[]
			for el in dati_diplemmi:
				if i<len( el ):
					tutti_vuoti=False
					lista_i.append([el[i]])
				else:
					lista_i.append([massimo])
			if not tutti_vuoti:
				lista_di_liste.append(lista_i)
				#~ print "DEBUG: lista numero",i, lista_i
				i += 1
	
		lista_di_matrici=[]
		
		width = len(lista_possibili_diplemmi)
		height = len(dati_diplemmi)
		
		#print "Debug: dimensioni matrice ",height, "x", width
		
		matrice_sparsa_diplemmi = scipy.sparse.csr_matrix ((height,width))
		
		for lista_i in lista_di_liste:
			matrice_i = self.enc_diplemmi.transform(lista_i)
		#	print "Debug: lista ",lista_i, "matrice trasformata"
		#	print matrice_i.toarray()
			matrice_sparsa_diplemmi += matrice_i
		#~ print "Debug: matrice somma "
		#~ print matrice_sparsa_diplemmi.toarray()


		
		#~ print "Debug: matrice somma senza prima colonna"
		#~ print matrice_senza_prima_colonna.toarray()
		
		
		
		return matrice_sparsa_diplemmi
		
	def encode (self, features, intestazione):
		
		self.indici_da_trasformare=[]
		#~ self.lista_card
		
		i=0
		for el in intestazione[:-1]:
			#~ print el
			#~ m=raw_input()
			for tupla in el:
				tipo=tupla[2]
				if tipo!="numeric" and tipo!="bool":
					self.indici_da_trasformare.append(i)
				i+=1
		
		self.enc = preprocessing.OneHotEncoder(categorical_features=self.indici_da_trasformare, dtype=np.int)		
		self.enc.fit(features)
	
		matrice = self.enc.transform(features)


		return scipy.sparse.csr_matrix(matrice)

	#~ def recursiveSelection (self, matrice, tag):
		#~ mappa = {'ABSTRACT':1, 'ANIMATE':2, 'OBJECT':3, 'LOCATION':4, 'EVENT':5, 'O':6}
		
		#~ y = [mappa[el] for el in tag]
		
		#~ clf = svm.LinearSVC()
		
		#~ lkf = cross_validation.LabelKFold(self.labels, n_folds=_NFOLD)
		
		#~ rfecv = RFECV(estimator=clf, step=1, cv=lkf, scoring='accuracy')
		
		#~ rfecv.fit (matrice, y)
		
		#~ print("Optimal number of features : %d" % rfecv.n_features_)
		
		#~ pass
		
		
	
