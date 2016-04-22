#!/usr/bin/python
# coding= utf-8

from sklearn import svm
from sklearn import preprocessing
from sklearn import cross_validation
from sklearn import metrics
import scipy.sparse
import numpy as np
import matplotlib.pyplot as plt


import Dumper
import PredictionMatrix as PM


class Classifier:
	
	
	def __init__(self, printer):
		self.file_output="../dump/classificatori/statistics_"+printer.versione
		self.file_output_errori="../dump/classificatori/errori_"+printer.versione
		
		self.intestazione=printer.intestazione
		
		self.tags=self.normalizza(printer.tags)
		
		self.dati=np.array(printer.dati)
		self.dati_diplemmi=np.array(printer.dati_diplemmi)
	
		self.identificatori=np.array(printer.identifiers)
		
		#~ self.PredictionMatrix=PM.PredictionMatrix(printer.identifiers, printer.tags)
		
		self.labels=[]
		
		for el in self.identificatori:
			l=el.split(".")
			self.labels.append(l[1][1:])

		self.predictions=[]
		self.gold=[]
		self.ide_test=[]
		
		self.tutti_i_possibili_diplemmi = [[el] for el in printer.intestazione[-1][0][1]]
		
	
	def classifica_diplemmi (self, k):
		
		self.lkf = cross_validation.LabelKFold(self.labels, n_folds=k)
		
		lista_card=[len(self.intestazione[p][0][1]) for p in self.indici_da_trasformare]
		
		self.enc = preprocessing.OneHotEncoder(n_values=lista_card, categorical_features=self.indici_da_trasformare, dtype=np.int)
		
		self.enc.fit(self.dati[0])
		
		self.clf = svm.LinearSVC()
		
		for train_index, test_index in self.lkf:
			
			
			
			D_train, D_test = self.dati[train_index], self.dati[test_index]	
			D_diplemmi_train, D_diplemmi_test = self.dati_diplemmi[train_index], self.dati_diplemmi[test_index]	
			
			
			D_train, D_test = self.enc.transform(D_train), self.enc.transform(D_test)
			D_train_sparse, D_test_sparse = scipy.sparse.csr_matrix (D_train), scipy.sparse.csr_matrix (D_test)
			D_diplemmi_train_sparse, D_diplemmi_test_sparse = self.espandiMatrice_diplemmi (D_diplemmi_train), self.espandiMatrice_diplemmi (D_diplemmi_test)
			X_train, X_test = scipy.sparse.hstack ([D_train_sparse, D_diplemmi_train_sparse]), scipy.sparse.hstack ([D_test_sparse, D_diplemmi_test_sparse])
			
			#~ np.set_printoptions(threshold='nan')
			#~ np.set_printoptions(linewidth='nan')
			
			#~ print "Debug accostamento matrici (D train)"
			#~ print D_train_sparse.todense()
			
			#~ print "Debug accostamento matrici (D diplemmi train)"
			#~ print D_diplemmi_train_sparse.todense()
			
			#~ print "Debug accostamento matrici (X train)"
			#~ print X_train.todense()
			
			
			
			
			
			
			y_train, y_test = self.tags[train_index], self.tags[test_index]
			ide_train, ide_test = self.identificatori[train_index], self.identificatori[test_index]
				
			self.clf.fit(X_train, y_train)
			
			
			self.predictions.append ( self.clf.predict (X_test) )
			self.gold.append ( y_test )
			self.ide_test.append ( ide_test )
	
	
	def classifica (self, k):
		
		self.lkf = cross_validation.LabelKFold(self.labels, n_folds=k)
		
		lista_card=[len(self.intestazione[p][0][1]) for p in self.indici_da_trasformare]
		
		self.enc = preprocessing.OneHotEncoder(n_values=lista_card, categorical_features=self.indici_da_trasformare, dtype=np.int)
		
		self.enc.fit(self.dati[0])
		
		self.clf = svm.LinearSVC()
		
		for train_index, test_index in self.lkf:
			
			X_train, X_test = self.dati[train_index], self.dati[test_index]	
			
			
			y_train, y_test = self.tags[train_index], self.tags[test_index]
			ide_train, ide_test = self.identificatori[train_index], self.identificatori[test_index]
				
			self.clf.fit(X_train, y_train)
		
			self.predictions.append ( self.clf.predict (X_test) )
			self.gold.append ( y_test )
			self.ide_test.append ( ide_test )
			
			
	
	#vedilo come uno pseudocodice
	def espandiMatrice_diplemmi (self, dati_diplemmi):

		self.enc_diplemmi=preprocessing.OneHotEncoder()
		self.enc_diplemmi.fit(self.tutti_i_possibili_diplemmi)
		
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
					lista_i.append([0])
			if not tutti_vuoti:
				lista_di_liste.append(lista_i)
				#~ print "DEBUG: lista numero",i, lista_i
				i += 1
	
		lista_di_matrici=[]
		
		width = len(self.tutti_i_possibili_diplemmi)
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

		matrice_senza_prima_colonna = scipy.sparse.csr_matrix(matrice_sparsa_diplemmi)[:,range(1,width)]
		
		#~ print "Debug: matrice somma senza prima colonna"
		#~ print matrice_senza_prima_colonna.toarray()

				
		return matrice_senza_prima_colonna
		
	def normalizza(self, tags):
		self.mappa_sensi={'ABSTRACT':1, 'ANIMATE':2, 'OBJECT':3, 'LOCATION':4, 'EVENT':5, 'O':6}
		
		ret=[]
		
		for el in tags:
			ret.append(self.mappa_sensi[el])
			
		return np.array(ret)
		
	
	def estraiIndiciClass(self):
		
		self.indici_da_trasformare=[]
		
		i=0
		for el in self.intestazione:
			for tupla in el:
				tipo=tupla[2]
				if tipo!="numeric" and tipo!="bool":
					self.indici_da_trasformare.append(i)
				i+=1
		
		self.indici_da_trasformare=self.indici_da_trasformare[:-1]
		
