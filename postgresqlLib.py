import psycopg2						# DB postgresql

""" Gestion de la base de données postgresql """


class postgresqlDatabase:
	""" Classe pour la gestion de la DB """

	def __init__(self, dbName, dbServer, dbPort, dbUser, dbPassword, GUI=False, sslmode="allow", options = ""):
		self.db = None
		self.cursor = None
		self.database = dbName
		self.host = dbServer
		self.port = dbPort
		self.user = dbUser
		self.password = dbPassword
		self.GUI = GUI
		self.sslmode = sslmode # Valeurs possibles : disable, allow, prefer, require, verify-ca, verify-full
		self.options = options # Chercher dans un schéma particulier : options="-c search_path=dbo,public")


	def connect(self):
		""" Méthode pour se connecter à la base de données """
		self.db = psycopg2.connect(host = self.host, port = self.port, database = self.database, user = self.user, password = self.password, sslmode = self.sslmode, options = self.options)
		if self.db is None:
			return False
		else:
			return True

	def deconnect(self):
		""" Méthode pour déconnecter la db """
		self.db.close()

	def disconnect(self):
		""" Méthode pour déconnecter la db """
		self.db.close()

	def open(self):
		""" Méthode pour créer un curseur """
		# On essaye de fermer le curseur avant d'en recréer un 
		try:
			self.cursor.close()
		except:
			pass
		self.cursor = self.db.cursor()
		if self.cursor is not None:
			return True
		else:
			return False


	def commit(self):
		""" Méthode qui met à jour la db """
		self.db.commit()


	def close(self, commit = False):
		""" Méthode pour détruire le curseur, avec ou sans commit """
		# Si commit demandé à la fermeture
		if commit:
			self.db.commit()
		self.cursor.close()
		


	def execute(self, query, params = None):
		""" Méthode pour exécuter une requête mais qui gère les drop de curseurs """
		self.cursor.execute(query, params)


	def exec(self, query, params = None, fetch = "all"):
		""" Méthode pour exécuter une requête et qui ouvre et ferme  la db automatiquement """
		# Détermination du commit
		if not "SELECT" in query[:10]:
			commit = True
		else:
			commit = False
		self.open()
		self.cursor.execute(query, params)
		# Si pas de commit ce sera une récupération
		if not commit:	
			if fetch == "all":
				value = self.fetchall()
			elif fetch == "one":
				value = self.fetchone()
			else:
				raise ValueError("Wrong fetch type")
			self.close()
			return value
		else:
			self.close(commit=commit)


	def fetchall(self):
		""" Méthode pour le fetchall """

		return self.cursor.fetchall()


	def fetchone(self):
		""" Méthode pour le fetchone """

		return self.cursor.fetchone()


	def dateToPostgres(self, date):
		""" Méthode pour convertir une date au format JJ/MM/AAAA au format AAAA-MM-JJ pour l'envoyer dans la db """
		# print(date.split("/"))
		return str(date.split("/")[2]) + "-" + str(date.split("/")[1] + "-" + str(date.split("/")[0]))













