#!/usr/bin/python
# coding= utf-8

import sys

class Type_resolver:
	
	dizionario_possibili_liste = None
	
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
				ret = [ tuple([lista_nome]+[tipo_arff]) ]
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
