#!/usr/bin/python
# coding= utf-8


class Token:
	"""
	Memorizza 
	"""
	
	
	frequenze_lemmi={}
	
	def aggiorna_frequenze(self):
		if self.lemmi in Token.frequenze_lemmi:
			Token.frequenze_lemmi[self.lemmi]+=1
		else:
			Token.frequenze_lemmi[self.lemmi]=1
	
	def __init__(self, lista):
		
		self.reset()
		
		self.posizione=int(lista[0])
				
		self.form=lista[2]
		self.lemma=lista[3
		
		self.aggiorna_frequenze()
		
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


	def fMorfologia(self, stringa):
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
		for lemma in lista_pre:
			self.ModAdj_lemmi_pre.add(lemma)
			
			if lemma in mappa_cluster:
				lista=mappa[lemma]
				for c in lista:
					self.ModAdj_cluster_pre.add(str(c))
		
		for lemma in lista_post:
			self.ModAdj_lemmi_post.add(lemma)
			
			if lemma in mappa_cluster:
				lista=mappa[lemma]
				for c in lista:
					self.ModAdj_cluster_post.add(str(c))

	def fModNum(self, modNum):
		self.ModNum=modNum
		
	def fDet(self, ddef, dindef):
		self.Det_def=ddef
		self.Det_indef=dindef


	def fAntiDip (self, lista_antidip):
		#IPOTESI: len(lista_antidip)=1 per ogni token
		#Controllare		
		el=lista_antidip[0]
		self.AntiDip['tipo']=el.tipo
		self.AntiDip['lemma']=el.lemmi[0]
		self.AntiDip['PoS']=el.PoS_testa.upper()
		self.AntiDip['preposizione']=el.preposizione
		self.AntiDip['forza_associazione']={'normalizedLL': el.normalizedLL, 'scaledLL': el.scaledLL}
		
		self.AntiDip['classe_associazione']={'ABSTRACT': el.abst, 'ANIMATE': el.anim, 'LOCATION':el.loc, 'EVENT': el.ev, 'OBJECT': el.obj}
		
		
	def fDip (self, lista_dip):
		
		for el in lista_dip:
			self.Dip[el.tipo]={}
			
			self.Dip[el.tipo]['lemmi']=el.lemmi
			self.Dip[el.tipo]['PoS']=el.PoS.keys()
			self.Dip[el.tipo]['preposizione']=el.preposizione
			self.Dip[el.tipo]['classes']={'ABSTRACT': el.abst, 'ANIMATE': el.anim, 'LOCATION':el.loc, 'EVENT': el.ev, 'OBJECT': el.obj}

		
	def fCoDip (self, lista_codip):
		for el in lista_codip:
			self.CoDip[el.tipo]={}
			
			self.CoDip[el.tipo]['lemmi']=el.lemmi
			self.CoDip[el.tipo]['PoS']=el.PoS.keys()
			self.CoDip[el.tipo]['preposizione']=el.preposizione
			self.CoDip[el.tipo]['classes']={'ABSTRACT': el.abst, 'ANIMATE': el.anim, 'LOCATION':el.loc, 'EVENT': el.ev, 'OBJECT': el.obj}



	def reset(self):
		self.ModAdj_lemmi_pre=set()
		self.ModAdj_lemmi_post=set()
		self.ModAdj_cluster_pre=set()
		self.ModAdj_cluster_post=set()
		self.modNum=False
		self.Det_def=False
		self.Det_indef=False
		self.AntiDip={}
		self.Dip={}
		self.CoDip={}
