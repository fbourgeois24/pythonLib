""" Faciliter la communication avec un arduino branché sur le port série 
	Structure des messages envoyés à l'arduino
	'type, addresse, etat'
	Si 	type = 1 -> relais
	 	type = 2 -> pwm
	adresse = numéro de la pin
	etat = 0 OU 1
"""

import serial
import time


class arduino():
	def __init__(self, port="/dev/ttyACM0", bitrate=9600, auto_connect = False):
		self.arduino = serial.Serial(port, bitrate, timeout=1)
		if auto_connect:
			time.sleep(1)
			self.connect()


	def connect(self):
		""" Ouverture du port série """
		if not self.arduino.isOpen():
			raise ConnectionError("Erreur de connexion avec l'arduino")


	def send_message(self, message = "", verify_response: bool = True) -> bool:
		""" Envoyer un message à l'arduino """

		# Envoi du message
		self.arduino.write(message)

		# On attends que l'arduino renvoie le message
		while self.arduino.inWaiting()==0: 
			pass

		# Si l'arduino a renvoyé un message
		if  self.arduino.inWaiting() > 0: 
			if verify_response:    
			    self.answer = self.arduino.readline()
			    self.arduino.flushInput()

			    # Si la réponse est = au message initial (message correctement envoyé et sortie activée)
			    if self.answer == self.message.encode():
			    	print("Com Arduino OK")
			    	return True
			    else:
			    	print("Com Arduino NOK")
			    	return False
			else:
				self.arduino.flushInput()
				return True


	def digital_write(self, pin: int, value: bool, verify_response: bool = True) -> bool:
		""" Ecriture d'une sortie TOR sur l'arduino """
		
		# Constitution et envoi du message
		if value:
			etat = 1
		else:
			etat = 0

		return self.send_message("1," + str(pin) + "," + str(etat))
		

	def analog_write(self, pin: int, value: int) -> bool:
		""" Ecriture d'une sortie pwm sur l'arduino """
		if value < 0 or value > 255:
			raise ValueError("Envoi du'une valeur pwm incorrecte vers l'arduino")
			return False

		return self.send_message("2," + str(pin) + "," + str(value))

