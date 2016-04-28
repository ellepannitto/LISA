#!/usr/bin/python
# coding= utf-8

import sklearn.metrics
import numpy as np
import matplotlib.pyplot as plt
import copy

#~ def avg(l, weights):
	
	#~ return sum([l[i]*weights[i] for i in range(len(l))])/sum(weights)
def avg(l):
	
	return sum(l)/len(l)

def list_of_average ( lista ):
	avgs=[]
	
	for i in range(len (lista[0])):
		avgs.append(0)
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

def matrix_pprint (matrix, label_x=None, label_y=None, formato="%0.2f"):
	
	#~ print "parametro",matrix
	
	str_ret = ""
	
	if label_x is not None:
		if label_y is not None:
			str_ret = '{:10s}'.format ("")
		for lbx in label_x:
			  str_ret += '{:10s}'.format (str(lbx))
		str_ret += "\n"
	
	for i in range (len(matrix)):
		row = matrix[i]
		#~ print "riga",i,row
		
		if label_y is not None:
			str_ret += '{:10s}'.format (str(label_y[i]))
		
		for j in range (len(row)):
			str_ret += '{:10s}'.format (formato % row[j]) 
		str_ret += "\n"
		
	return str_ret


class InfoPlotter:
	''' visualizza e stampa su un file il grafico riassuntivo della k-fold cross validation'''
	
	def __init__ (self, file_riepilogo=None, ver=None):
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
		self.tags = ['ABSTRACT', 'ANIMATE', 'OBJECT', 'LOCATION', 'EVENT', 'O']
		self.versione = ver
		self.precisions_avg = []
		self.recalls_avg = []
		self.fmeasures_avg = []
		
		self.weights = [len(el) for el in self.preds]
		
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
		fmeasure = sklearn.metrics.f1_score (gold,pred, average=None)

		precision_avg = sklearn.metrics.precision_score (gold,pred, average="weighted")
		recall_avg = sklearn.metrics.recall_score (gold,pred,average="weighted")
		fmeasure_avg = sklearn.metrics.recall_score (gold,pred,average="weighted")
		
		
		cm = sklearn.metrics.confusion_matrix ( gold, pred )
		self.accuracies.append (accuracy)
		
		self.precisions.append (precision)
		self.recalls.append (recall)
		self.fmeasures.append (fmeasure)

		self.precisions_avg.append (precision_avg)
		self.recalls_avg.append (recall_avg)
		self.fmeasures_avg.append (fmeasure_avg)
		
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
		assert len (self.accuracies)>0, "[InfoPlotter] get_average_accuracy : feed with data first"
		return avg (self.accuracies) 

	def average_precisions ( self ):
		assert len (self.precisions)>0, "[InfoPlotter] get_average_precisions : feed with data first"
		return list_of_average (self.precisions)
	
	def average_recalls ( self ):
		assert len (self.recalls)>0, "[InfoPlotter] get_average_recalls : feed with data first"
		return list_of_average (self.recalls)
	
	def average_fmeasures ( self ):
		assert len (self.fmeasures)>0, "[InfoPlotter] get_average_fmeasures : feed with data first"
		return list_of_average (self.fmeasures)
		
	
	def normalize_confusion_matrices ( self ):
		
		sum_cm=copy.deepcopy(self.confusion_matrices[0])
		
		#~ print "SOMMA_INIZIALE", sum_cm
		
		for mat in self.confusion_matrices[1:]:
			
			#~ print "DA SOMMARE:", self.confusion_matrices[i:]
			for i in range(len(mat)):
				for j in range (len(mat[i])):
					sum_cm[i][j]+=mat[i][j]
						
		return get_normalized_confusion_matrix(sum_cm)
		
	def sum_confusion_matrices ( self ):
		
		sum_cm=copy.deepcopy(self.confusion_matrices[0])
		
		#~ print "SOMMA_INIZIALE", sum_cm
		
		for mat in self.confusion_matrices[1:]:
			
			#~ print "DA SOMMARE:", self.confusion_matrices[i:]
			for i in range(len(mat)):
				for j in range (len(mat[i])):
					sum_cm[i][j]+=mat[i][j]
						
		return sum_cm
			
			
	def plot_confusion_matrix (self, cm, title='Confusion matrix', cmap=plt.cm.Blues):
		plt.figure()
		plt.imshow(cm, interpolation='nearest', cmap=cmap)
		plt.title(title)
		plt.colorbar()
		plt.clim(0,1)
		tick_marks = np.arange(len(cm[0]))
		plt.xticks(tick_marks, self.tags, rotation=45)
		plt.yticks(tick_marks, self.tags)
		plt.tight_layout()
		plt.ylabel('True label')
		plt.xlabel('Predicted label')
		
		plt.savefig("../riepilogo/plot_"+self.versione)
		#~ plt.show ()
		
	
	def print_riepilogo (self):
		np.set_printoptions(precision=2)
		
		
		cm = self.sum_confusion_matrices ()
		normalized_cm = self.normalize_confusion_matrices ()			
		if self.file_riepilogo is not None:
			fout = open (self.file_riepilogo, "w")
			
			accuracy = self.average_accuracy ()
			
			precisions = self.average_precisions ()
			recalls = self.average_recalls ()
			fmeasures = self.average_fmeasures ()

			avg_precision = avg(self.precisions_avg)
			avg_recall = avg(self.recalls_avg)
			avg_fmeasure = avg(self.fmeasures_avg)
			
			#~ avg_precision = 0
			#~ avg_recall = 0
			#~ avg_fmeasure = 0
			
			avgs = [avg_precision, avg_recall, avg_fmeasure]
			
			matrice_statistica = [[precisions[i],recalls[i],fmeasures[i]] for i in range(len(precisions))] + [avgs]
			
			str_riepilogo = "RIEPILOGO VERSIONE "+str(self.versione)+"\n"+\
							"numero fold: "+ str(self.folds)+"\n"+\
							"tipo classificatore: LinearSVC\n"+\
							"\n"+\
							"Confusion matrix:\n"+\
							matrix_pprint (normalized_cm, self.tags, self.tags)+"\n"+\
							"\n"+\
							matrix_pprint (cm, self.tags, self.tags, "%.0f")+"\n"+\
							"\n"+\
							"Accuracy: "+str(accuracy)+"\n"
							#~ "\n"+\
							#~ matrix_pprint ( matrice_statistica ,["Precision", "Recall","F-Measure"], self.tags+["AVG"])+"\n"+\
							#~ "\n"
			
			fout.write ( str_riepilogo )
							
			
		
		self.plot_confusion_matrix (normalized_cm, title="Confusion Matrix versione "+self.versione)

if __name__ == "__main__":
	matrix = [ [0, 1, 2],
			   [3, 4, 5],
			   [6, 7, 8],
			   [9, 10, 11]]
	label_x = ["col1","col2","col3"]
	label_y = ["rowA","rowB","rowC","rowD"]
	
	print "prova matrix_pprint"
	print matrix_pprint ( matrix,label_x, label_y )
	print matrix_pprint ( matrix,None, label_y )
	print matrix_pprint ( matrix,label_x, None )
	print matrix_pprint ( matrix,None, None )
