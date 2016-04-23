#!/usr/bin/python
# coding= utf-8

import Dumper
import Classifier as CL
#~ import Classifier_pipeline as CL
import InfoPlotter as IP
import datetime


class Main:
		
	lista_file_printer=["../arff/matrici/v_00","../arff/matrici/v_01","../arff/matrici/v_01_bis","../arff/matrici/v_02","../arff/matrici/v_03","../arff/matrici/v_04","../arff/matrici/v_05","../arff/matrici/v_06","../arff/matrici/v_07","../arff/matrici/v_08","../arff/matrici/v_09","../arff/matrici/v_09_bis","../arff/matrici/v_11"]
	#~ lista_file_printer=["../arff/matrici/v_11"]
	#~ lista_file_printer=["../arff/matrici/v_lucio", "../arff/matrici/v_10", "../arff/matrici/v_12"]
	#~ lista_file_printer=["../arff/matrici/v_10"]
	
	_NFOLD=5
	
	def __init__(self):
		
		now = datetime.datetime.now ()
		data = now.strftime ("%Y_%m_%d")
		
		for file_printer in Main.lista_file_printer:
			
			printer=Dumper.binary_load(file_printer)
						
			print "classificazione versione",printer.versione			
			
			classificatore=CL.Classifier(printer)
			
			classificatore.estraiIndiciClass()
			
			#classificatore.classifica_diplemmi(Main._NFOLD)
			classificatore.classifica(Main._NFOLD)
			
			Dumper.binary_dump(classificatore, "../dump/classificatori/"+printer.versione)
			
			#~ classificatore = Dumper.binary_load("../dump/classificatori/"+printer.versione)
			
			
			nome_file_riepilogo = "riepilogo_"+printer.versione+"_"+data
			
			ip = IP.InfoPlotter (nome_file_riepilogo, printer.versione)
			ip.feed_classificatore (classificatore)
			ip.print_riepilogo ()
			
m=Main()
	
