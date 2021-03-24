# coding: utf-8
from os import system, name
import sys
# import mysql.connector
from Config.config import categories, name_of_product_fields, user, password, host, database
from View.menu import Menu
from Database.init_database import Initialise_database
from Database.sql_requests import Request_Sql
from Database.filling import Filling
from Database.tables_creation import Tables


class Show(Initialise_database):

    def __init__(self):
        Initialise_database.__init__(self)
        self.selected_category_id = 99999
        self.selected_product = []
        self.selected_substitute = []
        self.menu = Menu()
        self.request = Request_Sql()
        self.filling = Filling()
        self.tables = Tables()
    

    def main_menu(self):
        """ displays choices of main menu """
        self.__clear()
        self.menu.main_menu()
        response = int(input("Sélectionnez une action : ") or 0)
        while response not in range(1,5):
            self.__clear()
            self.menu.main_menu()
            response = int(input("Sélectionnez une action (1 à 4): ") or 0)
        actions = {
            1: show.select_category_menu,
            2: show.display_recorded_substitutes,
            3: show.reinitialisation_BDD_OFF,
            4: show.quit_program
            }
        actions[response]()


    def select_category_menu(self):
        """ displays choices of main menu """
        self.__clear()
        self.menu.category_menu(categories)
        response = int(input("Sélectionnez une catégorie de produits: ") or 0)
        while response not in range(1,6):
            self.__clear()
            self.menu.category_menu(categories)
            response = int(input("Sélectionnez une catégorie de produits (1 à 5): ") or 0)
        self.selected_category_id = response
        self.select_product_of_category()



    def select_product_of_category(self):
        # loads products of selected category_id
        products_of_category = self.request.loads_products_of_category(self.selected_category_id)
        products_nb = len(products_of_category)
        # displays products of category
        self.menu.display_products_of_category(products_of_category)
        response = int(input("Sélectionnez un produit : ") or 0)
        while response not in range(1, products_nb+1):
            self.__clear()
            self.menu.display_products_of_category(products_of_category)
            response = int(input(f"Sélectionnez un produit (1 à {products_nb}): ") or 0)
        self.selected_product = products_of_category[response-1]
        # print("self.selected_product : ", self.selected_product)
        self.select_find_substitut()


    def select_find_substitut(self):
        self.__clear()
        self.menu.display_details_of_product(self.selected_product, name_of_product_fields)
        response = int(input("Sélectionnez une option (1- chercher un substitut;"
                        " 2- retour au menu principal; 3- quitter l'application) : ") or 0)
        while response not in range(1, 4):
            self.__clear()
            self.menu.display_details_of_product(self.selected_product, name_of_product_fields)
            response = int(input("Sélectionnez une option (1- chercher un substitut;"
                        " 2- retour au menu principal; 3- quitter l'application) : ") or 0)
        actions = {1: self.select_substitute_of_product, 2: self.main_menu, 3: self.quit_program}
        actions[response]()


    def select_useful_substituts(self, substitutes_list, nutri_test):
        """ selects substitutes whose nutriscore is lower than a nutriscore test """
        # substitutes_liste = self.tri_bulles(substitutes_list, 4)
        results_list = []
        for data in substitutes_list:
            if data[4] <= nutri_test:
                results_list.append(data)
        return results_list


    def cleaning_of_substitutes(self, substitutes_list):
        # get nutrigrade of selected product
        nutri_test = self.selected_product[4]
        # selects only substituts with nurtigrade <= nutrigrade of product
        substitutes_list = self.select_useful_substituts(substitutes_list, nutri_test)
        # for remove the substitute identical to the product
        for i in range(len(substitutes_list)):
            # if a substitute is identical to the product 
            if substitutes_list[i][0] == self.selected_product[0]:
                substitute_index = i
                # print("substitute_index : ", substitute_index)
        # removes the substitute identical to the product 
        del substitutes_list[substitute_index]
        return substitutes_list


    def load_substitutes_of_product(self):
        # loads substitutes of category_id from database
        substitutes_list = self.request.loads_products_of_category(self.selected_category_id)
        # selects only useful substituts and puts them in' response_substituts'
        substitutes_list = self.cleaning_of_substitutes(substitutes_list)
        return substitutes_list


    def display_product_and_substitutes(self, substitutes_list):
        """ displays a product and the finded substitutes for this product """
        self.__clear()
        # displays details of product to substitute
        print("Produit à remplacer par un substitut :")
        self.menu.display_details_of_product(self.selected_product, name_of_product_fields)
        # displays all substitutes of product
        self.menu.display_substitutes_of_product(substitutes_list)


    def display_product_and_substitute(self):
        """ displays a product and the selected substitute """
        self.__clear()
        # displays details of product to substitute
        print("Produit à remplacer par un substitut : ")
        self.menu.display_details_of_product(self.selected_product, name_of_product_fields)
        # displays details of product to substitute
        self.menu.display_details_of_substitute(self.selected_substitute, name_of_product_fields)


    def select_substitute_of_product(self):
        # loads list of substitutes of product in substitutes_list
        substitutes_list = self.load_substitutes_of_product()
        # numbers of finded substitutes
        substitutes_nb = len(substitutes_list)
        # asks to choose a substitute
        self.display_product_and_substitutes(substitutes_list)
        response = int(input("Sélectionnez un substitut (ou '0' pour revenir au menu) : ") or 9999)
        while response not in range(substitutes_nb +1):
            # asks to choose a substitute
            self.display_product_and_substitutes(substitutes_list)
            response = int(input("Sélectionnez un substitut (ou '0' pour revenir au menu) : ") or 9999)
        if response == 0:
            self.main_menu()
        else:
            # records the selected substitute
            self.selected_substitute = substitutes_list[response-1]
            self.select_recording_of_substitute()


    def select_recording_of_substitute(self):
        """ asks if user wants to record selected substitute """
        self.display_product_and_substitute()
        response = input("Voulez-vous enregistrer ce substitut ? (O/N) : ").upper()
        while response not in ['O', 'N']:
            self.display_product_and_substitute()
            response = input("Voulez-vous enregistrer ce substitut ? (O/N) : ").upper()
        # actions = {'O': self.record_selected_substitute, 'N': self.main_menu}
        if response == 'O':
            if self.exist_in_substitutes_category():
                self.substitute_already_recorded()
            else:
                self.record_selected_substitute()
        else:
            self.main_menu()
        

    def exist_in_substitutes_category(self):
        """ tests if 'self.selected_substitute' already exists in Substitutes table
            In reception : nothing
            On return    : 'True' if selected substitute already exists else 'False' 
        """
        # loads all substitutes recorded in table 'Substitutes'
        substitutes_recorded_dico = self.request.load_recorded_substitutes()
        # search duplicate of (origin_id, substitut_id)
        presence = False
        for product in substitutes_recorded_dico:
            if (product == self.selected_product[0]) and (self.selected_substitute[0] in substitutes_recorded_dico[product]):
                presence = True
        return presence


    def substitute_already_recorded(self):
        self.menu.display_already_record(self.selected_product, self.selected_substitute)
        response = input("Voulez-vous rechercher un autre substitut au produit ? (O/N) : ").upper()
        while response not in ['O', 'N']:
            self.menu.display_already_record(self.selected_product, self.selected_substitute)
            response = input("Voulez-vous rechercher un autre substitut au produit ? (O/N) : ").upper()
        if response == 'O':
            self.select_substitute_of_product()
        else:
            self.main_menu()            


    def record_selected_substitute(self):
        """ records the substitute chosen by user """
        # self.__clear()
        self.filling.fill_substitute_table(self.selected_product[0], self.selected_substitute[0])
        print("Enregistrement du substitut sélectionné...")
        quit()


    def display_recorded_substitutes(self):
        """ displays all recorded substitutes """
        # loads all substitutes recorded in table 'Substitutes'
        substitutes_recorded_dico = self.request.load_recorded_substitutes()
        # displays name and brand of each product with her substitute(s)
        self.__clear()
        print("Affichage des substituts enregistrés pour chaque produit :"), print()
        for product_id in substitutes_recorded_dico:
            print("- " + self.request.get_name_of_product_id(product_id), " :",  end=" ")
            for substitut_id in substitutes_recorded_dico[product_id]:
                print(self.request.get_name_of_product_id(substitut_id), end=", ")
            print()
        print()


    def reinitialisation_BDD_OFF(self):
        self.__clear()
        print("reinitialisation_BDD_OFF")
        self.tables.drop_all_tables_BDD_OFF()
        self.tables.create_all_tables_BDD_OFF()
        self.filling.fill_table_Category(categories)
        # Appeler l'API

        # enregistrer les infos dans la table Product
        


    def quit_program(self):
        """ end of program """
        self.__clear()
        print('Arrêt du programme demandé...')
        print()
        quit()
        print("quit_program")


    def tri_bulles(self, my_liste, column):
        for i in range (len(my_liste)-1,0, -1):
            for j in range(i):
                if my_liste[j][column]>my_liste[j+1][column]:
                    # on inverse les éléments de la liste situés aux index j et j+1
                    my_liste[j], my_liste[j+1] = my_liste[j+1], my_liste[j]
        return my_liste


    def __clear(self): 
	    # for windows 
	    if name == 'nt': 
	        _ = system('cls') 
	  
	    # for mac and linux
	    else: 
	        _ = system('clear')

