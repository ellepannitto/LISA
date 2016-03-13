#!/usr/bin/python
# coding= utf-8

import Corpus as C
import Repubblica as R
import MappaSensi as MS
import AssociazioniFiller as AF
import AssociazioniClass as AC

CORPUS_STD = "../dati/corpus/corpus_attuale"
REPUBBLICA_STD = "../dati/repubblicaFreqs/sorted.repubblica.sensitive.lemmasAndPos"
MAPPA_STD = "../dati/Mapping/fillers2LSO-merged.map"
DEPFILLER_STD = "../dati/Patterns/evalita2011.lemmaDepFiller.ass"
DEPCLASS_STD = "../dati/Patterns/evalita2011.lemmaDepClass.freqs"


class Main:
	
	def __init__(self):
		
		frequenze_repubblica=R.Repubblica( REPUBBLICA_STD )
		print '[main] calcolate frequenze standard'
		
		mappa=MS.MappaSensi( MAPPA_STD )
		print '[main] letta mappa WordNet -> LSO'
		
		associazioni_filler=AF.AssociazioniFiller( DEPFILLER_STD )
		print '[main] lette associazioni filler'
		
		associazioni_class=AC.AssociazioniClass( DEPCLASS_STD )
		print '[main] lette associazioni class'
		
		
		
		corpus=C.Corpus( CORPUS_STD )
		
