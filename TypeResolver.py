#!/usr/bin/python
# coding= utf-8

import sys

class Type_resolver:
	"""
	Gli oggetti di questa classe servono per risolvere e memorizzare 
	
	Oltre ai tipi di feature di base, quali possono essere `numeric`, `bool` e `class`, sono supportati tipi più complessi, definiti come prodotti cartesiani fra tipi più semplici.
	 Per esempio, potremmo voler usare come feature di nome FT la presenza o meno di una certa relazione fra il token in esame e qualcuno dei lemmi che compaiono nel corpus.
	 Per ogni lemma, il fatto che la relazione sia presente o meno può essere espressa con un valore booleano, quindi la feature in questione verrà risolta come un gruppo composto da "una feature booleana per ogni possibile lemma"
	
	I tipi complessi sono della forma T1*T2, e vengono risolti da sinistra verso destra.
	 nell'esempio, FT sarebbe di tipo lemmi*bool, dove `lemmi` è un tipo che assume come valori i possibili lemmi presenti nel corpus
	 
	Per funzionare, gli oggetti di questa classe hanno bisogno di una lista di tutti i possibili valori assunti da uno specifico tipo, come la lista di tutti i lemmi presenti nel corpus.
	 nell'esempio, il gruppo di feature derivate da FT avrà la stessa cardinalità dell'insieme di tutti i possibili lemmi presenti nel corpus
	"""
	
	dizionario_possibili_liste = None
	"""
	Il dizionario di possibili liste va settato prima di risolvere i tipi complessi.
	 ogni elemento ha chiave t e valore v, dove t è il nome del tipo e v la lista di tutti i possibili valori che quel tipo assumerà
	"""
	#~ def set_dizionario_possibili_liste (diz):
		#~ if Type_resolver.dizionario_possibili_liste is not None:
			#~ Type_resolver.dizionario_possibili_liste = diz
		#~ else:
			#~ print "[Type_resolver] Warning: multiple call of set_dizionario_possibili_liste"
			#~ print "[Type_resolver] old dizionario:", Type_resolver.dizionario_possibili_liste
			#~ print "[Type_resolver] new dizionario:", diz
			#~ print "[Type_resolver] the new dizionario will overwrite the old one"
			#~ Type_resolver.dizionario_possibili_liste = diz
	
	def __init__(self):
		"""
		costruttore di default
		"""
		self.lista_tipi={}
		
	def tipo_to_arff (self, tipo):
		tipo_arff = tipo
		if tipo=="bool":
			tipo_arff = ['0','1']
		elif not tipo=="numeric":
			lista = Type_resolver.dizionario_possibili_liste [tipo]
			#~ tipo_arff = "{"+','.join(lista)+"}"
			tipo_arff=lista
			#~ print tipo_arff
			#~ tipo_arff = self.lista_tipi [tipo]
		
		return tipo_arff
	
	def risolvi_lista (self, tipo):
		ret = []
		if tipo in Type_resolver.dizionario_possibili_liste:
			ret = Type_resolver.dizionario_possibili_liste[tipo]
		else:
			print "[Type_resolver] ERROR: unknown tipo: ", tipo
			sys.exit ()
		#~ print "DEBUG risoluzione tipo:", tipo, "->", ret
		return ret
			
	
	#~ def risolvi_tipi (self, nome, tipo):
	
		#~ if Type_resolver.dizionario_possibili_liste is not None:
			#~ ret = []
			#~ if "*" not in tipo:
				#~ tipo_arff = self.tipo_to_arff (tipo)
				#~ ret = [ tuple([nome]+[tipo_arff]) ]
			#~ else:
				#~ tipo_split = tipo.split ('*',1)
				
				#~ lista_tag = self.risolvi_lista (tipo_split[0])
				
				#~ for tag in lista_tag:
					#~ ret.extend (self.risolvi_tipi(nome+"|"+str(tag), tipo_split[1]))
		#~ else:
			#~ print "[Type_resolver] ERROR: set dizionario_possibili_liste first"
			#~ print "[Type_resolver] error occurs while resolving type:", tipo
			#~ sys.exit ()
		#~ return ret
	
	def risolvi_tipi (self, lista_nome, tipo):
	
		if Type_resolver.dizionario_possibili_liste is not None:
			ret = []
			if "*" not in tipo:
				tipo_arff = self.tipo_to_arff (tipo)
				ret = [ tuple([lista_nome]+[tipo_arff]+[tipo]) ]
			else:
				tipo_split = tipo.split ('*',1)
				
				lista_tag = self.risolvi_lista (tipo_split[0])
				
				for tag in lista_tag:
					ret.extend (self.risolvi_tipi(lista_nome+[str(tag)], tipo_split[1]))
		else:
			print "[Type_resolver] ERROR: set dizionario_possibili_liste first"
			print "[Type_resolver] error occurs while resolving type:", tipo
			sys.exit ()
		return ret
