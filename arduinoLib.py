""" Faciliter la communication avec un arduino branché sur le port série 
	Structure des messages envoyés à l'arduino
	'type, addresse, etat'
	Si 	type = 1 -> relais
	 	type = 2 -> pwm
	adresse = numéro de la pin
	etat = 	si > -1 => valeur à écrire (0 ou 1 si digital et entre 0 et 255 pour pwm)
			si = -1 (on demande la lecture), l'arduino répond avec le type, l'adresse et la valeur à la place de l'état
"""

import serial
import time
from datetime import datetime as dt
from datetime import timedelta


class arduino():
	def __init__(self, port="/dev/ttyACM0", bitrate=9600, auto_connect = False):
		self.port = port
		self.bitrate = bitrate
		if auto_connect:
			self.connect()
		self.pin_state = [False for i in range(55)]


	def connect(self):
		""" Ouverture du port série """
		self.arduino = serial.Serial(self.port, self.bitrate, timeout=1)
		time.sleep(1)
		
		if not self.arduino.isOpen():
			raise ConnectionError("Erreur de connexion avec l'arduino")


	def send_message(self, message = "", verify_response: bool = True, response_timeout = 5) -> bool:
		""" Envoyer un message à l'arduino """

		# Envoi du message
		message += "\r" # Ajout du retour chariot
		self.arduino.write(message.encode())

		# On attends que l'arduino renvoie le message
		now = dt.now()
		while self.arduino.inWaiting()==0: 
			# Si le timeout est dépassé
			if dt.now() > now + timedelta(seconds=response_timeout):
				print(f"Aucune réponse de l'arduino après {response_timeout} sec")
				return False	
	
		# Si l'arduino a renvoyé un message
		if  self.arduino.inWaiting() > 0: 
			if verify_response:    
				answer = self.arduino.readline()
				self.arduino.flushInput()

				# Si la réponse est = au message initial (message correctement envoyé et sortie activée)
				if answer == message[:-1].encode():
					print("Com Arduino OK")
					return True
				else:
					print("Com Arduino NOK")
					return False
			else:
				self.arduino.flushInput()
				return True


	def digitalWrite(self, pin: int, value: bool, verify_response: bool = True) -> bool:
		""" Ecriture d'une sortie TOR sur l'arduino """
		
		# Constitution et envoi du message
		if value:
			etat = 1
		else:
			etat = 0

		# Update du status de la pin
		self.pin_state[pin] = value

		return self.send_message("1," + str(pin) + "," + str(etat))
		

	def analogWrite(self, pin: int, value: int) -> bool:
		""" Ecriture d'une sortie pwm sur l'arduino """
		if value < 0 or value > 255:
			raise ValueError("Envoi du'une valeur pwm incorrecte vers l'arduino")
			return False

		# Update du status de la pin
		self.pin_state[pin] = value

		return self.send_message("2," + str(pin) + "," + str(value))


	def analogRead(self, pin: int) -> int:
		""" Lecture d'une pin analogique sur l'arduino """
		pass

