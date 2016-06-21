#!/usr/bin/python
# coding= utf-8

import Dumper
import Data as D

import InfoPlotter as IP
import datetime

import sklearn
from sklearn import svm
from sklearn import preprocessing
from sklearn import cross_validation
from sklearn import metrics
import scipy.sparse
import numpy as np
import matplotlib.pyplot as plt

def espandiMatrice_diplemmi (dati_diplemmi, possibili_diplemmi):

	#~ print len(possibili_diplemmi)

	enc_diplemmi=preprocessing.OneHotEncoder(handle_unknown="ignore")
	enc_diplemmi.fit(possibili_diplemmi)
	
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
	
	width = len(possibili_diplemmi)
	height = len(dati_diplemmi)
	
	#print "Debug: dimensioni matrice ",height, "x", width
	
	matrice_sparsa_diplemmi = scipy.sparse.csr_matrix ((height,width))
	
	for lista_i in lista_di_liste:
		matrice_i = enc_diplemmi.transform(lista_i)
	#	print "Debug: lista ",lista_i, "matrice trasformata"
	#	print matrice_i.toarray()
		matrice_sparsa_diplemmi += matrice_i
	#~ print "Debug: matrice somma "
	#~ print matrice_sparsa_diplemmi.toarray()

	matrice_senza_prima_colonna = scipy.sparse.csr_matrix(matrice_sparsa_diplemmi)[:,range(1,width)]
	
	#~ print "Debug: matrice somma senza prima colonna"
	#~ print matrice_senza_prima_colonna.toarray()

			
	#~ print matrice_sparsa_diplemmi.shape	
	#~ print matrice_senza_prima_colonna.shape	
		
	return matrice_senza_prima_colonna


class Main:
	
	def __init__(self):
		
		file_train="../arff/matrici/v_baseline_train"
		file_test="../arff/matrici/v_baseline_test"
		
		now = datetime.datetime.now ()
		data = now.strftime ("%Y_%m_%d")
		

		printer_train=Dumper.binary_load(file_train)
		printer_test=Dumper.binary_load(file_test)
					
		print "classificazione versione",printer_train.versione
		
		dati_train=D.Data(printer_train)
		dati_test=D.Data(printer_test)
		
		dati_train.estraiIndiciClass()
		
		####
		enc = preprocessing.OneHotEncoder(categorical_features=dati_train.indici_da_trasformare, dtype=np.int, handle_unknown='ignore')		
		enc.fit(dati_train.dati)
		
		clf = svm.LinearSVC()
		
		D_train, D_test = dati_train.dati, dati_test.dati
		print "dimensione D_train, test", D_train.shape, D_test.shape
		#~ m = raw_input ()
		
		
		D_diplemmi_train, D_diplemmi_test = dati_train.dati_diplemmi, dati_test.dati_diplemmi
				
		D_train, D_test = enc.transform(D_train), enc.transform(D_test)
		
		print "dimensione D_train, test dopo il transform", D_train.shape, D_test.shape
		#~ m = raw_input ()
		
		D_train_sparse, D_test_sparse = scipy.sparse.csr_matrix (D_train), scipy.sparse.csr_matrix (D_test)
			
		D_diplemmi_train_sparse, D_diplemmi_test_sparse = espandiMatrice_diplemmi (D_diplemmi_train, dati_train.tutti_i_possibili_diplemmi), espandiMatrice_diplemmi (D_diplemmi_test, dati_train.tutti_i_possibili_diplemmi)
		print "dimensione D_diplemmi_train_sparse, D_diplemmi_test_sparse", D_diplemmi_train_sparse.shape, D_diplemmi_test_sparse.shape
		#~ m = raw_input ()
		
		X_train, X_test = scipy.sparse.hstack ([D_train_sparse, D_diplemmi_train_sparse]), scipy.sparse.hstack ([D_test_sparse, D_diplemmi_test_sparse])
		
		y_train, y_test = dati_train.tags, dati_test.tags
		#ide_train, ide_test = self.identificatori[train_index], self.identificatori[test_index]
		
		clf.fit(X_train, y_train)
		
		pred = clf.predict(X_test)
		
		accuracy = sklearn.metrics.accuracy_score (y_test,pred)
		precision = sklearn.metrics.precision_score (y_test,pred, average=None)
		recall = sklearn.metrics.recall_score (y_test,pred, average=None)
		fmeasure = sklearn.metrics.f1_score (y_test,pred, average=None)
		cm = sklearn.metrics.confusion_matrix (y_test,pred)
		
		print accuracy
		print precision
		print recall
		print fmeasure
		print cm
		#~ print clf.score(X_test, y_test)
		
		#classificatore.classifica_diplemmi(Main._NFOLD)
		#classificatore.classifica(Main._NFOLD)
		
		#Dumper.binary_dump(classificatore, "../dump/classificatori/"+printer.versione)
		
		#~ classificatore = Dumper.binary_load("../dump/classificatori/"+printer.versione)
		
		
		#nome_file_riepilogo = "../riepilogo/"+printer.versione+"_"+data
		
		#ip = IP.InfoPlotter (nome_file_riepilogo, printer.versione)
		#ip.feed_classificatore (classificatore)
		#ip.print_riepilogo ()
			
m=Main()
	
