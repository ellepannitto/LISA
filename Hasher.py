#!/usr/bin/python
#coding: utf-8

class Hasher:
	
	def __init__ (self):
		self.next_hash = 0
		self.dizionario_hash = {}
	
	def hash (self, s):
		if s in self.dizionario_hash:
			ret = self.dizionario_hash[s]
		else:
			self.dizionario_hash[s] = str(self.next_hash)
			self.next_hash += 1
		return self.dizionario_hash[s]

	
