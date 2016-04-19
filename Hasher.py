#!/usr/bin/python
#coding: utf-8

import codecs

class Hasher:
	"""
	Gli oggetti di questa classe vengono usati per generare dei codici univoci interi (hash) a partire da qualsiasi variabile, tipicamente stringhe
	 È gatantito che oggetti uguali abbiano lo stesso hash.
	 È garantito che oggetti diversi abbiano hash diverso
	"""
	def __init__ (self):
		"""
		Costruttore di default
		"""
		self.next_hash = 1
		self.dizionario_hash = {"MISSING_VALUE":0}
	
	def hash (self, s):
		"""
		Restituisce l'hash di una variabile
		 Parametri:
		  s: la variabile della quale calcolare l'hash
		 
		 Valore restituito:
		  l'hash di s
		"""
		if s in self.dizionario_hash:
			ret = self.dizionario_hash[s]
		else:
			self.dizionario_hash[s] = self.next_hash
			self.next_hash += 1
		return self.dizionario_hash[s]

	def dump (self, nome_file):
		file_output=codecs.open(nome_file, "w", "utf-8")
		
		for key, val in self.dizionario_hash.items():
			file_output.write(key.decode("utf-8")+"\t"+str(val)+"\n")

	
def test_hash ():
	"""
	esegue alcuni test per verificare il funzionamento della classe Hasher
	"""
	a = "Ciao Mondo"
	b = "Ciao Mondo"
	c = "Ciamo oondo"
	h = Hasher ()
	assert h.hash (a) == h.hash (b), "[Hasher] ERROR: oggetti uguali devono avere lo stesso hash"
	assert h.hash (a) == h.hash (a), "[Hasher] ERROR: oggetti uguali devono avere lo stesso hash"
	assert h.hash (a) != h.hash (c), "[Hasher] ERROR: oggetti diversi devono avere diversi hash"
	
	print "All tests successfully passed"

#uncomment to perform tests
#test_hash ()
