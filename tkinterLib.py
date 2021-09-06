from tkinter import * # Pour l'interface graphique
from tkinter.messagebox import * # Pour les messages popup
from tkinter.filedialog import * # Pour la sélection d'un fichier
from tkinter.ttk import * # Pour la création du tableau


#################################################################################################################################################################################
# Gestion fenêtres
#################################################################################################################################################################################


''' Barre de défilement'''
class AutoScrollbar(Scrollbar):
	def set(self, lo, hi):
		if float(lo) <= 0.0 and float(hi) >= 1.0:
			# grid_remove is currently missing from Tkinter!
			self.tk.call("grid", "remove", self)
		else:
			self.grid()
		Scrollbar.set(self, lo, hi)
	def pack(self, **kw):
		raise TclError("cannot use pack with this widget")
	def place(self, **kw):
		raise TclError("cannot use place with this widget")



''' Gestion de fenêtres '''
class window:
	""" Classe pour la gestion des fenêtres"""


	def __init__(self, title, size, main = False, scrollbar = False, menu = None, function = None):
		""" Constructeur qui stocke le titre et la taille de la fenêtre"""
		self.title = title
		self.size = size
		self.mainWindow = main
		self.scrollbarActivate = scrollbar
		self.menu = menu
		self.function = function

		



	def open(self, title=None):
		""" Méthode qui ouvre la fenêtre ou la fait passer au premier plan si elle est déjà ouverte
		Elle peut afficher un menu ou une barre de défilement sur la fenêtre"""
		try:
			self.w.focus_force()
			self.w.lift()
			return True
		except:
			self.w = Tk()
			if title == None:
				self.w.title(self.title)
			else:
				self.w.title(title)
			self.w.geometry(self.size)
			# Affichage du menu
			if self.menu != None:
				self.menuBar = Menu(self.w)
				
				# Boucle qui lit le dicttionnaire des menus et qui les génèrent
				"""
				Exemple de dictionnaire
				dictMenu = [
					{"nom":"Fichier","enfants":[
						{"nom":"Sauvegarder","fonction":None, "raccourci":None},
							{"nom":"_","fonction":None, "raccourci":None},
						{"nom":"Quitter","fonction":lambda: sys.exit(0), "raccourci":"<Mod1-q>"},
						]},
					{"nom":"Gérer","enfants":[
						{"nom":"Signaux","fonction":fnSignauxWindow, "raccourci":None},
						]}]

				"""
				for item in self.menu:	
					newMenu = Menu(self.menuBar, tearoff=0)
					self.menuBar.add_cascade(label=item["nom"], menu = newMenu)
					for subItem1 in item["enfants"]:
						newMenu2 = Menu(self.menuBar, tearoff=0)
						try:
							# on teste si il y a des enfants, si oui c'est un sous menu
							test = subItem1["enfants"]
						except:
							# Elément de menu
							if subItem1["nom"] == "_":
								newMenu.add_separator()
							else:
								newMenu.add_command(label=subItem1["nom"], command=subItem1["fonction"])
								if subItem1["raccourci"] != None:
									newMenu.bind_all(subItem1["raccourci"], subItem1["fonction"])
						else:
							# Sous-menu
							newMenu2 = Menu(newMenu, tearoff=0)
							newMenu.add_cascade(label=subItem1["nom"], menu = newMenu2)
							for subItem2 in subItem1["enfants"]:
								if subItem2["nom"] == "_":
									newMenu2.add_separator()
								else:
									newMenu2.add_command(label=subItem2["nom"], command=subItem2["fonction"])
									if subItem2["raccourci"] != None:
										newMenu2.bind_all(subItem2["raccourci"], subItem2["fonction"])


				# for item in self.menu:	
				# 	newMenu = Menu(self.menuBar, tearoff=0)
				# 	self.menuBar.add_cascade(label=item["nom"], menu = newMenu)
				# 	for subItem in item["enfants"]:
				# 		if subItem["nom"] == "_":
				# 			newMenu.add_separator()
				# 		else:
				# 			newMenu.add_command(label=subItem["nom"], command=subItem["fonction"])
				# 			if subItem["raccourci"] != None:
				# 				newMenu.bind_all(subItem["raccourci"], subItem["fonction"])



				
				# On attache le menu à la fenêtre principale
				self.w.config(menu = self.menuBar)
			# Affichage de la barre de défilement
			if self.scrollbarActivate:
				self.vscrollbar = AutoScrollbar(self.w)
				self.vscrollbar.grid(row=0, column=1, sticky=N+S, rowspan=3)
				self.hscrollbar = AutoScrollbar(self.w, orient=HORIZONTAL)
				self.hscrollbar.grid(row=3, column=0, sticky=E+W)
				self.upFixFrame = Frame(self.w)
				self.upFixFrame.grid(row=0, column=0, sticky=E+W)
				self.canvas = Canvas(self.w, yscrollcommand=self.vscrollbar.set, xscrollcommand=self.hscrollbar.set)
				self.canvas.grid(row=1, column=0, sticky=N+S+E+W)
				self.dnFixFrame = Frame(self.w)
				self.dnFixFrame.grid(row=2, column=0, sticky=E+W)
				self.vscrollbar.config(command=self.canvas.yview)
				self.hscrollbar.config(command=self.canvas.xview)
				self.w.grid_rowconfigure(1, weight=1)
				self.w.grid_columnconfigure(0, weight=1)
				self.scrlFrame = Frame(self.canvas)
				self.scrlFrame.rowconfigure(1, weight=1)
				self.scrlFrame.columnconfigure(1, weight=1)	
				self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)
			else:
				self.upFixFrame = Frame(self.w)
				self.upFixFrame.pack(fill="both")
				self.scrlFrame = Frame(self.w)
				self.scrlFrame.pack(fill="both", expand="yes")
				self.dnFixFrame = Frame(self.w)
				self.dnFixFrame.pack(fill="both")
			return False

	def close(self, ask = False, title = None, message = None):
		""" Méthode qui ferme la fenêtre"""
		if title != None or message != None or ask == True:
			if title != None:
				boxTitle = title
			else:
				boxTitle = "Fermer cette fenêtre ?"
			if message != None:
				boxMessage = message
			else:
				boxMessage = "Êtes vous sur de vouloir fermer cette fenêtre ?"
			if not askyesno(boxTitle, boxMessage):
				return
		try:
			self.w.destroy()
		except:
			pass


	def reopen(self, parameter=None):
		""" Méthode qui ferme puis réouvre la fenêtre"""
		try:
			self.w.destroy()
		except:
			pass
		if parameter == None:
			self.function()
		else:
			self.function(parameter)

		



	def loop(self):
		""" Méthode pour que la scrollbar fonctionne, à appeler en fin de fonction"""
		if self.scrollbarActivate:
			self.canvas.create_window(0, 0, anchor=NW, window=self.scrlFrame)
			self.scrlFrame.update_idletasks()
			self.canvas.config(scrollregion=self.canvas.bbox("all"))
		if self.mainWindow:
			self.w.mainloop()


	def onMouseWheel(self, event):
		""" Méthode pour défiler la fenêtre à l'aide de la roulette """
		shift = (event.state & 0x1) != 0
		scroll = -1 if event.delta > 0 else 1
		if shift:
		   self.canvas.xview_scroll(scroll*4, "units")
		else:
		   self.canvas.yview_scroll(scroll, "units")

	def dataSaved(self):
		""" Affichage de la fenêtre de sauvegarde réussie """
		self.dataSavedWindow = Toplevel()
		self.dataSavedWindow.title("Données sauvegardées")
		self.dataSavedWindow.geometry("550x50+250+300")
		Label(self.dataSavedWindow, text="Les données ont bien été sauvegardées", font=("Helvetica, 30")).pack()
		# self.dataSavedWindow.wx_attributes("-topmost", 1)
		self.dataSavedWindow.after(1000, self.dataSavedWindow.destroy)


	# def selectedLine(self, object):
	# 	""" Renvoie la valeur de la ligne sélectionnée """
	# 	return object.get()


	def showAsTable(self,titles,data,selectFn=None,ajout=True, edit=True,editFn=None,supprFn=None):
		""" Méthode pour afficher une liste comme tableau
		La scrollbar de la fenêtre doit être désactivée
		titles est une liste qui contient les titres des colonnes
		data contient les infos à afficher (liste sur 2 niveaux pour lignes et colonnes)
			Dans les colonnes, la permière ne sera pas affichée et servira de valeur renvoyée à la sélection d'une ligne
		selectFn : Fonction appelée par le bouton "Sélectionner". Appelle la fonction passée avec le paramètre id=id de la ligne sélectionnée
		editFn : Fonction déclenchée par le bouton "Ajout" ou "Modification" appelle la fonction passée avec les paramètres 
			- id=0 et create=True si ajout (paramètre ajout=True)
			- id=id de la ligne sélectionnée et create = False si modification(paramètre edit=True)
		supprFn : Fonction déclenchée par le bouton "Supprimer", appelle la fonction passée avec le paramètre id=id de la ligne sélectionnée
		"""


		def fixed_map(option):
		    """ Fonction pour résoudre un bug dans l'affichage des lignes colorées """
		    return [elm for elm in style.map('Treeview', query_opt=option) if
		        elm[:2] != ('!disabled', '!selected')]

	
		def actionSelected(suppr=False, create=False, select=False):
			""" Vérifier si une ligne a bien été sélectionnée si bouton editer ou supprimer """
			# Si suppr ou create = False on vérifie si une ligne a bien été sélectionnée
			if (suppr or ((not suppr) and not create)) and tableau.focus() == "":
				# Le message est adapté suivant le type d'action (de bouton pressé)
				if (not suppr) and not select:
					action = "modifier"
				elif not suppr:
					action = "sélectionner"
				else:
					action = "supprimer"
				showwarning("Pas de ligne sélectionnée","Aucune ligne n'a été sélectionnée, veuillez sélectionner une ligne pour pouvoir la " + action, master=frameTableau)
				return
	
			
			# Si sélection
			if select:
				selectFn(id=tableau.focus())
			# Si suppression
			elif suppr:
				supprFn(id=tableau.focus())
			# Si création
			elif create:
				editFn(id=0, create=True)
			# Sinon modification
			else:
				editFn(id=tableau.focus(), create=False)


		# Vérification si des infos à afficher ont bien été transmises
		if data is None:
			print("Aucune info à afficher !")
			return


		# Définition du style pour le tableau
		style = Style()
		style.theme_use('default')
		# style.configure('Treeview', bg='#D3D3D3', fg='black', rowheight=25, fieldbackground='#D3D3D3')
		# style.map('Treeview',bg=[('selected','#347083')])
		style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))

		
		# Création d'une frame pour y mettre le tableau
		frameTableau = Frame(self.scrlFrame)
		frameTableau.pack(pady=10, expand=YES, fill=BOTH)

		# Création d'une frame pour mettre les boutons au dessus du tableau
		frameBoutons = Frame(frameTableau)
		frameBoutons.pack(fill=X)

		# Ajout des boutons, on active seulement les boutons pour lesquels une fonction a été fournie
		if selectFn != None:
			Button(frameBoutons, text="Sélectionner", command=lambda: actionSelected(select=True)).pack(side=LEFT, padx=10, pady=10)
		if editFn != None:
			if ajout:
				Button(frameBoutons, text="Ajouter", command=lambda: actionSelected(create=True)).pack(side=LEFT, padx=10, pady=10)
			if edit:
				Button(frameBoutons, text="Editer", command=lambda: actionSelected(create=False)).pack(side=LEFT, padx=10, pady=10)
		if supprFn != None:
			Button(frameBoutons, text="Supprimer", command=lambda: actionSelected(suppr=True)).pack(side=LEFT, padx=10, pady=10)


		# Création de la barre de défilement pour le tableau
		scrollbarYTableau = Scrollbar(frameTableau)
		scrollbarYTableau.pack(side=RIGHT,fill=Y)
		scrollbarXTableau = Scrollbar(frameTableau, orient='horizontal')
		scrollbarXTableau.pack(side=BOTTOM,fill=X)

		# Création du tableau et définition des colonnes (le nom de la colonne = le titre de la colonne)
		tableau = Treeview(frameTableau, yscrollcommand=scrollbarYTableau.set, xscrollcommand=scrollbarXTableau.set, selectmode='extended', columns=(titles))
		# Spécification des colonnes
		for item in titles:
			tableau.column(item, anchor=CENTER)
		scrollbarYTableau.config(command=tableau.yview)
		scrollbarXTableau.config(command=tableau.xview)
		

		# Attribution du titre à la colonne
		for id, item in enumerate(titles):
			tableau.heading(id, text=item, anchor=CENTER)
		# On masque la colonne "text" qui apparait à gauche
		tableau['show'] = 'headings'

		tableau.pack(pady = (0, 10), expand=YES, fill=BOTH)

		

		# On insère dans le tableau toutes les lignes suivantes contenues dans la liste
		for id, item in enumerate(data):
 			# Si c'est une ligne impaire, on la colorie
			if id % 2 != 0:
				tableau.insert('', 'end', iid=item[0], values=(item[1:]), tags=("ligneCouleur",))
			else:
				tableau.insert('', 'end', iid=item[0], values=(item[1:]), tags=("ligneBlanche",))

		# Configuration des tags pour la coloration d'une ligne sur 2
		tableau.tag_configure('ligneCouleur', background='lightblue')
		tableau.tag_configure('ligneBlanche', background='white')

