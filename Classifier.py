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

import time
import random

class Classifier:	
	def __init__(self, matrice, tags, ids):
		#~ self.file_output="../dump/classificatori/statistics_"+printer.versione
		#~ self.file_output_errori="../dump/classificatori/errori_"+printer.versione
	
		self.tags=np.array(tags)
		self.dati=matrice
	
		self.identificatori=np.array(ids)
	
		self.labels=[]
		
		for el in self.identificatori:
			l=el.split(".")
			self.labels.append(l[0][1:])

	def perform_dummy ( self ):
		'''
		 test performing without losing time
		'''
		s = random.randint (0,100)
		time.sleep (s/10)
		return [s,s,s]
	
	def perform (self):
		
		self.lkf = cross_validation.LabelKFold(self.labels, n_folds=5)
		self.svc = svm.LinearSVC()
		
		scores = cross_validation.cross_val_score(self.svc, self.dati, self.tags, cv=self.lkf, scoring='accuracy')
		
		return scores
		
		
	#~ def normalizza(self, tags):
		#~ self.mappa_sensi={'ABSTRACT':1, 'ANIMATE':2, 'OBJECT':3, 'LOCATION':4, 'EVENT':5, 'O':6}
		
		#~ ret=[]
		
		#~ for el in tags:
			#~ ret.append(self.mappa_sensi[el])
			
		#~ return np.array(ret)
