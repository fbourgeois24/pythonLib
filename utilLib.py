""" Utilitaires divers 
	- timer : timer multifonction
	- ping : ping une adresse et renvoie un booléen avec le résultat
	- log : effectue un print vers la sortie choisie (stdout ou fichier)
	"""

import time
import os, sys
import datetime


class timer:
	""" Timer multifonctions basé sur le timestamp
		Renvoie vrai ou faux
		Paramètres : 
		- time : temps entre chaque "débordement" du timer
		- basculeMode : si vrai, le timer devient une bascule (change d'état (vrai / faux) à chaque "débordement" du timer)
						si faux, le timer renvoie vrai une seule fois à chaque "débordement" du timer sinon il renvoie faux
		- initialState : utile si basculeMode est à vrai, définit l'état de départ de la bascule (vrai ou faux)
	"""
	def __init__(self, time, basculeMode=False, initialState = True):
		self.time = time
		self.oldTimeStamp = 0.0
		self.basculeMode = basculeMode
		if initialState:
			self.bascule = True
		else:
			self.bascule = False

	def eval(self):
		""" Evalue le timer, renvoie vrai ou faux suivant la configuration"""
		# récupération du timestamp actuel
		now = time.time()

		# Bascule est un mode qui change la valeur renvoyée à chaque débordement du timer
		if not self.basculeMode:	
			# Evaluation du timer
			if now > self.time + self.oldTimeStamp:
				self.oldTimeStamp = now
				return True
			else:
				return False

		else:
			if now > self.time + self.oldTimeStamp:
				self.oldTimeStamp = now
				self.bascule = not self.bascule
			if self.bascule:
				# print("bascule ON")
				return True
			else:
				# print("bascule OFF")
				return False

def ping(address):
	""" Ping une adresse, renvoie vrai si ping réussi et faux si non"""
	response = os.popen("ping -c 1 " + address)
	if "ttl" in response.read():
		return True
	else:
		return False


def log(msg, output=""):
	""" Afficher le log dans la sortie standard ou dans un fichier 
		Si rien n'est spécifié dans output : sortie standard
		Si un nom est spécifé un fichier avec ce nom sera créé """
	if output != "":
		logFile = open(output, 'a')
		print(str(datetime.datetime.now()) + " -> " + str(msg), file=logFile)
		logFile.close()
	else:
		print(str(datetime.datetime.now()) + " -> " + str(msg))





if __name__ == '__main__':
	print(ping("1.1.1.1"))
