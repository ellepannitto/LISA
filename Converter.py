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
						
						
						
						replicare=len(tok.AntiDip)
						
						#~ if replicare > 1:
							#~ print "sono qui", replicare, tok.lemma, tok.AntiDip
							#~ i=raw_input()
						
						bis=0
						
						while True:							
							tt = TT.Token_target (tok, frase, bis)
							tt.fId (n, m, k, bis)
							tt.fWithinQuotes (quotes)
							tt.fFrequenzaLemmaPoS (tok, dizionario_frequenze)
							tt.fFrequenzaLemmaPoS_log (tok, dizionario_frequenze)
							tt.fFrequenzaRelativaLemmaPoS (tok, 0.1, dizionario_frequenze, frequenze_cumulate, massimafreq)
							ret.append (tt)
							
							replicare-=1
							bis+=1
							if not replicare>0:
								break
						
				m+=1
		self.set_liste_possibili_valori ()
		self.dump_hasher()
		
		file_debug=open("token_target", "w")
		
		for t in ret:
			new_dict={TT.Token_target.hasher_lemmi_dipendenze.unhash(k):v for k,v in t.Dip_lemmi.items()}
			file_debug.write(t.id+" "+str(new_dict)+"\n")
		
		return ret
	
	def dump_hasher(self):
		TT.Token_target.hasher_forms.dump("../dump/hasher/forms")
		TT.Token_target.hasher_lemmas.dump("../dump/hasher/lemmi")
		TT.Token_target.hasher_dipendenze.dump("../dump/hasher/dipendenze")
		TT.Token_target.hasher_lemmi_dipendenze.dump("../dump/hasher/lemmi_dipendenze")
		TT.Token_target.hasher_aggettivi.dump("../dump/hasher/aggettivi")
		TT.Token_target.hasher_cluster.dump("../dump/hasher/cluster")
		TT.Token_target.hasher_antidipendenze.dump("../dump/hasher/antidipendenze")
		TT.Token_target.hasher_lemmi_antidipendenze.dump("../dump/hasher/lemmi_antidipendenze")
		TT.Token_target.hasher_preposizioni.dump("../dump/hasher/preposizioni")
		print "[CONVERTER] fine dump hash"
	
	def set_liste_possibili_valori (self):
		self.lista_di_tutti_i_possibili = {}
		self.lista_di_tutti_i_possibili ["lemmi"] = TT.Token_target.hasher_lemmas.dizionario_hash.values()
		self.lista_di_tutti_i_possibili ["forme"] = TT.Token_target.hasher_forms.dizionario_hash.values()
		self.lista_di_tutti_i_possibili ["morfologia_genere"] = TT.Token_target.hasher_morfologia_genere.dizionario_hash.values()
		self.lista_di_tutti_i_possibili ["morfologia_numero"] = TT.Token_target.hasher_morfologia_numero.dizionario_hash.values()
		self.lista_di_tutti_i_possibili ["CPoS"] = TT.Token_target.hasher_CPoS.dizionario_hash.values()
		self.lista_di_tutti_i_possibili ["CPoS_sostantivi"] = ["S"]
		self.lista_di_tutti_i_possibili ["bin_frequenza"] = ["altissima","alta","media","bassa","bassissima"]
		self.lista_di_tutti_i_possibili ["aggettivi"] = TT.Token_target.hasher_aggettivi.dizionario_hash.values()
		self.lista_di_tutti_i_possibili ["clusters"] = TT.Token_target.hasher_cluster.dizionario_hash.values()
		self.lista_di_tutti_i_possibili ["dipendenze"] = TT.Token_target.hasher_dipendenze.dizionario_hash.values()
		self.lista_di_tutti_i_possibili ["LSO"] = ["ANIMATE", "ABSTRACT", "OBJECT", "EVENT", "LOCATION", "O"] 
		self.lista_di_tutti_i_possibili ["misure_associazione"] = ["normalizedLL", "scaledLL"]
		self.lista_di_tutti_i_possibili ["PoS"] = TT.Token_target.hasher_PoS.dizionario_hash.values()
		self.lista_di_tutti_i_possibili ["PoS_sostantivi"] = TT.Token_target.hasher_PoS_sostantivi.dizionario_hash.values()
		self.lista_di_tutti_i_possibili ["lemmi_antidipendenze"] = TT.Token_target.hasher_lemmi_antidipendenze.dizionario_hash.values()
		self.lista_di_tutti_i_possibili ["preposizioni"] = TT.Token_target.hasher_preposizioni.dizionario_hash.values()
		self.lista_di_tutti_i_possibili ["lemmi_dipendenze"] = TT.Token_target.hasher_lemmi_dipendenze.dizionario_hash.values()
