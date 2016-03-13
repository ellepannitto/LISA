#!/usr/bin/python
# coding= utf-8

import Frase as F


debug=open("../debug_documenti", "w")

class Corpus:
	"""
	Si occupa di parsare il corpus a partire dal file di input e aggiornare i token con l'informazione relativa alle dipendenze sintattiche.
	"""
	
	def __init__(self, file_corpus, pattern, mappa_cluster, test=0):
		"""
			Inizializza un oggetto di classe corpus.
	
			Parametri:
				file_corpus -> file di input da cui leggere il corpus
		"""
		self.documenti={}
		
		self.leggi(file_corpus)
	
		#~ print vars (F.Frase)
		#~ print vars (F)
		self.dizionario_frequenze = F.T.Token.frequenze_lemmi
		
		self.aggiorna_pattern(pattern, mappa_cluster, test)
		

	def leggi (self, file_corpus):
		"""
			Parsa il corpus.

			Parametri:
				file_corpus -> file di input nel seguente formato (CoNLL)
				
					<doc id="NUMERO_DOCUMENTO" [ins="no"]>
					<s [ins="no"]>
					id_token	form	lemma	analisi_morfologica	CPoS	PoS	posizione_testa	dipendenza_sintattica	_	_	tag
					...	
					</s>
					</doc>
		"""		
		with open(file_corpus, 'r') as f:
			dentro_doc=False
			dentro_frase=False
			d=0
			fr=-1
			
			#~ a_che_riga_sono=1
			for line in f:
				#~ print a_che_riga_sono
				#~ a_che_riga_sono += 1
				if line[-1]=="\n":
					line = line[:-1]
					
				if not dentro_doc:
					if line[0:3]=='<do' and not "ins=\"no\"" in line:
						dentro_doc=True
						d=int(line.split('"')[1])
						self.documenti[d]=[]
						fr=-1
						#~ print "[Corpus] leggo doc",d
				else:
					if not dentro_frase:
						if line[0:2]=='<s' and "ins=\"no\"" in line:
							self.documenti[d].append(F.Frase())
							fr+=1
						if line[0:2]=='<s' and not "ins=\"no\"" in line:
							dentro_frase=True
							self.documenti[d].append(F.Frase())
							fr+=1
							
						elif line[0:3]=='</d':
							dentro_doc=False
							
					else:		
						if line[0:3]=='</s':	
							dentro_frase=False
							
						else:
							self.documenti[d][fr].aggiungiToken(line.split('\t'))



	def aggiorna_pattern(self, pattern, mappa_cluster, test=0):
		"""
			Aggiorna i token con l'informazione relativa al parsing sintattico.
			
			Parametri:
				pattern -> oggetto di classe SelectedPattern
				test -> 0 se il corpus da aggiornare è il train, 1 se è il test
						(default:0)
			
		"""
		patterns=pattern.records.items()
		cluster = mappa_cluster.mappa
		if test:
			patterns=pattern.records_test.items()
		
		for k, p in patterns: 
			try:
				target = self.documenti[k[0]][k[1]-1].tokens[k[2]]
				
				frase = self.documenti[k[0]][k[1]-1]
				
				target.fModAdj(p.modAdj_pre.lista, p.modAdj_post.lista, cluster)
				target.fModNum (p.modNum)
				target.fDet(p.det_def, p.det_indef)
				target.fAntiDip (p.antidip)
				target.fDip (p.dip)					
				target.fCoDip (p.codip)
			except (IndexError, KeyError):
				#~ print "[parser_corpus] impossibile trovare il token: doc",str(k[0]),"frase",str(k[1]),"token",str(k[2]),"---",str(k[3])
				
				debug.write("impossibile trovare il token doc "+str(k[0])+" frase "+str(k[1])+" token "+str(k[2])+" "+str(k[3])+"\n")
		
		
