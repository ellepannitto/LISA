#!/usr/bin/python
# coding= utf-8

import Token as T

class Frase:
    def __init__(self):
        self.tokens={}
         
    def aggiungiToken(self, lista):
        self.tokens[int(lista[0])]=T.Token(lista)
