""" Utilitaires divers 
	- timer : timer multifonction
	- ping : ping une adresse et renvoie un booléen avec le résultat
	- log : effectue un print vers la sortie choisie (stdout ou fichier)
	"""

import time
import os, sys
import datetime as dt
import platform

try:
	import yaml
except ModuleNotFoundError:
	# Installation des dépendances
	os.popen("pip install PyYAML").read()
	import yaml

import socket


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
		print(str(dt.datetime.now()) + " -> " + str(msg), file=logFile)
		logFile.close()
	else:
		print(str(dt.datetime.now()) + " -> " + str(msg))


class yaml_parametres():
	""" Gestion des paramètres dans un fichier yaml externe
		Lors de l'initialisation de la fonction, read permet de directement lire les valeurs qui seront stockées dans self.content
		Dans ce cas les valeurs ne sont évidemment pas renvoyés sous forme de dictionnaire !
	 """
	def __init__(self, path, read=False):
		self.path = path
		self.content = {}
		if read:
			self.content = self.read()

	def read(self):
		""" Lire les paramètres et les stocker dans un dictionnaire
			Lors de l'exécution de cette fonction, les paramètres sont stockés dans self.content et sont renvoyés
		 """
		try:	
			yaml_file = open(self.path, "r")
		except FileNotFoundError:
			dict_parameters = {}
		else:	
			dict_parameters = yaml.load(yaml_file, Loader=yaml.FullLoader)
			yaml_file.close()
		self.content = dict_parameters
		return dict_parameters

	def write(self, dict_parameters=None):
		""" Ecrire les paramètres dans le fichier yaml 
			Sauve les paramètres stockés.
			Si un dictionnaire est passé en paramètre, c'est lui qui est stocké sinon ce sera self.content qui sera stocké
		"""
		yaml_file = open(self.path, "w")
		if dict_parameters is not None:
			yaml.dump(dict_parameters, yaml_file)
		else:
			yaml.dump(self.content, yaml_file)
		yaml_file.close()


def get_ip(inteface_name="eth0"):
	""" Récupérer l'ip de la carte ethernet de la machine"""
	return str(os.popen('ifconfig').read().split(inteface_name)[1].split('inet')[1].split('netmask')[0].replace(" ",""))


def get_hostname():
	""" Récupérer le nom de la machine """
	return str(socket.gethostname())


def get_username():
	""" Récupérer le nom d'utilisteur courant de la machine """
	return os.getlogin()

def get_os():
	""" Récupérer l'os sur lequel le script est exécuté """
	return platform.system()


def supervisor_status():
	""" Affiche le statut du superviseur (renvoie un dictionnaire avec le nom du script comme clé et un autre dictionnaire contenenant les infos comme valeur) 
	exemple de retour de la commande de statut du superviseur:
	automate_telegram                RUNNING   pid 20523, uptime 1 day, 8:09:27
	cpu_fan                          RUNNING   pid 20519, uptime 1 day, 8:09:27
	gestion_signaux                  RUNNING   pid 20520, uptime 1 day, 8:09:27
	"""

	dict_scripts = {}
	supervisor_status = os.popen("sudo supervisorctl status").read().split("\n")[:-1]
	for script in supervisor_status:
		# rstrip permet de supprimer les espaces à la fin de la chaine de caractère
		try:
			dict_scripts[script[:33].rstrip()] = {"status": script[33:43].rstrip(), "pid": script[47:].split(",")[0], "uptime": dt.timedelta(days=int(script[61:].split("day, ")[0]),hours=int(script[61:].split("day,")[1].split(":")[0]) , minutes=int(script[61:].split("day,")[1].split(":")[2]), seconds=int(script[61:].split("day,")[1].split(":")[2]))}
		except ValueError:
			# Si la lecture échoue c'est que le script ne tourne pas et il n'y a donc pas plus d'infos
			dict_scripts[script[:33].rstrip()] = {"status": script[33:43].rstrip()}
		
	return dict_scripts