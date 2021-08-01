""" Utilitaires divers """

import time
import os


class timer:
	""" timer basé sur le timestamp """
	def __init__(self, time, basculeMode=False, initialState = True):
		self.time = time
		self.oldTimeStamp = 0.0
		self.basculeMode = basculeMode
		if initialState:
			self.bascule = True
		else:
			self.bascule = False

	def eval(self):
		""" Evalue le timer, renvoie vrai si le temps est écoulé """
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
	""" Ping une adresse, renvoie vrai si ping réussi """
	response = os.popen("ping -c 1 " + address)
	if "ttl" in response.read():
		return True
	else:
		return False





if __name__ == '__main__':
	print(ping("1.1.1.1"))
