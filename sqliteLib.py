import os, sys

try:
	import sqlite3
except ModuleNotFoundError:
	# Installation des dépendances
	os.popen("pip install db-sqlite3").read()
	import sqlite3

import time


""" Utilitaires pour gérer une db sqlite """
class sqliteDatabase:
	""" Classe pour la gestion d'une base de données sqlite
		Paramètres:
			dbName = Nom de la DB
			GUI = Type d'interface graphique utilisée
				- None (Défaut)
				- tkinter

	"""

	def __init__(self, dbName, GUI=None):
		""" Constructeur """
		self.db = ""
		self.cursor = ""
		self.name = dbName
		self.GUI = GUI
		if self.GUI not in (None, "tkinter"):
			raise TypeError("Paramètre GUI incorrect")

	def open(self, returnFormat='list'):
		""" Méthode pour se connecter à la base de données """
		if os.path.exists("./" + self.name):
			# Si la db est inacessible, on réessaye 
			for i in range(10):	
				try:
					self.db = sqlite3.connect(self.name)
					if returnFormat == 'dict':
						self.db.row_factory = sqlite3.Row
					self.cursor = self.db.cursor()
					return True
				except sqlite3.OperationalError as e: #sqlite3.OperationalError: database is locked:
					if e == "database is locked":
						time.sleep(0.2)
					else:
						print(e)
						return False
				except Exception as e:
					print(e)
					return False

		else:
			if self.GUI == 'tkinter':
				showwarning("Base de données introuvable !", "La base de données est introuvable, le programme va se fermer !!")
			sys.exit(0)



	def close(self,commit = False):
		""" Méthode pour fermer la base de données """
		if commit:
			self.commit()
		self.cursor.close()
		self.db.close()


	def backup(self, filepath=None):
		""" Méthode pour faire un backup de la base de données """
		# Ouvrir une fenêtre pour choisir la destination
		if self.GUI == 'tkinter':
			filepath = asksaveasfilename(title="Destination du backup",filetypes=[('db files','.db')], initialfile="Inventaire_jeux Backup " + time.strftime("%y%m%d%H%M"), defaultextension='.db', initialdir=dbBackupFolder)
		elif filepath is None:
			raise ValueError("Aucun chemin de backup spécifié")
		
		# Copier la DB à l'endroit indiqué
		if filepath != "" and filepath is not None:
			if self.GUI == 'tkinter':	
				try:
					copyfile(self.name, filepath)
				except Exception as e:
					showwarning("Erreur de backup", "Le backup n'a pas réussi, une erreur c'est produite : " + str(e))
				else:
					showinfo("Backup réussi", "Le backup est réussi, le fichier a été sauvegardé dans : " + str(filepath))
			else:
				copyfile(self.name, filepath)


	def execute(self,query):
		""" Méthode pour exécuter une requête """
		# Si la db est inacessible, on réessaye 
		# L'erreur est : sqlite3.OperationalError: database is locked
		for i in range(5):
			try:
				self.cursor.execute(query)
				return True
			except sqlite3.OperationalError as e: #sqlite3.OperationalError: database is locked:
				if e == "database is locked":
					time.sleep(0.2)
				else:
					print(e)
					return False
			except Exception as e:
				print(e)
				return False
			

	def exec(self,query, fetch = "all", returnFormat='list'):
		""" Méthode pour exécuter un requête et qui gère l'ouverture et la fermeture de la db automatiquement """
		# Si INSERT ou UPDATE -> commit
		if "SELECT" in query[:10]:
			commit = False
		else:
			commit = True

		# Exécution de la requête
		self.open(returnFormat)
		if self.execute(query):
			if (not commit) and fetch == "all":
				result = self.fetchall()
			elif (not commit) and fetch == "one":
				result = self.fetchone()
			self.close(commit)
			if not commit:
				if type(result) is None:
					return ["",]
				else:
					if returnFormat == 'dict':
						listResult = []
						for item in result:
							listResult.append(dict(item))
						return listResult
					else:
						return result



	def fetchall(self):
		""" Méthode pour le fetchall """
		return self.cursor.fetchall()


	def fetchone(self):
		""" Méthode pour le fetchone """
		return self.cursor.fetchone()


	def commit(self):
		""" Méthode pour exécuter le commit """
		self.db.commit()
