#!/usr/bin/python
#coding: utf-8 
 
import sys
import math
import Hasher as H

_LIMITE_INFERIORE_FREQUENZE = 5
"""
Alcuni filtri sui lemmi richiedono che la frequenza dello stesso maggiore di questo limite, altrimenti il lemma non è ritenuto significativo e ne viene usato uno fittizio al suo posto
"""

class Token_target:
	"""
	Gli oggetti di classe Token_target memorizzano le informazioni di un singolo token, in un formato tale da poter essere stampato su un file arff
	 Alcune feature sono estratte dal token letto dal corpus, altre dipendono dal contesto e altre ancora da diversi parametri.
	
	I valori di feature o gruppi di feature possono essere recuperate semplicemente leggendo l'attributo corrispondente di un oggetto di classe Token_target.
	 Per esempio, per recuperare la feature denominata "lemma" è sufficiente usare:
	     `tt.lemma` oppure tt.__getattr__ ("lemma")
	 dove tt è un istanza della classe Token_target.
	 Il valore restituito può essere un intero, una stringa, oppure un dizionario. In quest'ultimo caso, il valore del gruppo di feature è da considerarsi ovunque '0' tranne che per le feature corrispondenti alle chiavi del dizionario
	
	Questa classe memorizza inoltre tutti i possibili valori assunti da alcune feature, per recuperarli usare
	    `Token_target.hasher_XXX.dizionario_hash.values()`
	 dove XXX è il nome della feature. Si noti che non tutte le feature sono supportate
	"""
	dizionario_filtro = None;
	hasher_forms = H.Hasher ();
	hasher_lemmas = H.Hasher ();
	hasher_dipendenze = H.Hasher ();
	hasher_lemmi_dipendenze = H.Hasher ();
	hasher_aggettivi = H.Hasher ();
	hasher_cluster = H.Hasher ();
	hasher_antidipendenze = H.Hasher ();
	hasher_lemmi_antidipendenze = H.Hasher ();
	hasher_preposizioni = H.Hasher();
	
	def set_dizionario_filtro (diz):
		if Token_target.dizionario_filtro is not None:
			Token_target.dizionario_filtro = diz
		else:
			print "[Token_target] Warning: multiple call of set_dizionario_filtro"
			print "[Token_target] old dizionario_filtro:", Token_target.dizionario_filtro
			print "[Token_target] new dizionario_filtro:", diz
			print "[Token_target] the new dizionario_filtro will overwrite the old one"
			Token_target.dizionario_filtro = diz
		
	def __init__ (self, tok, frase):
		self.from_token (tok)
		self.from_frase (tok.posizione, frase)
	
	def from_token (self, tok):
		if Token_target.dizionario_filtro is not None:
			form = tok.form
			lemma = tok.lemma
			self.fForm ( form )
			self.fLemma ( lemma, tok.PoS )
			self.fMorfologia_genere ( tok.morfologia )
			self.fMorfologia_numero ( tok.morfologia )
			self.fPoS ( tok.PoS )
			self.fCPoS ( tok.CPoS )
			self.fFirstWordCap ( form, tok.posizione )
			self.fFirstWordNoCap ( form, tok.posizione )
			self.fHyphen ( form )
			self.fCapitalized ( form )
			self.fContainsDigit ( form )
			self.fContainsPunct ( form )
			self.fUpper ( form )
			self.fWordShape ( )
			self.fFirstWord ( tok.posizione )
			self.fModAdj_pre_n  ( tok )	
			self.fModAdj_post_n ( tok )
			self.fModAdj_n ( )
			self.fModAdj_pre_b ( )  
			self.fModAdj_post_b ( ) 
			self.fModAdj_b ( )
			self.fModAdj_lemmi_pre ( tok )  
			self.fModAdj_lemmi_post ( tok )
			self.fModAdj_lemmi ( tok )
			self.fModAdj_clusters ( tok )
			self.fModNum ( tok )
			self.fDet_def ( tok )  
			self.fDet_indef ( tok )
			self.fPresenzaDet ( )
			self.fAntiDip_tipo ( tok )
			self.fAntiDip_lemma ( tok )
			self.fAntiDip_PoS ( tok )
			self.fAntiDip_preposizione ( tok ) 
			self.fAntiDip_forza_associazione ( tok )
			self.fAntiDip_classe_associazione ( tok )
			self.fPresenzaDip ( tok )
			self.fDip_n ( tok )
			self.fDip_b ()
			self.fPresenzaCoDip ( tok ) 
			self.fCoDip_n ( tok )
			self.fCoDip_b ()
			self.fDip_PoS ( tok )
			self.fDip_preposizioni ( tok ) 
			self.fCoDip_PoS ( tok )
			self.fCoDip_preposizioni ( tok )
			self.fDip_lemmi ( tok )
			self.fDip_classes ( tok )
			self.fCoDip_classes ( tok )
			self.fLSO ( tok )
			
		else: # dizionario_filtro is None
			print "[Token_target] ERROR: you must set dizionario_filtro first"
			print "[Token_target] error occurs while initialising token:", tok
			sys.exit ()
	
	def from_frase (self, posizione, frase):
		self.fPoSPrev (posizione, frase)
		self.fPoSNext (posizione, frase)
		self.fCPoSPrev (posizione, frase)
		self.fCPoSNext (posizione, frase)
		self.fSeqCap (posizione, frase)
		self.fCapNext (posizione, frase)
		self.fCapPrev (posizione, frase)

	def fId (self, documento, frase, posizione):
		self.id = 'd' + str(documento) + 's' + str (frase) + 't' + str (posizione)
		return self.id
	
	def fForm (self, form):
		self.form = Token_target.hasher_forms.hash (form)
		return self.form
	
	def fLemma (self, lemma, pos):
		#normalizza i nomi comuni
		if pos == "SP":
			lemma = "sp"
		#filtro su frequenza
		elif lemma not in Token_target.dizionario_filtro or Token_target.dizionario_filtro[lemma]<_LIMITE_INFERIORE_FREQUENZE:
			lemma = "no_lemma"	
		#hash
		self.lemma = Token_target.hasher_lemmas.hash (lemma)

	def fMorfologia_genere ( self, morfologia ):
		#~ assert "gen" in morfologia, "[Token_target] ERROR: found token with no 'gen' in morfologia"
		if "gen" in morfologia:
			self.morfologia_genere = morfologia["gen"]
		else:
			self.morfologia_genere = "missing"
		
		
	def fMorfologia_numero ( self, morfologia ):
		#~ assert "num" in morfologia, "[Token_target] ERROR: found token with no 'num' in morfologia"
		if "num" in morfologia:
			self.morfologia_numero = morfologia["num"]
		else:
			self.morfologia_numero = "missing"
	
	def fPoS (self, pos):
		self.PoS = pos

	def fCPoS (self, cpos):
		self.CPoS = cpos
	
	def fFirstWordCap(self, form, posizione):
		self.FirstWordCap= 1 if (posizione==1 and form.istitle()) else 0
		return self.FirstWordCap
	
	def fFirstWordNoCap(self, form, posizione):
		self.FirstWordNoCap= 1 if (posizione==1 and not form.istitle()) else 0
		return self.FirstWordNoCap
	
	def fHyphen(self, form):
		l=form.split('-')
		self.Hyphen=1 if len(l)==2 else 0
		return self.Hyphen	

	def fFrequenzaLemmaPoS(self, lemma, dizionario_frequenze):
		tupla=tuple([lemma]+[self.PoS])
		if tupla in dizionario_frequenze:
			if dizionario_frequenze[tupla]>936:
				ret="altissima"
			elif dizionario_frequenze[tupla]>334:
				ret="alta"
			elif dizionario_frequenze[tupla]>105:
				ret="media"
			elif dizionario_frequenze[tupla]>52:
				ret="bassa"
			else:
				ret="bassissima"
		else:
			ret="bassissima"
			
		self.FrequenzaLemmaPoS=ret
		return ret

	def fFrequenzaLemmaPoS_log (self, lemma, dizionario_frequenze):
		tupla=tuple([lemma]+[self.PoS])
		if tupla in dizionario_frequenze:
			ret=round(math.log(dizionario_frequenze[tupla]))
		else:
			ret=0
			
		self.FrequenzaLemmaPoS_log=ret
		return ret

	def fFrequenzaRelativaLemmaPoS (self, lemma, soglia, dizionario_frequenze, frequenze_cumulate, massimafreq):
		tupla=tuple([lemma]+[self.PoS])
		totale=frequenze_cumulate[lemma]+1.0 if lemma in frequenze_cumulate else massimafreq		
		f = dizionario_frequenze[tupla] if tupla in dizionario_frequenze else 0.0
		ret=f/totale
		self.FrequenzaRelativaLemmaPoS=1 if ret<=soglia else 0
		return self.FrequenzaRelativaLemmaPoS
	
	def fCapitalized(self, form):
		self.Capitalized=1 if form.istitle() else 0
		return self.Capitalized

	def fContainsDigit(self, form):
		self.ContainsDigit=1 if any(c.isdigit() for c in form) else 0
		return self.ContainsDigit
	
	def fContainsPunct(self, form):
		self.ContainsPunct=1 if any(not c.isdigit() and not c.isalpha() for c in form) else 0
		return self.ContainsPunct

	def fUpper(self, form):
		self.Upper=1 if any(c.isupper() for c in form) and not form.istitle() else 0
		return self.Upper

	def fWordShape(self):
		ret=self.ContainsDigit or self.ContainsPunct or self.Upper
		self.WordShape=ret
		return self.WordShape

	def fFirstWord(self, posizione):
		self.FirstWord= 1 if posizione==1 else 0
		return self.FirstWord 
		
	def fPoSPrev(self, posizione, frase):
		self.PoSPrev='M' if not posizione-1 in frase.tokens else frase.tokens[posizione-1].PoS
		return self.PoSPrev
	
	def fPoSNext(self, posizione, frase):			
		self.PoSNext=frase.tokens[posizione+1].PoS if posizione+1 in frase.tokens else 'M'
		return self.PoSNext

	def fCPoSPrev(self, posizione, frase):
		self.CPoSPrev='M' if not posizione-1 in frase.tokens else frase.tokens[posizione-1].CPoS
		return self.CPoSPrev
	
	def fCPoSNext(self, posizione, frase):
		self.CPoSNext='M' if not posizione+1 in frase.tokens else frase.tokens[posizione+1].CPoS
		return self.CPoSNext

	def fSeqCap(self, posizione, frase):
		calcolabile=1 if (posizione-1 in frase.tokens and posizione+1 in frase.tokens) else 0
		if calcolabile:
			prevcap=frase.tokens[posizione-1].form.istitle()
			cap=frase.tokens[posizione].form.istitle()
			nextcap=frase.tokens[posizione+1].form.istitle()

			self.SeqCap=1 if (prevcap and cap and nextcap) else 0
		else:
			self.SeqCap=0
			
		return self.SeqCap

	def fCapNext(self, posizione, frase):
		calcolabile=1 if posizione+1 in frase.tokens else 0
		
		if calcolabile:
			cap=frase.tokens[posizione].form.istitle()
			nextcap=frase.tokens[posizione+1].form.istitle()
			
			self.CapNext=1 if (cap and nextcap) else 0
		else:
			self.CapNext=0
			
		return self.CapNext

	def fCapPrev(self, posizione, frase):
		calcolabile=1 if posizione-1 in frase.tokens else 0
		if calcolabile:
			cap=frase.tokens[posizione].form.istitle()
			prevcap=frase.tokens[posizione-1].form.istitle()
			
			self.CapPrev=1 if (cap and prevcap) else 0
		else:
			self.CapPrev=0
		return self.CapPrev

	def fWithinQuotes(self, boolean):
		self.WithinQuotes=1 if boolean else 0
		return self.WithinQuotes

	def fModAdj_pre_n (self, tok):
		self.ModAdj_pre_n = len (tok.ModAdj_lemmi_pre)
		return self.ModAdj_pre_n
	
	def fModAdj_post_n (self, tok):
		self.ModAdj_post_n = len (tok.ModAdj_lemmi_post)
		return self.ModAdj_post_n
		
	def fModAdj_n (self):
		self.ModAdj_n = self.ModAdj_post_n + self.ModAdj_pre_n
		return self.ModAdj_n

	def fModAdj_pre_b (self):
		self.ModAdj_pre_b = 1 if self.ModAdj_pre_n>0 else 0
		return self.ModAdj_pre_b
	
	def fModAdj_post_b (self):
		self.ModAdj_post_b = 1 if self.ModAdj_post_n>0 else 0
		return self.ModAdj_post_b
	
	def fModAdj_b (self):
		self.ModAdj_b = 1 if self.ModAdj_n>0 else 0
		return self.ModAdj_b
	
	def fModAdj_lemmi_pre (self, tok):
		ret = {}
		for lemma in tok.ModAdj_lemmi_pre:
			ret[Token_target.hasher_aggettivi.hash (lemma)] = 1
		self.ModAdj_lemmi_pre = ret;
		return ret

	#si potrebbe mettere un filtro, nel caso servisse
	def fModAdj_lemmi_post (self, tok):
		ret = {}
		for lemma in tok.ModAdj_lemmi_post:
			ret[Token_target.hasher_aggettivi.hash (lemma)] = 1
		self.ModAdj_lemmi_post = ret;
		return ret

	def fModAdj_lemmi (self, tok):
		ret = {}
		for lemma in tok.ModAdj_lemmi_post:
			ret[Token_target.hasher_aggettivi.hash (lemma)] = 1
		for lemma in tok.ModAdj_lemmi_pre:
			ret[Token_target.hasher_aggettivi.hash (lemma)] = 1
		self.ModAdj_lemmi = ret;
		return ret
	
	def fModAdj_clusters (self, tok):
		ret = {}
		for num in tok.ModAdj_cluster_pre:
			ret[Token_target.hasher_cluster.hash (num)] = 1
		for num in tok.ModAdj_cluster_post:
			ret[Token_target.hasher_cluster.hash (num)] = 1
		self.ModAdj_clusters = ret;
		return ret
	
	def fModNum (self, tok):
		self.ModNum = 1 if tok.modNum else 0
		return self.ModNum
	
	def fDet_def (self, tok):
		self.Det_def = 1 if tok.Det_def else 0
		return self.Det_def
	
	def fDet_indef (self, tok):
		self.Det_indef = 1 if tok.Det_indef else 0
		return self.Det_indef
		
	def fPresenzaDet (self):
		self.PresenzaDet = self.Det_def or self.Det_indef
		return self.PresenzaDet
	
	def fAntiDip_tipo (self, tok):
		h = 'M'
		if len(tok.AntiDip)>0:
			tipo = tok.AntiDip['tipo']
			h = Token_target.hasher_antidipendenze.hash (tipo)
		self.AntiDip_tipo =  h
		return h

	def fAntiDip_lemma (self, tok):
		h = 'M'
		if len(tok.AntiDip)>0:
			lemma = tok.AntiDip['lemma']
			h = Token_target.hasher_lemmi_antidipendenze.hash (lemma)
		self.AntiDip_lemma =  h
		return h

	def fAntiDip_PoS (self, tok):
		h = 'M'
		if len(tok.AntiDip)>0:
			pos = tok.AntiDip['PoS']
			h = Token_target.hasher_lemmi_antidipendenze.hash (pos)
		self.AntiDip_pos =  h
		return h

	def fAntiDip_preposizione (self, tok):
		h = 'M'
		if len(tok.AntiDip)>0:
			prep = tok.AntiDip['preposizione']
			h = Token_target.hasher_lemmi_antidipendenze.hash (prep)
		self.AntiDip_preposizione =  h
		return h
	
	def fAntiDip_forza_associazione (self, tok):
		h = {}
		if len(tok.AntiDip)>0:
			h = tok.AntiDip['forza_associazione']
		self.AntiDip_forza_associazione =  h
		return h
		
	def fAntiDip_classe_associazione (self, tok):
		h = {}
		if len(tok.AntiDip)>0:
			h = tok.AntiDip['classe_associazione']
		self.AntiDip_forza_associazione =  h
		return h

	def fPresenzaDip(self, tok):
		self.PresenzaDip=1 if len(tok.Dip)>0 else 0
		return self.PresenzaDip
		
	def fDip_n(self, tok):
		h={}
		for el in tok.Dip:
			h[Token_target.hasher_dipendenze.hash(el)]=len(tok.Dip[el]['lemmi'])
		self.Dip_n=h
		return h
		
	def fDip_b(self):
		h={}
		for el in self.Dip_n:
			h[el]=1
		self.Dip_b=h
		return h

	def fPresenzaCoDip(self, tok):
		self.PresenzaCoDip=1 if len(tok.CoDip)>0 else 0
		return self.PresenzaCoDip
		
	def fCoDip_n(self, tok):
		h={}
		for el in tok.CoDip:
			h[Token_target.hasher_dipendenze.hash(el)]=len(tok.CoDip[el]['lemmi'])
		self.CoDip_n=h
		return h
		
	def fCoDip_b(self):
		h={}
		for el in self.CoDip_n:
			h[el]=1
		self.CoDip_b=h
		return h
		
	def fDip_PoS(self, tok):
		h={}
		for el in tok.Dip:
			lista=tok.Dip[el]['PoS']
			for p in lista:
				h[p]=1
		self.Dip_PoS=h
		return h

	def fDip_preposizioni(self, tok):
		h={}
		for el in tok.Dip:
			lista=tok.Dip[el]['preposizioni']
			for p in lista:
				h[Token_target.hasher_preposizioni.hash(p)]=1
		self.Dip_preposizioni=h
		return h
	
	def fCoDip_PoS(self, tok):
		h={}
		for el in tok.CoDip:
			lista=tok.CoDip[el]['PoS']
			for p in lista:
				h[p]=1
		self.CoDip_PoS=h
		return h

	def fCoDip_preposizioni(self, tok):
		h={}
		for el in tok.CoDip:
			lista=tok.CoDip[el]['preposizioni']
			for p in lista:
				h[Token_target.hasher_preposizioni.hash(p)]=1
		self.CoDip_preposizioni=h
		return h
		
	def fDip_lemmi(self, tok):
		h={}
		for el in tok.Dip:
			lista=tok.Dip[el]['lemmi']
			for l in lista:
				h[Token_target.hasher_lemmi_dipendenze.hash(l)]=1
		self.Dip_lemmi=h
		return h
	
	def fDip_classes(self, tok):
		h={}
		for el in tok.Dip:
			el_hashed=Token_target.hasher_dipendenze.hash(el)
			h[el_hashed]={}
			h[el_hashed]['classes']=tok.Dip[el]['classes']
		self.Dip_classes=h
		return h
	
	def fCoDip_classes(self, tok):
		h={}
		for el in tok.CoDip:
			el_hashed=Token_target.hasher_dipendenze.hash(el)
			h[el_hashed]={}
			h[el_hashed]['classes']=tok.CoDip[el]['classes']
		self.CoDip_classes=h
		return h
					
	def fLSO(self, tok):
		self.LSO=tok.LSO
		return self.LSO
