#!/usr/bin/python
# coding= utf-8

import Corpus as C
import Repubblica as R
import MappaSensi as MS
import AssociazioniFiller as AF
import AssociazioniClass as AC
import AdjectiveCluster as JC

CORPUS_STD = "../dati/corpus/corpus_attuale"
REPUBBLICA_STD = "../dati/repubblicaFreqs/sorted.repubblica.sensitive.lemmasAndPos"
MAPPA_STD = "../dati/Mapping/fillers2LSO-merged.map"
DEPFILLER_STD = "../dati/Patterns/evalita2011.lemmaDepFiller.ass"
DEPCLASS_STD = "../dati/Patterns/evalita2011.lemmaDepClass.freqs"
CLUSTERS_STD = "../dati/adjClasses/adjs2WNclusters-merged.txt"

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
		
		mappa_cluster=JC.AdjectiveCluster( CLUSTERS_STD )
		print '[main] letti cluster aggettivi'
		
		pattern=PP.Pattern ( PATTERN_STD )
		print '[main] letti pattern'
		
		corpus=C.Corpus( CORPUS_STD )
		corpus.aggiorna_pattern(pattern)
		print '[main] letto corpus'
		
