# coding: utf-8
from os import system, name
# from config import categories, name_of_product_fields
# import config
import sys

"""
Cette classe ne fait qu'afficher des éléments du menu
"""

class Menu:

	def main_menu(self):
		""" displays the main menu """
		self.__clear()
		print(
			f"1 - Rechercher un produit \n"
			f"2 - Afficher les produits substitués \n"
			f"3 - Réinitialiser la base de données \n"
			f"4 - Quitter le programme \n"
		)
		print()


	def category_menu(self, catg):
		""" displays stored categories """
		self.__clear()
		[print(key, '- ', catg[key]) for key in catg.keys()]
		print()
	

	def display_products_of_category(self, products_list):
		""" displays finded products of choosed category """
		self.__clear()
		increment = 1
		for product in products_list:
			print("{}- {} de '{}' (nutriscore {}) : {}.".format(str(increment),
								product[1], product[2], product[4], product[5]))
			increment = increment + 1
		print()


	def display_details_of_product(self, product, name_of_product_fields):
		""" displays details of a'product' """
		for i in range(1, 7):
			print('  ', name_of_product_fields[i-1], ' :', product[i])
		print()


	def display_substitutes_of_product(self, substitutes_list):
		""" displays the substitutes found for a product """
		print('Substituts trouvés pour le produit ci-dessus :')
		increment = 1
		for substitute in substitutes_list :
			print("{}- {} de '{}' (nutriscore {}) : {}.".format(str(increment), substitute[1],
												substitute[2], substitute[4], substitute[5]))
			increment += 1
		print()


	def display_details_of_substitute(self, substitute, name_of_product_fields):
		""" displays details of a 'substitute' """
		print("Substitut sélectionné pour le produit ci-dessus :")
		self.display_details_of_product(substitute, name_of_product_fields)
		print()


	def display_already_record(self, product, substitute):
		""" indicates that the selected substitute has already
			been registered for this product
		"""
		self.__clear()
		print("\t ATTENTION : le substitut sélectionné a déjà été enregistré pour ce produit !")
		print()
		# displays the product to substitut
		print('Produit à remplacer par un substitut :', product[1], '(', product[2], ')')
		print()
		# displays the substitut of product
		print('Substitut sélectionné :', substitute[1], '(', substitute[2], ')')
		print()
	

	def display_substituted_products(self, products_substitutes_result):
		""" displays all products with one or more substitutes """
		self.__clear()
		for product in products_substitutes_result:
			print("* Substitut(s) au produit", product, " :")
			for substitute in products_substitutes_result[product]:
				print("-", substitute)
			print()
		print()
	

	def display_end_of_program(self):
		""" displays the end of program """
		self.__clear()
		print('Arrêt du programme demandé...')
		print()


	def __clear(self): 
	    # for windows 
	    if name == 'nt': 
	        _ = system('cls') 
	  
	    # for mac and linux
	    else: 
	        _ = system('clear')


if __name__=='__main__':
	# sys.path.insert(0, "C:/Users/utilisateur/Desktop/Formation_OpenClassRoom/Projet_5/Projet_OFF")
	menu = Menu()
	menu.main_menu()
	input("")
	menu.category_menu()
	input("")
	products_list = [(31, 'Gazpacho', 'Alvalle', 'https', 'a', 'eau et sel (pour le goût)', ' Franprix,Magasins U,Auchan', 5), (32, 'TUC original', 'LU', 'https', 'd', 'eau et sel (pour le goût)', ' Carrefour,Irma.dk,Magasins U,E.Leclerc,REWE', 5), (33, 'Salade & Compagnie - Manhattan', 'Sodebo,salade & compagnie', 'https', 'a', 'eau et sel (pour le goût)', ' Carrefour,Super U,Auchan,Magasins U,Cora,Elclerc,Intermarche', 5), (34, 'Le bâtonnet Moelleux - 30 bâtonnets', 'Fleury Michon', 'https', 'b', 'eau et sel (pour le goût)', ' Magasins U', 5), (35, 'Carré gourmand Tomates et Mozzarella', 'Herta', 'https', 'a', 'eau et sel (pour le goût)', ' Magasins U', 5), (36, 'Le Ravioli, Pur Bouf', 'Panzani', 'https', 'b', 'eau et sel (pour le goût)', ' Banque alimentaire,Franprix,Intermarché,Auchan', 5), (37, 'Carottes râpées au citron de Sicile', 'Bonduelle', 'https', 'a', 'eau et sel (pour le goût)', ' Magasins U', 5), (38, 'Croq soja provencal', 'Céréal Bio', 'https', 'a', 'eau et sel (pour le goût)', ' Carrefour,Intermarche,Casino,Magasins U, Leclerc', 5), (39, 'Quinoa gourmand', 'Tipiak', 'https', 'a', 'eau et sel (pour le goût)', ' carrefour,Leclerc,Magasins U', 5)]
	menu.display_products_of_category(products_list)
	input("")
	system('CLS')
	product = (35, 'Carré gourmand Tomates et Mozzarella', 'Herta', 'https', 'a', 'eau et sel (pour le goût)', ' Magasins U', 5)
	print('Affichage du produit sélectionné pour la catégorie "', categories[5],'" :')
	menu.display_details_of_product(product, name_of_product_fields)
	input("")
	system('CLS')
	print("Produit à remplacer par un substitut :")
	menu.display_details_of_product(product, name_of_product_fields)
	substitutes_list = [[31, 'Gazpacho', 'Alvalle', 'https', 'a', 'eau et sel (pour le goût)', ' Franprix,Magasins U,Auchan', 5], [33, 'Salade & Compagnie - Manhattan', 'Sodebo,salade & compagnie', 'https', 'a', 'eau et sel (pour le goût)', ' Carrefour,Super U,Auchan,Magasins U,Cora,Elclerc,Intermarche', 5], [37, 'Carottes râpées au citron de Sicile', 'Bonduelle', 'https', 'a', 'eau et sel (pour le goût)', ' Magasins U', 5], [38, 'Croq soja provencal', 'Céréal Bio', 'https', 'a',
'eau et sel (pour le goût)', ' Carrefour,Intermarche,Casino,Magasins U, Leclerc', 5], [39, 'Quinoa gourmand', 'Tipiak', 'https', 'a', 'eau et sel (pour le goût)', ' carrefour,Leclerc,Magasins U', 5]]
	substitute = (39, 'Quinoa gourmand', 'Tipiak', 'https', 'a', 'eau et sel (pour le goût)', ' carrefour,Leclerc,Magasins U', 5)
	menu.display_substitutes_of_product(substitutes_list)
	input("")
	menu.substitute_already_recorded(product, substitute)
	input("")
	products_substitutes_result = {1: [6], 32: [31, 38], 34: [31, 33, 38, 39]}
	menu.display_substituted_products(products_substitutes_result)
	input("")
	menu.display_end_of_program()
	