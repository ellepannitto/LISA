#!/usr/bin/python
# coding= utf-8

import Dumper
import Classifier as CL
#~ import Classifier_pipeline as CL


class Main:
	
	#~ lista_file_printer=["../arff/matrici/v_06", "../arff/matrici/v_07", "../arff/matrici/v_08", "../arff/matrici/v_09", "../arff/matrici/v_10", "../arff/matrici/v_11"]
	lista_file_printer=["../arff/matrici/v_12"]
	
	_NFOLD=2
	
	def __init__(self):
		
		for file_printer in Main.lista_file_printer:
			
			printer=Dumper.binary_load(file_printer)
			
			classificatore=CL.Classifier(printer)
			
			classificatore.estraiIndiciClass()
			
			classificatore.classifica_diplemmi(Main._NFOLD)
			
			#~ classificatore.espandiMatrice_diplemmi()
			#~ classificatore.espandiMatrice()
			
			#~ classificatore.splitLabels(Main._NFOLD)
			#~ classificatore.classifica()

			#~ classificatore.PredictionMatrix.stampa_errori(classificatore.file_output_errori)
			Dumper.binary_dump(classificatore, "../dump/classificatori/"+printer.versione)

m=Main()
	
