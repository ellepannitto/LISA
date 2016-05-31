#!/usr/bin/python
# coding= utf-8

import Dumper
import Data as D
#~ import Classifier_pipeline as CL
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


class Main:
		
	_NFOLD=10
	
	def __init__(self):
		
		file_train="../arff/matrici/v_rfe_train"
		file_test="../arff/matrici/v_rfe_test"
		
		now = datetime.datetime.now ()
		data = now.strftime ("%Y_%m_%d")
		

		printer_train=Dumper.binary_load(file_train)
		printer_test=Dumper.binary_load(file_test)
					
		print "classificazione versione",printer_train.versione
		
		classificatore_train=D.Data(printer_train)
		classificatore_test=D.Data(printer_test)
		
		classificatore_train.estraiIndiciClass()
		
		####
		enc = preprocessing.OneHotEncoder(categorical_features=classificatore_train.indici_da_trasformare, dtype=np.int, handle_unknown='ignore')		
		enc.fit(classificatore_train.dati)
		
		clf = svm.LinearSVC()
		
		D_train, D_test = classificatore_train.dati, classificatore_test.dati
		
		#D_diplemmi_train, D_diplemmi_test = classificatore_train.dati_diplemmi[train_index], classificatore_test.dati_diplemmi[test_index]	
				
		D_train, D_test = enc.transform(D_train), enc.transform(D_test)
		
		D_train_sparse, D_test_sparse = scipy.sparse.csr_matrix (D_train), scipy.sparse.csr_matrix (D_test)
			
		#D_diplemmi_train_sparse, D_diplemmi_test_sparse = self.espandiMatrice_diplemmi (D_diplemmi_train), self.espandiMatrice_diplemmi (D_diplemmi_test)
		
		#X_train, X_test = scipy.sparse.hstack ([D_train_sparse, D_diplemmi_train_sparse]), scipy.sparse.hstack ([D_test_sparse, D_diplemmi_test_sparse])
		
		y_train, y_test = classificatore_train.tags, classificatore_test.tags
		#ide_train, ide_test = self.identificatori[train_index], self.identificatori[test_index]
		
		clf.fit(D_train, y_train)
		
		pred = clf.predict(D_test)
		
		accuracy = sklearn.metrics.accuracy_score (y_test,pred)
		precision = sklearn.metrics.precision_score (y_test,pred, average=None)
		recall = sklearn.metrics.recall_score (y_test,pred, average=None)
		fmeasure = sklearn.metrics.f1_score (y_test,pred, average=None)
		
		print accuracy, precision, recall, fmeasure
		
		#classificatore.classifica_diplemmi(Main._NFOLD)
		#classificatore.classifica(Main._NFOLD)
		
		#Dumper.binary_dump(classificatore, "../dump/classificatori/"+printer.versione)
		
		#~ classificatore = Dumper.binary_load("../dump/classificatori/"+printer.versione)
		
		
		#nome_file_riepilogo = "../riepilogo/"+printer.versione+"_"+data
		
		#ip = IP.InfoPlotter (nome_file_riepilogo, printer.versione)
		#ip.feed_classificatore (classificatore)
		#ip.print_riepilogo ()
			
m=Main()
	
