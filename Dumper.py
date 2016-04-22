#!/usr/bin/python
# coding= utf-8

import os
import cPickle
#~ import pickle as cPickle
	
def binary_dump (oggetto, nome_file):
	output=open(nome_file, "w")
	cPickle.dump(oggetto, output)
	output.close()

def binary_load (nome_file):
	input = open (nome_file, "r")
	ogg=cPickle.load(input)
	input.close ()
	return ogg
	
