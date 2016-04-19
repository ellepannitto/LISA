#!/usr/bin/python
# coding= utf-8

import Dumper
import Classifier as CL


class Main:
	
	lista_file_printer=["../arff/matrici/v_04"]
	
	def __init__(self):
		for file_printer in Main.lista_file_printer:
			printer=Dumper.binary_load(file_printer)
			classificatore=CL.Classifier(printer)
	


m=Main()
	
