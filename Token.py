#!/usr/bin/python
# coding= utf-8


class Token:
	"""
	Memorizza il singolo token del corpus con le sue proprietà
	"""
	
	frequenze_lemmi={}
	
	def aggiorna_frequenze(self):
		"""
		Aggiorna le frequenze di ogni lemma nell'attributo della classe frequenze_lemmi
		"""
		if self.lemma in Token.frequenze_lemmi:
			Token.frequenze_lemmi[self.lemma]+=1
		else:
			Token.frequenze_lemmi[self.lemma]=1
	
	def __init__(self, lista):
		"""
		Setta gli attributi di ogni token, nello specifico:
			posizione -> posizione del token all'interno della frase
			form -> forma grammaticale del token
			lemma -> lemma del token
			CPoS -> Part of Speech Coarse Grained del token
			PoS -> Part of Speech Fine Grained del token
			morfologia -> #####
			pos_testa -> posizione del token da cui dipende il token in esame
			tipo_dipendenza -> tipo di dipendenza sintattica del token dalla sua testa
			LSO -> Supersenso da assegnare
		"""
		
		self.reset()
		
		self.posizione=int(lista[0])
				
		self.form=lista[1]
		self.lemma=lista[2]
		
		self.CPoS=lista[3]
		self.PoS=lista[4]
		
		self.morfologia=self.fMorfologia(lista[5])
		self.pos_testa=int(lista[6])
		self.tipo_dipendenza_testa=lista[7]
		
		tag=lista[10]
		bio=lista[10].split("-")
		if len(bio)>1:
			self.LSO=bio[1]
		else:
			self.LSO="O"

		self.aggiorna_frequenze()


	def fMorfologia(self, stringa):
		"""
		Parsa la stringa di analisi morfologica restituendo un dizionario del tipo {categoria_morfologica:valore}
		"""
		ret={}
		if not stringa=="_":
			elementi=stringa.split("|")
			for el in elementi:
				cv=el.split("=")
				chiave=cv[0]
				valore=cv[1]
				ret[chiave]=valore
		return ret

	def fModAdj(self, lista_pre, lista_post, mappa_cluster):
		"""
	
		"""
		for lemma in lista_pre:
			self.ModAdj_lemmi_pre.add(lemma)
			
			if lemma in mappa_cluster:
				lista=mappa_cluster[lemma]
				for c in lista:
					self.ModAdj_cluster_pre.add(str(c))
		
		for lemma in lista_post:
			self.ModAdj_lemmi_post.add(lemma)
			
			if lemma in mappa_cluster:
				lista=mappa_cluster[lemma]
				for c in lista:
					self.ModAdj_cluster_post.add(str(c))

	def fModNum(self, modNum):
		"""
		"""
		self.ModNum=modNum
		#~ print modNum
		#~ print self.form, self.lemma
		#~ m=raw_input()
		
	def fDet(self, ddef, dindef):
		"""
		"""
		self.Det_def=ddef
		self.Det_indef=dindef


	def fAntiDip (self, lista_antidip):
		"""
		"""
		self.AntiDip={}
		
		
			#~ m=raw_input()
		
		
		for el in lista_antidip:
			self.AntiDip[el.tipo]={}
			
			self.AntiDip[el.tipo]['lemma']=el.lemmi[0]
			self.AntiDip[el.tipo]['PoS']=el.PoS_testa.upper()
			self.AntiDip[el.tipo]['preposizione']=el.preposizione
			self.AntiDip[el.tipo]['forza_associazione']={'normalizedLL': el.normalizedLL, 'scaledLL': el.scaledLL}
			self.AntiDip[el.tipo]['classe_associazione']={'ABSTRACT': el.abst, 'ANIMATE': el.anim, 'LOCATION':el.loc, 'EVENT': el.ev, 'OBJECT': el.obj}
		
		#~ if len(lista_antidip)>1:
			#~ print len(lista_antidip), self.lemma
			#~ print len(self.AntiDip)
			#~ m=raw_input()
		
		#~ if len(lista_antidip)>0:
			#~ el=lista_antidip[0]
			#~ self.AntiDip['tipo']=el.tipo
			#~ self.AntiDip['lemma']=el.lemmi[0]
			#~ self.AntiDip['PoS']=el.PoS_testa.upper()
			#~ self.AntiDip['preposizione']=el.preposizione
			
			
			#~ self.AntiDip['forza_associazione']={'normalizedLL': el.normalizedLL, 'scaledLL': el.scaledLL}
			#~ print "[TOKEN] debug forza_associazione:"
			#~ print self.lemma, self.Antidip['forza_associazione']
			#~ m = raw_input ();
			
			#~ self.AntiDip['classe_associazione']={'ABSTRACT': el.abst, 'ANIMATE': el.anim, 'LOCATION':el.loc, 'EVENT': el.ev, 'OBJECT': el.obj}
		
		
		#~ else:
			#print "aveva ragione Ludovica !!! <3 beccato un baco malefico"
			#~ pass
			
			
	def fDip (self, lista_dip):
		
		#~ print self.form, self.lemma
		#~ for el in lista_dip:
			#~ print vars(el)
		
		
		for el in lista_dip:
			
			if el.tipo in self.Dip:
				self.Dip[el.tipo].append({})
				p=len(self.Dip[el.tipo])-1
				self.Dip[el.tipo][p]['lemmi']=el.lemmi
				self.Dip[el.tipo][p]['PoS']=el.PoS.keys()
				self.Dip[el.tipo][p]['preposizioni']=el.preposizione
				self.Dip[el.tipo][p]['classes']={'ABSTRACT': el.abst, 'ANIMATE': el.anim, 'LOCATION':el.loc, 'EVENT': el.ev, 'OBJECT': el.obj}
				
			else:
				self.Dip[el.tipo]=[{}]
				self.Dip[el.tipo][0]['lemmi']=el.lemmi
				self.Dip[el.tipo][0]['PoS']=el.PoS.keys()
				self.Dip[el.tipo][0]['preposizioni']=el.preposizione
				self.Dip[el.tipo][0]['classes']={'ABSTRACT': el.abst, 'ANIMATE': el.anim, 'LOCATION':el.loc, 'EVENT': el.ev, 'OBJECT': el.obj}

		#~ print self.Dip
		#~ m=raw_input()

		
	def fCoDip (self, lista_codip):
		for el in lista_codip:
			if el.tipo in self.CoDip:
				self.CoDip[el.tipo].append({})
				p=len(self.CoDip[el.tipo])-1
				self.CoDip[el.tipo][p]['lemmi']=el.lemmi
				self.CoDip[el.tipo][p]['PoS']=el.PoS.keys()
				self.CoDip[el.tipo][p]['preposizioni']=el.preposizione
				self.CoDip[el.tipo][p]['classes']={'ABSTRACT': el.abst, 'ANIMATE': el.anim, 'LOCATION':el.loc, 'EVENT': el.ev, 'OBJECT': el.obj}
				
			else:
				self.CoDip[el.tipo]=[{}]
				self.CoDip[el.tipo][0]['lemmi']=el.lemmi
				self.CoDip[el.tipo][0]['PoS']=el.PoS.keys()
				self.CoDip[el.tipo][0]['preposizioni']=el.preposizione
				self.CoDip[el.tipo][0]['classes']={'ABSTRACT': el.abst, 'ANIMATE': el.anim, 'LOCATION':el.loc, 'EVENT': el.ev, 'OBJECT': el.obj}



	def reset(self):
		"""
		
		"""
		self.ModAdj_lemmi_pre=set()
		self.ModAdj_lemmi_post=set()
		self.ModAdj_cluster_pre=set()
		self.ModAdj_cluster_post=set()
		self.ModNum=False
		self.Det_def=False
		self.Det_indef=False
		self.AntiDip={}
		self.Dip={}
		self.CoDip={}
