#!/usr/bin/python

import sklearn.metrics
import numpy as np
import matplotlib.pyplot as plt

def avg(l): return sum(l)/len(l)

def list_of_average ( lista ):
	avgs=[]
	
	for i in range (lista[0]):
		for l in lista:
			avgs[i] += l[i]
		avgs[i] /= len (lista)
	
	return avgs
	
def get_normalized_confusion_matrix (cm):
	'''
	restituisce la confusion matrix associata ad una confusion matrix data in input
	'''
	cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
	return cm_normalized

class InfoPlotter:
	''' visualizza e stampa su un file il grafico riassuntivo della k-fold cross validation'''
	
	def __init__ (self, file_riepilogo=None):
		'''
		inizializza un oggetto vuoto
		 file_riepilogo: nome del file sul quale stampare il riepilogo. Se None, verrà visualizzato il grafico senza stampare alcun riepilogo.
		'''
		self.file_riepilogo = file_riepilogo
		self.preds = []
		self.golds = []
		self.accuracies = []
		self.precisions = []
		self.recalls = []
		self.fmeasures = []
		self.confusion_matrices = []
		self.folds = 0;
		
	def feed_one_fold (self, pred, gold):
		'''
		fornisce i dati di una classificazione
		 pred: lista di risultati della predizione
		 gold: lista di tag corretti della stessa predizione
		'''
		self.preds.append (pred)
		self.golds.append (gold)
		accuracy = sklearn.metrics.accuracy_score (gold,pred)
		precision = sklearn.metrics.precision_score (gold,pred, average=None)
		recall = sklearn.metrics.recall_score (gold,pred, average=None)
		fmeasure = sklearn.metrics.recall_score (gold,pred, average=None)
		cm = sklearn.metrics.confusion_matrix ( gold, pred )
		self.accuracies.append (accuracy)
		self.precisions.append (precision)
		self.recalls.append (recall)
		self.fmeasures.append (fmeasure)
		self.confusion_matrices.append (cm)
		self.folds += 1
	
	def feed_k_fold (self, preds, golds):
		'''
		fornisce i dati di una k-fold cross validation
		 pred: lista che contiene una lista di risultati per ogni predizione
		 gold: lista che contiene una lista di tag corretti per ogni predizione
		'''
		assert len(preds)==len(golds), "[InfoPlotter] feed_k_fold: preds and golds doesn't have the same length" 
		
		for i in range (len(preds)):
			self.feed_one_fold (preds[i], golds[i])
	
	def feed_classificatore (self, classificatore):
		self.feed_k_fold (classificatore.predictions, classificatore.gold)
	
	def average_accuracy ( self ):
		assert len (self.accuracies)>0 "[InfoPlotter] get_average_accuracy : feed with data first"
		return avg (self.accuracies) 

	def average_precisions ( self ):
		assert len (self.precisions)>0 "[InfoPlotter] get_average_precisions : feed with data first"
		return list_of_average (self.precisions)
	
	def average_recalls ( self ):
		assert len (self.recalls)>0 "[InfoPlotter] get_average_recalls : feed with data first"
		return list_of_average (self.recalls)
	
	def average_fmeasures ( self ):
		assert len (self.fmeasures)>0 "[InfoPlotter] get_average_fmeasures : feed with data first"
		return list_of_average (self.fmeasures)
		
	
	def normalize_confusion_matrices ( self ):
		sum_cm=[[0]*len(self.confusion_matrices[0])]*len(self.confusion_matrices)
		
		for i in range(len(self.confusion_matrices)):
			for j in range(len(self.confusion_matrices[i])):
				sum_cm+=self.confusion_matrices[i][j]
				
		return get_normalized_confusion_matrix(sum_cm)
			
			
	def plot_confusion_matrix (cm, title='Confusion matrix', cmap=plt.cm.Blues):
		plt.figure()
		plt.imshow(cm, interpolation='nearest', cmap=cmap)
		plt.title(title)
		plt.colorbar()
		tick_marks = np.arange(len(cm[0]))
		#~ plt.xticks(tick_marks, iris.target_names, rotation=45)
		#~ plt.yticks(tick_marks, iris.target_names)
		plt.tight_layout()
		plt.ylabel('True label')
		plt.xlabel('Predicted label')
		plt.show ()
	
	def print_riepilogo (self):
		normalized_cm = self.normalize_confusion_matrices ()			
		if self.file_riepilogo is not None:
			fout = open (self.file_riepilogo, "w")
			
			accuracys = self.average_accuracy ()
			precisions = self.average_precisions ()
			recalls = self.average_recalls ()
			fmeasures = self.average_fmeasures ()
			
			fout.write ( "confusion matrix:\n" + str(normalized_cm) + "\n" )
			fout.write ( "accuracy: " + str(accuracy) + "\n" )
			fout.write ( "precisions: " + str(precisions) + "\n" )
			fout.write ( "recalls: " + str(recalls) + "\n" )
			fout.write ( "fmeasures: " + str(fmeasures) + "\n" )
		
		plot_confusion_matrix (normalized_cm)

