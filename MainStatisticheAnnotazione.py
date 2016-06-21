#!/usr/bin/python
# coding= utf-8

import os

import Corpus as C
import Repubblica as R
import MappaSensi as MS
import AssociazioniFiller as AF
import AssociazioniClass as AC
import AdjectiveCluster as JC
import PatternParser as PP
import ConfigReader as CR
import Converter as CVT
import TypeResolver as TR
import ArffPrinter as AP
import MatrixPrinter_backup_diplemmi as MP

import StatisticheAnnotazione as SA

import Dumper

#####NB: migliorare gestione passaggio train-test


class Main:
		
	#~ _PARSE_CORPUS_STD = "../dati/corpus/corpus_test"
	_PARSE_CORPUS_STD = "../dati/corpus/corpus_attuale"
	#~ _PARSE_CORPUS_STD = "../dati/corpus/corpus_testing"
	_PARSE_REPUBBLICA_STD = "../dati/repubblicaFreqs/sorted.repubblica.sensitive.lemmasAndPos"
	_PARSE_MAPPA_STD = "../dati/Mapping/fillers2LSO-merged.map"
	_PARSE_DEPFILLER_STD = "../dati/Patterns/evalita2011.lemmaDepFiller.ass"
	_PARSE_DEPCLASS_STD = "../dati/Patterns/evalita2011.lemmaDepClass.freqs"
	_PARSE_CLUSTERS_STD = "../dati/adjClasses/adjs2WNclusters-merged.txt"
	_PARSE_PATTERN_STD = "../dati/Patterns/evalita2011.selected.pat.sp"
	#~ _PARSE_PATTERN_STD = "../dati/Patterns/evalita2011.selected.pat"
	#~ _PARSE_PATTERN_STD = "../dati/Patterns/primo_documento.sp"
	#~ _PARSE_FEATURES_STD = "../dati/Config/lista_features_unitarie"
	_PARSE_FEATURES_STD = "../dati/Config/lista_features"
	#~ _PARSE_CONFIGURAZIONI_STD = ["../dati/Config/v_00","../dati/Config/v_01","../dati/Config/v_02","../dati/Config/v_03","../dati/Config/v_04","../dati/Config/v_05","../dati/Config/v_06","../dati/Config/v_07","../dati/Config/v_08","../dati/Config/v_09","../dati/Config/v_10","../dati/Config/v_11", "../dati/Config/v_13", "../dati/Config/v_14" ]
	#~ _PARSE_CONFIGURAZIONI_STD = [ "../dati/Config/test/t_antidip", "../dati/Config/test/t_associazioni_testa", "../dati/Config/test/t_codip", "../dati/Config/test/t_dip", "../dati/Config/test/t_diplemmi", "../dati/Config/test/t_distribuzionali", "../dati/Config/test/t_lso", "../dati/Config/test/t_modadj", "../dati/Config/test/t_morfologia", "../dati/Config/test/t_NER_e_filtri", "../dati/Config/test/t_PoS"]
	#~ _PARSE_CONFIGURAZIONI_STD = ["../dati/Config/v_rfe", "../dati/Config/v_compl"]
	_PARSE_CONFIGURAZIONI_STD = ["../dati/Config/v_baseline"]
	#~ _PARSE_CONFIGURAZIONI_STD = ["../dati/Config/v_distr_2", "../dati/Config/v_baseline", "../dati/Config/v_distr_lemmi", "../dati/Config/v_lemmi_sp", "../dati/Config/v_compl", "../dati/Config/v_morfologia", "../dati/Config/v_distr_1", "../dati/Config/v_evalita_sp", "../dati/Config/v_ner"]

	_DUMP_CORPUS_STD = "../dump/corpus_attuale"
	_DUMP_REPUBBLICA_STD = "../dump/sorted.repubblica.sensitive.lemmasAndPos"
	_DUMP_MAPPA_STD = "../dump/fillers2LSO-merged.map"
	_DUMP_DEPFILLER_STD = "../dump/evalita2011.lemmaDepFiller.ass"
	_DUMP_DEPCLASS_STD = "../dump/evalita2011.lemmaDepClass.freqs"
	_DUMP_CLUSTERS_STD = "../dump/adjs2WNclusters-merged.txt"
	_DUMP_PATTERN_STD = "../dump/evalita2011.selected.pat.sp"
	_DUMP_FEATURES_STD = "../dump/lista_features"
	_DUMP_CONFIGURAZIONE_STD = "../dump/v_01"
	_DUMP_TOKEN_TARGET_STD = "../dump/token_target_primo_documento"
	
	_PARSE = 1
	_DUMP = 2
	_DUMP_OR_PARSE = 3
	
	_CONF = 1
	
	def comportamento ( self, modulo, o ):
		self.opzione[modulo] = o
	
	def __init__(self):
		self.opzione = {}
		self.opzione ["corpus"] = Main._PARSE
		self.opzione ["repubblica"] = Main._DUMP_OR_PARSE
		self.opzione ["mappa"] = Main._DUMP_OR_PARSE
		self.opzione ["depfiller"] = Main._DUMP_OR_PARSE
		self.opzione ["depclass"] = Main._DUMP_OR_PARSE
		self.opzione ["clusters"] = Main._DUMP_OR_PARSE
		self.opzione ["pattern"] = Main._PARSE
		self.opzione ["features"] = Main._PARSE
		self.opzione ["configurazione"] = Main._PARSE
		self.opzione ["token_target"] = Main._PARSE
	
	def test_parse (self, modulo, f):
		return self.opzione [modulo] == Main._PARSE or  ( self.opzione [modulo] == Main._DUMP_OR_PARSE and not os.path.isfile (f) )
	
		
	def parse_or_dump (self, modulo, file_dump, fun_parse, lista_moduli_dipendenti=[]):
		if self.test_parse (modulo, file_dump): 
			print '[main] parso', modulo
			ret=fun_parse()
			Dumper.binary_dump (ret, file_dump )
			for mod in lista_moduli_dipendenti:
				self.opzione[modulo] = Main._PARSE
		else:
			print '[main] carico dal dump', modulo
			ret = Dumper.binary_load (file_dump)
		print '[main] letto', modulo
		return ret
	
	def perform (self):
		
		frequenze_repubblica =  R.Repubblica( Main._PARSE_REPUBBLICA_STD ) 
		mappa_sensi = MS.MappaSensi( Main._PARSE_MAPPA_STD )
		associazioni_filler = AF.AssociazioniFiller( Main._PARSE_DEPFILLER_STD )
		associazioni_class = AC.AssociazioniClass( Main._PARSE_DEPCLASS_STD )
		mappa_cluster = JC.AdjectiveCluster( Main._PARSE_CLUSTERS_STD )
		pattern = PP.Pattern ( Main._PARSE_PATTERN_STD, mappa_cluster, associazioni_class, associazioni_filler )
		corpus = C.Corpus( Main._PARSE_CORPUS_STD, pattern, mappa_cluster )
		
		s= SA.StatisticheAnnotazione( corpus ) 
		
		

if __name__ == "__main__":
	m = Main ()
	m.comportamento ("corpus", Main._PARSE)
	m.comportamento ("repubblica", Main._DUMP)
	m.comportamento ("mappa", Main._DUMP)
	m.comportamento ("depfiller", Main._PARSE)
	m.comportamento ("depclass", Main._PARSE)
	m.comportamento ("cluster", Main._PARSE)
	m.comportamento ("pattern", Main._PARSE)
	m.comportamento ("features", Main._PARSE)
	m.comportamento ("configurazione", Main._PARSE)
	m.perform ()
