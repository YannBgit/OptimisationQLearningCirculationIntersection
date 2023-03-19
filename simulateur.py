import random

def afficherTraffic(t, nbPhases, vehiculesEnAttente):
	print("/// TEMPS = {t} ///")

	for i in range(nbPhases - 1):
		print("Nombre de voitures en attente dans la file {i} : {vehiculesEnAttente[i]}")

def afficherResultats(nbPhases, tempsAttente, congestions):
	print("\n/// RESULTATS ///")
	print("Le temps d'attente moyen pour un véhicule est {tempsAttente}")
	
	for i in range(nbPhases - 1):
		print("Congestion moyenne dans la file {i} : {congestions[i]}")

def simulation():
	# Initialisation des variables
	nbEtapes = 10000
	TAU = 0.2
	LAMBDA = 0.5 - TAU				# La somme de LAMBDA et TAU doit valoir 0.5
	nbPhases = 3
	dureeMin = 5
	dureeMax = 45
	dureesPhases = [10, 10, 5]		# La dernière entrée correspond à la phase de transition
	t = 0
	phaseActive = 0
	dureeActive = 0
	nbVehiculesAttente = [0, 0]
	congestions = [0, 0]
	tempsAttente = 0
	gain = 0
	reward = 0
	tauxApprentissage = 0.05
	discount = 0.5

	# Simulation
	for i in range(nbEtapes):
		[int(random.expovariate(TAU)) for i in range(10000)]
		t = t + 1

	# AFfichage final
	afficherResultats(nbPhases, tempsAttente, congestions)

# Main
simulation()