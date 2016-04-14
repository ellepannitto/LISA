#!/usr/bin/python
# coding= utf-8

class AssociazioniClass:
	"""
	Memorizza una lista di oggetti di classe Dependency  
	"""
	
	def __init__(self, file_associazioni):
		"""
		Costruttore di default:
		 inizializza la lista di dipendenze leggendola dal file passato come parametro
		"""
		self.listaAssociazioni={}
		self.leggi(file_associazioni)

	def leggi(self, file_associazioni):
		"""
		Estende la lista di dipendenze con quelle lette dal file passato come parametro
		"""
		with open(file_associazioni, 'r') as f:
			f.readline()
			for line in f:
				self.addDependency(line.split())
	
	def addDependency(self, lista):
		"""
		Aggiunge una dipendenza alla lista memorizzata
		"""
		chiave=tuple([lista[1].split('_')[0]]+[lista[0].split('-')[0]])
		if not chiave in self.listaAssociazioni:
			self.listaAssociazioni[chiave]=[]
		self.listaAssociazioni[chiave].append(Dependency(lista))
		
		
class Dependency:
	"""
	Memorizza informazioni riguardo a una dipendenza fra token.
	 Di ogni dipendenza viene salvato: il tipo, la preposizione, il lemma e la pos dell'ascendente e la frequenza
	"""
	
	def __init__(self, lista):
		"""
		Costruttore di default.
		 Crea una nuova istanza di Dependency a partire da una lista in questo formato:
		 
		 TODO: descrivere il formato
		 
		"""
		split_tipo=lista[1].split('_')
		self.tipo=split_tipo[0]
		self.preposizione=split_tipo[1] if len(split_tipo) >1 else 'X'
		
		ascendente=lista[0].split('-')
		self.lemma_ascendente=ascendente[0]
		self.PoS_ascendente=ascendente[1]
		
		self.LSO=lista[2]
		
		self.frequenza=float(lista[3])
		self.frequenza_relativa=float(lista[4])
		
		#print "[Associazioni Class]nuovo elemento aggiunto:", self.tipo, self.preposizione, self.lemma_ascendente, self.PoS_ascendente, self.LSO, self.frequenza
		#m = raw_input ()
