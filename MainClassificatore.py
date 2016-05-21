#!/usr/bin/python
# coding= utf-8

import Dumper
#~ import Classifier as CL
#~ import Classifier_pipeline as CL
#~ import InfoPlotter as IP
import datetime
import FeatureSelector as FS
import RFE

versione_completa = "../arff/matrici/v_compl" 

def main():
	
	print "inizio!"
	
	printer=Dumper.binary_load(versione_completa)
	print "[MAIN] caricato Printer"
	
	#~ f=FS.FeatureSelector(printer)
	#~ print "[MAIN] creato FS"
	
	#~ Dumper.binary_dump (f, "../dump/FeatureSelector")
	f = Dumper.binary_load ("../dump/FeatureSelector")
	
	r = RFE.RFE(printer.tags, printer.identifiers)
	print "[MAIN] creato RFE"
	
	r.perform_dict(f.gruppi)


main()