if __name__=='__main__':
    sys.path.insert(0, "C:/Users/utilisateur/Desktop/Formation_OpenClassRoom/Projet_5/Projet_OFF/Controller")
    print()
    show = Show()
    show.main_menu()
    quit()
    actions = {
            1: show.select_category_menu,
            2: show.display_recorded_substitutes,
            3: show.reinitialisation_BDD_OFF,
            4: show.quit_program
            }
    # product = show.select_product_of_category(5)
    # product = (35, 'Carré gourmand Tomates et Mozzarella', 'Herta', 'https', 'a', 'eau et sel (pour le goût)', ' Magasins U', 5)
    # substitutes_list = [[31, 'Gazpacho', 'Alvalle', 'https', 'a', 'eau et sel (pour le goût)', ' Franprix,Magasins U,Auchan', 5], [33, 'Salade & Compagnie - Manhattan', 'Sodebo,salade & compagnie', 'https', 'a', 'eau et sel (pour le goût)', ' Carrefour,Super U,Auchan,Magasins U,Cora,Elclerc,Intermarche', 5], [37, 'Carottes râpées au citron de Sicile', 'Bonduelle', 'https', 'a', 'eau et sel (pour le goût)', ' Magasins U', 5], [38, 'Croq soja provencal', 'Céréal Bio', 'https', 'a', 'eau et sel (pour le goût)', ' Carrefour,Intermarche,Casino,Magasins U, Leclerc', 5], [39, 'Quinoa gourmand', 'Tipiak', 'https', 'a', 'eau et sel (pour le goût)', ' carrefour,Leclerc,Magasins U', 5]]
    substitute = (39, 'Quinoa gourmand', 'Tipiak', 'https', 'a', 'eau et sel (pour le goût)', ' carrefour,Leclerc,Magasins U', 5)
    choice = show.main_menu()
    choice_catg = actions[choice]()
    product = show.select_product_of_category()
    response_search_substitute = show.select_find_substitut()
    if response_search_substitute == 1:
        response = show.select_substitute_of_product()
    if response == 0:
        show.quit_program()
    else:
        response = show.select_recording_of_substitute()
    if response == 'O':
        if show.exist_in_substitutes_category():
            show.substitute_already_recorded()
        else:
            print("Enregistrement du substitut...")
    else:
        show.quit_program()
    # print("choice_catg :", choice_catg)
    # show.menu.category_menu(5)
    # input("")
    # show.menu.display_details_of_product(product, name_of_product_fields)
    # input("")
    # show.menu.display_details_of_substitute(substitute, name_of_product_fields)
