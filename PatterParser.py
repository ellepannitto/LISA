#!/usr/bin/python
# coding= utf-8

def creaChiave(stringa):
	dividi_uno=stringa.split("|")
	dividi_due=dividi_uno[1].split(".")
	
	try:
		doc=int(dividi_uno[0].replace("doc", ''))
		sentence=int(dividi_due[1].replace("sentence", ''))
		token=int(dividi_due[2].replace("token", ''))
		#~ print dividi_due[0]
		#~ m=raw_input()
		if dividi_due[0]=='training':
			b=True
		else:
			b=False
		tupla=tuple([doc]+[sentence]+[token]+[b])
	
	except ValueError:
		print 'Trovato NaN'
		tupla=tuple([0]+[0]+[0]+[0])
	
	return tupla

class Pattern:
	def __init__(self, file_pattern, sense_map, filler_dict, class_dict):
		self.records={}
		self.records_test={}
		
		self.leggi(file_pattern, sense_map, filler_dict, class_dict)
		
		
	def leggi(self, file_pattern, sense_map, filler_dict, class_dict):
		with open(file_patterns, 'r') as f:
		for line in f:
			self.addRecord(line.split(), sense_map, filler_dict, class_dict)
			
	def addRecord(self, lista, mappa, filler_dict, class_dict):
		chiave=creaChiave(lista[-1])
		
		if chiave[3]:
			self.records[chiave]=Record(lista, mappa, filler_dict, class_dict)
		else:
			self.records_test[chiave]=Record(lista, mappa, filler_dict, class_dict)
			
	def dump(self):
		for k, v in self.records.items():
			print "-----", k, "-------"
			v.dump()
			
		for k, v in self.records_test.items():
			print "-----", k, "-------"
			v.dump()
			
class AntiDip:
	
	def __init__ (self, tipo, arg, filler_dict, class_dict, filler): 
		
		split_tipo = tipo.split('_')
		self.tipo = split_tipo[0]
		self.PoS_testa = arg[0].split('-')[-1]
		#~ print self.PoS_testa
		#~ m=raw_input()
		self.preposizione = split_tipo[1] if len(split_tipo) >1 else 'X'
		self.lemmi=[]
		for el in arg:
			c=el.split('-')
			self.lemmi.append('-'.join(c[:-1]))
		
				
		tupla_filler=None
		for lemma in self.lemmi:
			if not lemma in ['essere', 'esistere']:
				tupla_filler=tuple([filler]+[self.tipo]+[lemma])
		if tupla_filler is None:
			tupla_filler=tuple([filler]+[self.tipo]+[self.lemmi[0]])
	
		#~ print tupla_filler
		#~ m=raw_input()
	
		self.frequenza_relativa=0
		self.log_likelihood=0
		self.normalizedLL=0
		self.scaledLL=0
		self.ranking=0
		
		if tupla_filler in filler_dict:
			el=filler_dict[tupla_filler]
			#~ print vars(el)
			#~ m=raw_input()
			self.frequenza_relativa=el.frequenza_relativa
			self.log_likelihood=el.log_likelihood
			self.normalizedLL=el.normalizedLL
			self.scaledLL=el.scaledLL
			self.ranking=el.ranking
			
		tupla_class=None
		for lemma in self.lemmi:
			if not lemma in ['essere', 'esistere']:
				tupla_class=tuple([self.tipo]+[lemma])
		if tupla_class is None:
			tupla_class=tuple([self.tipo]+[self.lemmi[0]])
		
		#~ print tupla_class
		#~ m=raw_input()
		
		self.abst=0
		self.anim=0
		self.loc=0
		self.ev=0
		self.obj=0
		
		
		if tupla_class in class_dict:
			el=class_dict[tupla_class]
			#~ print self.preposizione
			for occ in el:
				#~ print vars(occ)
				if occ.preposizone==self.preposizione:
					
					#~ m=raw_input()
					if occ.LSO=="ABSTRACT":
						self.abst=occ.frequenza_relativa
					elif occ.LSO=="ANIMATE":
						self.anim=occ.frequenza_relativa
					elif occ.LSO=="LOCATION":
						self.loc=occ.frequenza_relativa
					elif occ.LSO=="EVENT":
						self.ev=occ.frequenza_relativa
					elif occ.LSO=="OBJECT":
						self.obj=occ.frequenza_relativa
		
		
		#~ print self.abst, self.anim, self.loc, self.ev, self.obj
		#~ m=raw_input()
		
	def dump(self): 
		print "tipo", self.tipo 
		print "PoS_testa", self.PoS_testa 
		print "preposizione", self.preposizione

class ModAdj:
	def __init__ (self, arg=None):
		self.lista=[]
		if arg is not None:
			for el in arg:
				lemma = el.split('-')[0]
				self.lista.append (lemma)

	def dump(self):
		return self.lista


