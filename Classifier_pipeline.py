#!/usr/bin/python
# coding= utf-8

from sklearn import svm
from sklearn import preprocessing
from sklearn import cross_validation
from sklearn import metrics
import scipy.sparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline


import Dumper
import PredictionMatrix as PM


class Classifier:
	
	
	def __init__(self, printer):
		self.file_output="../dump/classificatori/statistics_"+printer.versione
		self.file_output_errori="../dump/classificatori/errori_"+printer.versione
		
		self.intestazione=printer.intestazione
		
		self.tags=self.normalizza(printer.tags)
		self.dati=np.array(printer.dati)
		self.dati_diplemmi=printer.dati_diplemmi
	
		
		self.identificatori=np.array(printer.identifiers)
		self.PredictionMatrix=PM.PredictionMatrix(printer.identifiers, printer.tags)
		
		self.labels=[]
		
		for el in self.identificatori:
			l=el.split(".")
			self.labels.append(l[1][1:])

		self.classificatore=[]
		self.reports=[]
		
		
		#SISTEMARE
		self.cm=[[0,0,0,0,0,0],
				[0,0,0,0,0,0],
				[0,0,0,0,0,0],
				[0,0,0,0,0,0],
				[0,0,0,0,0,0],
				[0,0,0,0,0,0]]
		self.cm_normalized=[[0,0,0,0,0,0],
				[0,0,0,0,0,0],
				[0,0,0,0,0,0],
				[0,0,0,0,0,0],
				[0,0,0,0,0,0],
				[0,0,0,0,0,0]]
		
		self.tutti_i_possibili_diplemmi = [[el] for el in printer.intestazione[-1][0][1]]
		
		#~ print self.tutti_i_possibili_diplemmi
		#~ m = raw_input ();
	
	
	def perform(self, k):
		
		
		lista_card=[len(self.intestazione[p][0][1]) for p in self.indici_da_trasformare]
		
		encoder = preprocessing.OneHotEncoder(n_values=lista_card, categorical_features=self.indici_da_trasformare, dtype=np.int)
		
		splitter = cross_validation.LabelKFold(self.labels, n_folds=k)
		
		classificatore=svm.LinearSVC()
		
		for train_index, test_index in splitter:
			X_train, X_test = self.dati[train_index], self.dati[test_index]
			y_train, y_test = self.tags[train_index], self.tags[test_index]
			
			pipeline = Pipeline([("enc", encoder),("clf", classificatore)])
		
			pipeline.fit(X_train, y_train)
			prediction = pipeline.predict(X_test)
		
		
			print metrics.classification_report(y_test, prediction)
			#~ print prediction
		
	
	#vedilo come uno pseudocodice
	def espandiMatrice_diplemmi (self):
		self.enc_diplemmi=preprocessing.OneHotEncoder()
		self.enc_diplemmi.fit(self.tutti_i_possibili_diplemmi)
		
		lista_di_liste=[]
		i=0
		
		#~ print "DEBUG: tutti i dati:", self.dati
		#~ print "DEBUG: tutti i dati diplemmi:", self.dati_diplemmi
		
		tutti_vuoti=False
		while not tutti_vuoti:
			tutti_vuoti=True
			lista_i=[]
			for el in self.dati_diplemmi:
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
		height = len(self.dati)
		
		#~ print "Debug: dimensioni matrice ",width, "x", height
		
		self.matrice_sparsa_diplemmi = scipy.sparse.bsr_matrix ((height,width))
		
		for lista_i in lista_di_liste:
			matrice_i = self.enc_diplemmi.transform(lista_i)
			#~ print "Debug: matrice trasformata ",matrice_i.toarray()
			self.matrice_sparsa_diplemmi += matrice_i
		#~ print "Debug: matrice somma ",self.matrice_sparsa_diplemmi.toarray()
				
		
		
	def normalizza(self, tags):
		self.mappa_sensi={'ABSTRACT':1, 'ANIMATE':2, 'OBJECT':3, 'LOCATION':4, 'EVENT':5, 'O':6}
		
		ret=[]
		
		for el in tags:
			ret.append(self.mappa_sensi[el])
			
		return np.array(ret)
	
	def splitLabels(self, k):
		
		#self.lkf=cross_validation.LabelKFold(self.labels, n_folds=k)
		self.lkf=cross_validation.LabelKFold(self.labels, n_folds=2)
		
		self.train_labels=[]
		self.test_labels=[]
		
		for train, test in self.lkf:
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
		
		self.indici_da_trasformare=self.indici_da_trasformare[:-1]
		
		#~ print self.intestazione
		#~ print self.indici_da_trasformare
		
	def espandiMatrice (self):
		
		#~ print self.indici_da_trasformare
		#~ print self.intestazione[self.indici_da_trasformare[0]]
		lista_card=[len(self.intestazione[p][0][1]) for p in self.indici_da_trasformare]
		
		#~ print lista_card
		
		self.enc=preprocessing.OneHotEncoder(n_values=lista_card, categorical_features=self.indici_da_trasformare, dtype=np.int)
		self.enc.fit(self.dati[0])
		
		
		print "HO FINITO L'ENCODING"
		

	def classifica(self):
			
		matrice_sparsa_altre_feature = scipy.sparse.bsr_matrix (self.dati)
		#~ print "Debug: matrice altre feature ",matrice_sparsa_altre_feature.toarray()	
		
		self.dati = scipy.sparse.hstack ([matrice_sparsa_altre_feature, self.matrice_sparsa_diplemmi])
		#~ print "Debug: matrice composta ",self.dati.toarray()
			
		i=0
		for train_index, test_index in self.lkf:
			self.classificatore.append( svm.LinearSVC() )
			
			#~ print "train_index", train_index
			#~ print "test_index", test_index
			#~ m = raw_input ()
			
			ide_train = []
			ide_test = []
			
			lista_x = []
			lista_y = []
			
			for j in train_index:
				lista_x.append (self.dati.getrow(j))
				ide_train.append (self.identificatori[j])
				lista_y.append (self.tags[j])
				if j%500 == 0 :
					print "lette",j,"righe di train"
			
			print "DEBUG: finito leggere righe train"
			
			X_train = scipy.sparse.vstack (lista_x)
			y_train = lista_y

			lista_x = []
			lista_y = []
			
			for j in test_index:
				lista_x.append (self.dati.getrow(j))
				ide_test.append (self.identificatori[j])
				lista_y.append (self.tags[j])
				if j%500 == 0 :
					print "lette",j,"righe di test"


			print "DEBUG: finito leggere righe train"
			
			X_test = scipy.sparse.vstack (lista_x)
			y_test = lista_y
			
			#~ ide_train, ide_test=self.identificatori[train_index], self.identificatori[test_index]
			
			#~ X_train, X_test = self.dati[train_index], self.dati[test_index]
			#~ y_train, y_test = self.tags[train_index], self.tags[test_index]
			
			#~ X_train=self.enc.transform(X_train)
			#~ X_test=self.enc.transform(X_test)
			
			self.classificatore[i].fit(X_train, y_train)
			
			predictions=self.classificatore[i].predict(X_test)
			
			self.PredictionMatrix.add_fold(list(predictions), list(ide_test), i)

			self.reports.append( metrics.classification_report(y_test, predictions) )
			
			def plot_confusion_matrix(cm, title='Confusion matrix', cmap=plt.cm.Blues):
				plt.imshow(cm, interpolation='nearest', cmap=cmap)
				plt.title(title)
				plt.colorbar()
				tick_marks = np.arange(6)
				plt.xticks(tick_marks, [1,2,3,4,5,6] , rotation=45)
				plt.yticks(tick_marks, [1,2,3,4,5,6])
				plt.tight_layout()
				plt.ylabel('True label')
				plt.xlabel('Predicted label')
			
			
			matrice = metrics.confusion_matrix(y_test, predictions)
			matrice_normalized = matrice.astype('float') / matrice.sum(axis=1)[:, np.newaxis]
			
			for p in range(len(self.cm)):
				self.cm[p]=[self.cm[p][j]+matrice[p][j] for j in range(len(self.cm[p]))]

			
			np.set_printoptions(precision=2)
			print('Confusion matrix, without normalization')
			print(self.cm)
			plt.figure()
			plot_confusion_matrix(self.cm)
			plt.show()
			#~ self.file_output.write ( self.stampa_matrice( matrice ) )
			#~ self.file_output.write ( "\n" )
			
			i+=1
			
	def stampa_matrice (self, matrice):
		self.inverso_mappa={v:k for k,v in self.mappa_sensi.items()}
		
		s="\tABSTRACT\tANIMATE\tOBJECT\tLOCATION\tEVENT\tO\n"
		
		for i in range( len(matrice)):
			
			el=matrice[i]
			s+=self.inverso_mappa[i+1]+"\t"
			
			for k in el:
				#~ print k
				s+=str(k)+"\t"
			s+="\n"
		return s	


	def confronta ( self, gold, predictions, ide, f):
		self.file_output_errori.write("FOLD: "+str(f)+"\n")
		self.file_output_errori.write("IDE\tGOLD\tPREDICTED"+"\n")
		
		for i in range(len(gold)):
			if gold[i]!=predictions[i]:
				self.file_output_errori.write ( ide[i]+"\t"+self.inverso_mappa[gold[i]]+"\t"+self.inverso_mappa[predictions[i]]+"\n" )
		

