#!/usr/bin/python
# coding= utf-8

from sklearn import svm
from sklearn import preprocessing
from sklearn import cross_validation
from sklearn import metrics
import numpy as np



class Classifier:
	
	def __init__(self, printer):
		
		self.file_output=open("../dump/classificatori/"+printer.versione)
		
		self.intestazione=printer.intestazione
		self.tags=self.normalizza(printer.tags)
		self.dati=np.array(printer.dati)		
				
		self.identificatori=printer.identifiers
		self.labels=[]
		
		for el in self.identificatori:
			l=el.split(".")
			self.labels.append(l[0][1:])

		self.estraiIndiciClass()
		#~ self.dati = self.espandiMatrice()
		self.espandiMatrice()
		
		self.splitLabels()
			
		self.classifica()	
			
	
		
	def normalizza(self, tags):
		mappa_sensi={'ABSTRACT':1, 'ANIMATE':2, 'OBJECT':3, 'LOCATION':4, 'EVENT':5, 'O':6}
		
		ret=[]
		
		for el in tags:
			ret.append(mappa_sensi[el])
			
		return np.array(ret)
	
	def splitLabels(self):
		
		self.lkf=cross_validation.LabelKFold(self.labels, n_folds=10)
		
		self.train_labels=[]
		self.test_labels=[]
		
		for train, test in self.lkf:
			#~ print ("%s %s"%(train, test))
			self.train_labels.append(train)
			self.test_labels.append(test)
		
	
	def estraiIndiciClass(self):
		
		self.indici_da_trasformare=[]
		
		i=0
		for el in self.intestazione:
			for tupla in el:
				tipo=tupla[2]
				if tipo!="numeric" and tipo!="bool":
					self.indici_da_trasformare.append(i)
				i+=1
		
	def espandiMatrice (self):
		
		self.enc=preprocessing.OneHotEncoder(categorical_features=self.indici_da_trasformare, dtype=np.int)
		
		self.enc.fit(self.dati)
		
		
		
		#~ return self.enc.transform(self.dati)
		

	def classifica(self):
		self.classificatore=svm.LinearSVC()
		
		for train_index, test_index in self.lkf:
			X_train, X_test = self.dati[train_index], self.dati[test_index]
			y_train, y_test = self.tags[train_index], self.tags[test_index]
			
			X_train=self.enc.transform(X_train)
			X_test=self.enc.transform(X_test)
			
			self.classificatore.fit(X_train, y_train)
			predictions=self.classificatore.predict(X_test)
			
			
			#~ print self.classificatore.score(X_test, y_test)
			self.file_output.write( metrics.classification_report(y_test, predictions) )
			self.file_output.write( metrics.confusion_matrix(y_test, predictions) )
			#~ print X_test
			#~ print y_train, y_test
			print "finito"
			m=raw_input()
