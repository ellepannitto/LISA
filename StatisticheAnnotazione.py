#!/usr/bin/python
# coding= utf-8

import copy

class StatisticheAnnotazione:

	def distribuzione_documenti(self):
		
		lista_ordinata = sorted(self.numeri, key=lambda x: len(x))
		
		#~ for el in lista_ordinata:
			#~ print len(el)
			
	def distribuzione_frasi(self):
		s=[]
		for el in self.numeri:
			s+=el
		
		lista_ordinata = sorted(s)
		
		#~ print lista_ordinata

	def __init__(self, corpus):

		self.dove_vanno_gli_sp={}
	
		self.lemmi_globali={}
		
		self.sostantivi={}
		#~ self.numeri=[]
		
		
		
		for n, doc in corpus.documenti.items ():
			#~ self.numeri.append([])
			for frase in doc:
				#~ self.numeri[-1].append(0)
				

				for k, tok in frase.tokens.items ():
					#~ self.numeri[-1][-1]+=1
		
					if tok.CPoS=="S":
		
						if not tok.PoS in self.sostantivi:
							self.sostantivi[tok.PoS]=0
						self.sostantivi[tok.PoS]+=1
		
						if tok.PoS=="SP":
							if not tok.LSO in self.dove_vanno_gli_sp:
								self.dove_vanno_gli_sp[tok.LSO]=0
								
							self.dove_vanno_gli_sp[tok.LSO]+=1
						else:
							if not tok.lemma in self.lemmi_globali:
								self.lemmi_globali[tok.lemma]={}
							if not tok.LSO in self.lemmi_globali[tok.lemma]:
								self.lemmi_globali[tok.lemma][tok.LSO]=[]
								
							self.lemmi_globali[tok.lemma][tok.LSO].append(n)
							
						
		print "SP:", self.dove_vanno_gli_sp
	
		print "statistiche sostantivi:", self.sostantivi
	
		print "lemmi non sp:", len(self.lemmi_globali)
		
		
		lemmi_non_ambigui = {k: v for k,v in self.lemmi_globali.items() if len(v)==1}
		
		lemmi_ambigui= {k: v for k,v in self.lemmi_globali.items() if len(v)>1}
		
		lemmi_per_classe = {el:[k for k,v in self.lemmi_globali.items() if v.keys()[0]==el] for el in ["ABSTRACT", "EVENT", "LOCATION", "ANIMATE", "OBJECT", "O"]}


		print "lemmi non ambigui in assoluto:", len(lemmi_non_ambigui)

		nuovi_lemmi_non_ambigui = copy.deepcopy(lemmi_non_ambigui)
			
		for lemma, diz in lemmi_ambigui.items():
			dizionario_per_documento={}
			for tag, docs in diz.items():
				for n in docs:
					if not n in dizionario_per_documento:
						dizionario_per_documento[n]=set()
					dizionario_per_documento[n].add(tag)
			if all(len(v)==1 for k,v in dizionario_per_documento.items()):
				nuovi_lemmi_non_ambigui[lemma] = diz
			
		print "lemmi non ambigui rispetto ai documenti:", len(nuovi_lemmi_non_ambigui)
		
		medie_rapporti={}
		for lemma in self.lemmi_globali:
			if not lemma in nuovi_lemmi_non_ambigui:
				print lemma
		
				ordinato_per_lunghezza=sorted(self.lemmi_globali[lemma].items(), key=lambda x: len(x[1]), reverse=True)
		
				#~ print ordinato_per_lunghezza
				#~ print ordinato_per_lunghezza[0][1]
					
				maxlen=len(ordinato_per_lunghezza[0][1])*1.0

				s=0
				
				#~ print maxlen
			
				for couple in ordinato_per_lunghezza[1:]:
					rapporto = len(couple[1])/maxlen
					print "\t", ordinato_per_lunghezza[0][0], "-", couple[0], "->", rapporto
					s+=rapporto
					#~ print couple[0], len(couple[1])
				s /= (len(ordinato_per_lunghezza)-1)
				
				medie_rapporti[lemma]=s
				
				#~ m=raw_input()
		
		for lemma, media in medie_rapporti.items():
			print lemma, "\t", media
		
		#~ print len(lemmi_non_ambigui)
		#~ print len(lemmi_ambigui_tra_due)
		
	
		#~ print self.lemmi_globali
	
	
		"""
		self.numero_documenti = len(corpus.documenti)
	
		self.numero_frasi = 0
		self.numero_tokens = 0
		self.sostantivi={}
		self.classi={}

		self.lemmi={}
		
		for n, doc in corpus.documenti.items ():
			for frase in doc:
				self.numero_frasi+=1
				for k, tok in frase.tokens.items ():
					self.numero_tokens+=1
					
					if tok.CPoS=="S":
						
						if not tok.PoS in self.sostantivi:
							self.sostantivi[tok.PoS] = 0
							
						self.sostantivi[tok.PoS]+=1		
								
						if not tok.LSO in self.classi:
							self.classi[tok.LSO]=0

						self.classi[tok.LSO]+=1
						
						if not tok.PoS == "SP":
							
							if not tok.lemma in self.lemmi:
								self.lemmi[tok.lemma]={}
							
							
							t=tuple([n]+[self.numero_frasi])
							#~ print t
							#~ m=raw_input()
							self.lemmi[tok.lemma][t]=tok.LSO
						
		self.lemmi_non_ambigui={}
		self.frequenze_non_ambigue={}
		for lemma in self.lemmi:
			lista = sorted(self.lemmi[lemma].items(), key= lambda x: x[0][0])
			
			if all([el[1] == lista[0][1] for el in lista]):
				tag = lista[0][1]
				
				#~ print lemma, tag
				#~ m=raw_input()
				
				if not tag in self.lemmi_non_ambigui:
					self.lemmi_non_ambigui[tag]=0
					self.frequenze_non_ambigue[tag]=0
					
				self.lemmi_non_ambigui[tag]+=1				
				self.frequenze_non_ambigue[tag]+=len(self.lemmi[lemma])
			
		print "LEMMI NON AMBIGUI:", sorted(self.lemmi_non_ambigui.items(), key=lambda x:x[1])
		print "FREQUENZE DI LEMMI NON AMBIGUI:", sorted(self.frequenze_non_ambigue.items(), key=lambda x:x[1])
		
		self.rapporti={el:(self.frequenze_non_ambigue[el]*1.0)/self.lemmi_non_ambigui[el] for el in self.frequenze_non_ambigue}
		
		print "FREQUENZE/LEMMI NON AMBIGUI:", sorted(self.rapporti.items(), key=lambda x:x[1])

		#~ self.media_frasi_per_doc = 0
		#~ self.media_token_per_frase = 0
		#~ self.media_token_per_doc = 0

		#~ self.media_sostantivi_per_frase = 0
		#~ self.media_sostantivi_per_doc = 0
		
		#~ print self.sostantivi
		#~ m=raw_input()
		#~ print self.lemmi 
		"""
