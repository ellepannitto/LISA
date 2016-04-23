#!/usr/bin/python
# coding= utf-8

class AdjectiveCluster:
	
	def __init__(self, file_cluster):
	
		self.mappa={}
		self.leggi(file_cluster)


	def leggi(self,file_cluster):
	
		with open(file_cluster, 'r') as f:
			for line in f:
				lista=line.split("\t")
				agg=lista[0].split('-')[0]
				clusters=[el.replace("cluster:", '').replace("\n", '') for el in lista[1].split('·')]
		
				self.mappa[agg]=clusters
