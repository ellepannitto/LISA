#!/usr/bin/python
# coding= utf-8

import Dumper
import Classifier as CL
#~ import Classifier_pipeline as CL
import InfoPlotter as IP


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
			
			#~ Dumper.binary_dump(classificatore, "../dump/classificatori/"+printer.versione)
			
			ip = IP.InfoPlotter ("riepilogo")
			ip.feed_classificatore (classificatore)
			
m=Main()
	
