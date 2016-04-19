#!/usr/bin/python
# coding= utf-8

import tarfile
import numpy
from sklearn import svm

import ConfigReader as CF

def leggi_intestazione(intestazione):
	
	mappa={}
	i=0
	with open(intestazione) as f:
		for line in f:
			#~ print line.split()
			#~ m=raw_input()
			feat=line.split()[1]
		
			mappa[feat]=i
			i+=1
			
	return mappa

def leggi_arff(arff, features_scelte, mappa_colonne, mappa_sensi):

	X=[]
	Y=[]
	
	da_stampare=[]
	
	for feat in features_scelte:
		da_stampare.append(mappa_colonne[feat[0]])
		
		
	with open(arff) as f:
		
		f.readline()
		
		for line in f:
			istance=line.split(",")
			
			tok=[]
			
			for k in da_stampare:
				try:
					tok.append(int(istance[k]))
				except ValueError:
					tok.append(float(istance[k]))
					
			
			tag=mappa[istance[-1][:-1]]
			
			X.append(tok)
			Y.append(tag)
			
	return X, Y
		
file_configurazione="../dati/Config/v_scikit_00"
file_intestazione="../arff/v_scikit_intestazione.arff"
arff="../arff/v_scikit.arff"

def main():
	mappa_sensi={'ABSTRACT':1, 'ANIMATE':2, 'OBJECT':3, 'LOCATION':4, 'EVENT':5, 'O':6}
	
	reader=CF.ConfigReader(file_configurazione)
	
	mappa_colonne=leggi_intestazione(file_intestazione)

	#~ print mappa_colonne
	#~ m=raw_input()
	
	print reader.features_scelte
	m=raw_input()
	
	X,Y=leggi_arff(arff, reader.features_scelte, mappa_colonne, mappa_sensi)
	
	
		#~ X_train=X[0:60000]
		#~ X_test=X[60000:]

		#~ Y_train=Y[0:60000]
		#~ Y_test=Y[60000:]
		
		#~ classifier=svm.LinearSVC()
		#~ classifier.fit(X_train,Y_train)
		
		#~ predictions=classifier.predict(X_test)
		#~ for i in range(len(Y_test)):
			#~ print "Gold:", Y_test[i], "Res:", predictions[i]

		
		#~ print predictions
main()
