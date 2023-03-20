import numpy as np

class Intersection:
	def __init__(self, tauxPoisson1, tauxPoisson2):
		self.tauxPoisson1 = tauxPoisson1
		self.tauxPoisson2 = tauxPoisson2
		self.file1 = 0
		self.file2 = 0
		self.lVerte = 0
		self.duree = 20 # Durée initiale des feux verts
		self.tempsDepuisDernierChangement = 0
		
	def etape(self):
		# Nombre d'arrivées sur chaque route
		arrivees1 = np.random.poisson(self.tauxPoisson1)
		arrivees2 = np.random.poisson(self.tauxPoisson2)
		
		# Mise à jour des files
		self.file1 += arrivees1
		self.file2 += arrivees2
		
		# Mise à jour de la durée des feux verts
		self.tempsDepuisDernierChangement += 1

		if self.tempsDepuisDernierChangement >= self.duree:
			self.lVerte = (self.lVerte + 1) % 2
			self.duree = 20 # Réinitialisation
			self.tempsDepuisDernierChangement = 0
		
		# Passage des voitures au feu vert
		if self.lVerte == 0:
			self.file1 = max(0, self.file1 - 1)
		else:
			self.file2 = max(0, self.file2 - 1)
			
		# Calcul du temps d'attente total
		tempsAttente = self.file1 + self.file2
		
		# Calcul de la récompense
		recompense = -tempsAttente

		return (self.file1, self.file2, self.lVerte), recompense
		
class QLearner:
	def __init__(self, tauxApprentissage, discount, tauxExploration):
		self.tauxApprentissage = tauxApprentissage
		self.discount = discount
		self.tauxExploration = tauxExploration
		self.tableauQ = {}
		
	def choisirAction(self, etat):
		if np.random.uniform() < self.tauxExploration:
			# Exploration
			return np.random.randint(0, 41, 1)[0]
		else:
			# Exploitation
			if etat in self.tableauQ:
				return np.argmax(self.tableauQ[etat])
			
			else:
				return np.random.randint(0, 41, 1)[0]
			
	def majTableauQ(self, etat, action, recompense, prochainEtat):
		if etat not in self.tableauQ:
			self.tableauQ[etat] = np.zeros(42)

		if prochainEtat not in self.tableauQ:
			self.tableauQ[prochainEtat] = np.zeros(42)

		ancienneValeur = self.tableauQ[etat][action]
		prochainMax = np.max(self.tableauQ[prochainEtat])
		nouvelleValeur = (1 - self.tauxApprentissage) * ancienneValeur + self.tauxApprentissage * (recompense + self.discount * prochainMax)
		self.tableauQ[etat][action] = nouvelleValeur
		
def simulation(tauxPoisson1, tauxPoisson2):
	intersection = Intersection(tauxPoisson1, tauxPoisson2)
	agent = QLearner(tauxApprentissage = 0.05, discount = 0.05, tauxExploration = 0.05)
	tempsAttenteTotal1 = 0
	tempsAttenteTotal2 = 0

	for i in range(10000):
		etat = (intersection.file1, intersection.file2, intersection.lVerte)
		action = agent.choisirAction(etat)
		intersection.duree = action + 5 # Intervalle entre passage de rouge à vert
		prochainEtat, recompense = intersection.etape()
		agent.majTableauQ(etat, action, recompense, prochainEtat)
		tempsAttenteTotal1 += prochainEtat[0]
		tempsAttenteTotal2 += prochainEtat[1]
	
	moyenneTempsAttente1 = tempsAttenteTotal1 / (10000 * tauxPoisson1)
	moyenneTempsAttente2 = tempsAttenteTotal2 / (10000 * tauxPoisson2)

	print("/// RESULTATS ///")
	print("Temps d'attente total :", tempsAttenteTotal1 + tempsAttenteTotal2)
	print("Temps d'attente moyen :", (moyenneTempsAttente1 + moyenneTempsAttente2) / 2)
	print("Temps d'attente total au feu 1 :", tempsAttenteTotal1)
	print("Temps d'attente moyen au feu 1 :", moyenneTempsAttente1)
	print("Temps d'attente total au feu 2 :", tempsAttenteTotal2)
	print("Temps d'attente moyen au feu 2 :", moyenneTempsAttente2)

simulation(0.2, 0.3)