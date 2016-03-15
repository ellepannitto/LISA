#!/usr/bin/python
#coding: utf-8

import Token_target as TT

class Converter:
	
	def __init__ (self):
		pass

	def converti_corpus_to_token_target (self, corpus, frequenze_standard):
		dizionario_filtro = corpus.dizionario_frequenze
		dizionario_frequenze = frequenze_standard.dizionario_frequenze
		frequenze_cumulate = frequenze_standard.dizionario_cumulato
		massimafreq = frequenze_standard.massima_frequenza

		ret = []
		#TT.Token_target.set_dizionario_filtro (dizionario_filtro)
		TT.Token_target.dizionario_filtro = dizionario_filtro
		#~ print "DEBUG"
		#~ print TT.Token_target.dizionario_filtro
		#~ m = raw_input ()
		for n, doc in corpus.documenti.items ():
			m=0
			for frase in doc:
				quotes = False
				for k, tok in frase.tokens.items ():
					if tok.form == '"':
						quotes = not quotes
					elif tok.form == '«':
						quotes = True
					elif tok.form == '»':
						quotes = False
					if tok.CPoS == 'S':
						tt = TT.Token_target (tok, frase)
						tt.fId (n, m, k)
						tt.fWithinQuotes (quotes)
						tt.fFrequenzaLemmaPoS (tok.lemma, dizionario_frequenze)
						tt.fFrequenzaLemmaPoS_log (tok.lemma, dizionario_frequenze)
						tt.fFrequenzaRelativaLemmaPoS (tok.lemma, 0.1, dizionario_frequenze, frequenze_cumulate, massimafreq)
						ret.append (tt)
				m+=1
		self.set_liste_possibili_valori ()
		return ret
	
	def set_liste_possibili_valori (self):
		self.lista_di_tutti_i_possibili = {}
		self.lista_di_tutti_i_possibili ["lemmi"] = TT.Token_target.hasher_lemmas.dizionario_hash.values() + [ "M" ]
		self.lista_di_tutti_i_possibili ["forme"] = TT.Token_target.hasher_forms.dizionario_hash.values() + [ "M" ]
		self.lista_di_tutti_i_possibili ["morfologia_genere"] = ["m", "f", "n", "missing"]
		self.lista_di_tutti_i_possibili ["morfologia_numero"] = ["s", "p", "n", "missing"]
		self.lista_di_tutti_i_possibili ["CPoS"] = ["A", "C", "B", "E", "D", "F", "I", "N", "P", "S", "R", "T", "V", "X", "M"]
		self.lista_di_tutti_i_possibili ["CPoS_sostantivi"] = ["S"]
		self.lista_di_tutti_i_possibili ["bin_frequenza"] = ["altissima","alta","media","bassa","bassissima"]
		self.lista_di_tutti_i_possibili ["aggettivi"] = TT.Token_target.hasher_aggettivi.dizionario_hash.values() + [ "M" ]
		self.lista_di_tutti_i_possibili ["clusters"] = TT.Token_target.hasher_cluster.dizionario_hash.values() + [ "M" ]
		self.lista_di_tutti_i_possibili ["dipendenze"] = TT.Token_target.hasher_dipendenze.dizionario_hash.values() + [ "M" ]
		self.lista_di_tutti_i_possibili ["LSO"] = ["ANIMATE", "ABSTRACT", "OBJECT", "EVENT", "LOCATION", "O"] 
		self.lista_di_tutti_i_possibili ["misure_associazione"] = ["normalizedLL", "scaledLL"]
		self.lista_di_tutti_i_possibili ["PoS"] = ["FS", "DI", "BN", "DE", "DD", "DR", "FB", "FC", "FF", "DQ", "PR", "PP", "PQ", "NO", "RD", "PC", "PD", "PE", "PI", "RI", "A", "VA", "B", "E", "CC", "EA", "VM", "N", "AP", "S", "T", "V", "CS", "X", "I", "P", "SP", "SW", "SA", "M"]
		self.lista_di_tutti_i_possibili ["PoS_sostantivi"] = ["S", "SP", "SW", "SA", "M" ]
		self.lista_di_tutti_i_possibili ["lemmi_antidipendenze"] = TT.Token_target.hasher_lemmi_antidipendenze.dizionario_hash.values() + [ "M" ]
		self.lista_di_tutti_i_possibili ["preposizioni"] = TT.Token_target.hasher_preposizioni.dizionario_hash.values() + [ "M" ]
		self.lista_di_tutti_i_possibili ["lemmi_dipendenze"] = TT.Token_target.hasher_lemmi_dipendenze.dizionario_hash.values() + [ "M" ]