class Dip:
	def __init__ (self, tipo, arg, dizionario):
		#~ print tipo, arg
		#~ m=raw_input()
		
		split_tipo = tipo.split('_')
		
		self.n=len(arg)
		self.tipo=split_tipo[0]
		self.preposizione = split_tipo[1] if len(split_tipo) >1 else 'X'
		
		self.PoS={}

		self.abst=0
		self.anim=0
		self.loc=0
		self.ev=0
		self.obj=0
		
		self.lemmi = []
		
		#~ if len(arg)>1:
			#~ print arg
			
		for el in arg:
			#~ print el
			e=el.split("-")
			try:
				lemma='-'.join(e[:-1])
				#~ print lemma
				#~ m=raw_input()
				self.lemmi.append (lemma)
				PoS=e[-1].upper()
				self.PoS[PoS]=1 if not PoS in self.PoS else self.PoS[PoS]+1
				
				#~ print dizionario
				#~ print PoS
				#~ m=raw_input()
				
				if PoS=='S' and lemma in dizionario:
					#~ print dizionario[lemma]
					self.abst+=(1.0/len(dizionario[lemma])) if ("ABSTRACT" in dizionario[lemma]) else 0
					self.anim+=(1.0/len(dizionario[lemma])) if ("ANIMATE" in dizionario[lemma]) else 0
					self.loc+=(1.0/len(dizionario[lemma])) if ("LOCATION" in dizionario[lemma]) else 0
					self.ev+=(1.0/len(dizionario[lemma])) if ("EVENT" in dizionario[lemma]) else 0
					self.obj+=(1.0/len(dizionario[lemma])) if ("OBJECT" in dizionario[lemma]) else 0
			except IndexError:
				print "Errore PoSTagging ", e
			
			#~ print self.abst, self.anim, self.loc, self.ev, self.obj
			#~ m=raw_input()
		
		if 'S' in self.PoS:
			self.abst/=self.PoS['S']
			self.anim/=self.PoS['S']
			self.loc/=self.PoS['S']
			self.ev/=self.PoS['S']
			self.obj/=self.PoS['S']
		
		#~ print self.abst, self.anim, self.loc, self.ev, self.obj
			
		self.normalizza_classi()
		
		#~ print self.abst, self.anim, self.loc, self.ev, self.obj
		#~ m=raw_input()
	
		
		#~ if self.abst+self.anim+self.loc+self.ev+self.obj==0:
			#~ self.abst=0.2
			#~ self.anim=0.2
			#~ self.loc=0.2
			#~ self.ev=0.2
			#~ self.obj=0.2
		
			#~ if not self.PoS['S'] == 1:
				#~ print self.PoS
				#~ print self.abst, self.anim, self.loc, self.ev, self.obj
				#~ m=raw_input()

	def normalizza_classi(self):
		maggiori_zero=0.0
		minori_zero=[]
		
		if self.abst>0:
			maggiori_zero+=self.abst
		else:
			minori_zero.append("abst")
		
		if self.anim>0:
			maggiori_zero+=self.anim
		else:
			minori_zero.append("anim")	
			
		if self.loc>0:
			maggiori_zero+=self.loc
		else:
			minori_zero.append("loc")
		
		if self.ev>0:
			maggiori_zero+=self.ev
		else:
			minori_zero.append("ev")
		
		if self.obj>0:
			maggiori_zero+=self.obj
		else:
			minori_zero.append("obj")
				
		#~ print minori_zero
		if len(minori_zero)>0:
			residuo=(1-maggiori_zero)/len(minori_zero)
			#~ print "check", maggiori_zero, residuo
			
		for el in minori_zero:
			setattr(self, el, residuo)
		

	def dump(self):
		print "preposizione", self.preposizione
		print "PoS", self.PoS
		print "abst", self.abst
		print "anim", self.anim
		print "loc", self.loc
		print "ev", self.ev
		print "obj", self.obj
		
		
def print_if_true (stringa, f):
	if f:
		print stringa
		m=raw_input()

class Record:
	def __init__(self, lista, mappa, filler_dict, class_dict):
		self.reset ()
		
		filler=lista[0].split('=')[1].split('-')[0][1:]
		self.filler=filler
		#~ print filler
		for el in lista[1:-1]: 
				
			#~ print_if_true ("el: ",filler == "capacità")
			#~ print_if_true (el,filler == "capacità")
			tipo = el.split('=')[0]
			arg = el.split('=')[1].replace('"','').split(';')
					
			if '|' in tipo: #è una codipendenza
				#~ print filler, tipo.split("|")[1], arg
				#~ m=raw_input()
				self.codip.append(Dip (tipo.split("|")[1], arg, mappa))
			elif tipo.find ('-1') != -1: #è un'antidipendenza
				self.antidip.append( AntiDip (tipo[:-2], arg, filler_dict, class_dict, filler) )
			elif tipo == "det":
				self.missing_det = 0
				if len (arg) > 1:
					self.det_def = self.det_indef = 1
				elif arg[0] == 'def':
					self.det_def = 1
				else:
					self.det_indef = 1
			elif tipo == 'modnum':
				self.modNum = 1
			elif tipo.find ('modadj') != -1 : #era un modAdj
				if tipo.split ('-')[1] == 'pre':
					self.modAdj_pre = ModAdj (arg)
				else:
					self.modAdj_post = ModAdj (arg)
			else :
				self.dip.append (Dip (tipo, arg, mappa))
				#~ print filler, tipo, arg
				#~ m=raw_input()
			
		#~ print filler
		#~ print self.dip
		#~ print self.codip
		#~ m=raw_input() 
		
	def reset (self):
		self.modAdj_pre = self.modAdj_post = ModAdj()
		self.det_def = self.det_indef = 0
		self.missing_det = 1
		self.modNum = 0
		self.antidip = []
		self.dip = []
		self.codip = []
		
	def dump (self):
		print "Record:"
		if self.modAdj_pre is not None:
			print "modAdj_pre: ",
			self.modAdj_pre.dump() 
		if self.modAdj_post is not None:
			print " modAdj_post: ",
			self.modAdj_post.dump()
		print "det_def, det_indef:", self.det_def, self.det_indef 
		print "missing_det", self.missing_det 
		print "modNum", self.modNum
		print "dip: "
		for el in self.dip:
			el.dump() 
		print "codip: "
		for el in self.codip:
			el.dump()
