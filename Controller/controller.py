# coding: utf-8
from os import system, name
import sys
from Config.config import CATEGORIES, NAME_OF_PRODUCT_FIELDS, URL,\
FIELDS_OF_PRODUCTS, PRODUCTS_NB , USER, PASSWORD, HOST, DATABASE
from View.menu import Menu
from Database.init_database import Initialise_database
from Database.sql_requests import Request_Sql
from API.api_requests import Request_Api
from Database.filling import Filling
from Database.tables_creation import Tables


class Show(Initialise_database):

    def __init__(self):
        Initialise_database.__init__(self)
        self.selected_category_id = 99999
        self.selected_product = []
        self.selected_substitute = []
        self.menu = Menu()
        self.request_sql = Request_Sql()
        self.request_api = Request_Api()
        self.filling = Filling()
        self.tables = Tables()
    
    def main_menu(self):
        """ displays actions of the main menu
            and launches the chosen one 
            In reception : nothing
            On return    : displays the menu and
                            triggers chosen action
        """
        self.__clear()
        # reset cursor
        show.cursor.close()
        # and reset connexion
        show.cnx.close()
        # then restart them
        show.__init__()
        # displays the main menu
        self.menu.main_menu()
        response = int(input("Sélectionnez une action : ") or 0)
        # only 4 possibles actions
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
        # the previous choice triggers one of 4 actions
        actions[response]()

    def select_category_menu(self):
        """ displays all categories from which
            the user must choose one  
        """
        self.__clear()
        # displays all categories
        self.menu.category_menu(CATEGORIES)
        response = int(input("Sélectionnez une catégorie de produits: ") or 0)
        while response not in range(1,6):
            self.__clear()
            self.menu.category_menu(CATEGORIES)
            response = int(input("Sélectionnez une catégorie de produits (1 à 5): ") or 0)
        # save the chosen category 
        self.selected_category_id = response
        # launches the display of all the products of the chosen category 
        self.select_product_of_category()

    def select_product_of_category(self):
        """ displays all products of the category
            from which the user must choose one product  
        """
        # loads all products of selected category_id
        products_of_category = self.request_sql.loads_products_of_category(self.selected_category_id)
        # number of products loaded
        PRODUCTS_NB  = len(products_of_category)
        # displays products of category...
        self.menu.display_products_of_category(products_of_category)
        # ... and asks to select one of them
        response = int(input("Sélectionnez un produit : ") or 0)
        while response not in range(1, PRODUCTS_NB +1):
            self.__clear()
            self.menu.display_products_of_category(products_of_category)
            response = int(input(f"Sélectionnez un produit (1 à {PRODUCTS_NB }): ") or 0)
        # save the chosen product 
        self.selected_product = products_of_category[response-1]
        # launches the display of chosen product as well as the possible substitutes 
        self.select_find_substitut()

    def select_find_substitut(self):
        """ displays the product selected
            as well as the possible substitutes
            from which the user must choose one
        """
        self.__clear()
        # displays details of the product selected
        self.menu.display_details_of_product(self.selected_product, NAME_OF_PRODUCT_FIELDS)
        response = int(input("Sélectionnez une option (1- chercher un substitut;"
                        " 2- retour au menu principal; 3- quitter l'application) : ") or 0)
        while response not in range(1, 4):
            self.__clear()
            self.menu.display_details_of_product(self.selected_product, NAME_OF_PRODUCT_FIELDS)
            response = int(input("Sélectionnez une option (1- chercher un substitut;"
                        " 2- retour au menu principal; 3- quitter l'application) : ") or 0)
        actions = {1: self.select_substitute_of_product, 2: self.main_menu, 3: self.quit_program}
        # launches action chosen
        actions[response]()

    def test_useful_substitutes(self, substitutes_list, nutri_test):
        """ return the substitutes whose nutriscore is lower than a nutriscore_test """
        # sorts by nutrigrade value
        substitutes_liste = self.tri_bulles(substitutes_list, 4)
        results_list = []
        # saves only the substitutes whose nutriscore is lower than 'nutri_test'
        for data in substitutes_list:
            if data[4] <= nutri_test:
                results_list.append(data)
        return results_list

    def cleaning_of_substitutes(self, substitutes_list):
        """ keeps only the substitutes whose nutriscore
            is lower than that of the product and drop
            the substitute identical to the product
        """
        # gets nutrigrade of selected product to be the 'nutri_test'
        nutri_test = self.selected_product[4]
        # selects only substituts with nurtigrade <= nutri_test
        substitutes_list = self.test_useful_substitutes(substitutes_list, nutri_test)
        # for remove the substitute identical to the product
        for i in range(len(substitutes_list)):
            # if a substitute is identical to the product 
            if substitutes_list[i][0] == self.selected_product[0]:
                substitute_index = i
        # removes the substitute identical to the product 
        del substitutes_list[substitute_index]
        return substitutes_list


    def load_substitutes_of_product(self):
        """ loads only the good substitutes of the product selected """
        # loads products of category_id from DATABASE (= substitutes)
        substitutes_list = self.request_sql.loads_products_of_category(self.selected_category_id)
        # selects only useful substituts and puts them in 'substitutes_list'
        substitutes_list = self.cleaning_of_substitutes(substitutes_list)
        return substitutes_list

    def display_product_and_substitutes(self, substitutes_list):
        """ displays a product and the finded substitutes for this product """
        self.__clear()
        # displays details of product to substitute
        print("Produit à remplacer par un substitut :")
        self.menu.display_details_of_product(self.selected_product, NAME_OF_PRODUCT_FIELDS)
        # displays all substitutes of product
        self.menu.display_substitutes_of_product(substitutes_list)

    def display_product_and_substitute(self):
        """ displays a product and the selected substitute """
        self.__clear()
        # displays details of product to substitute
        print("Produit à remplacer par un substitut : ")
        self.menu.display_details_of_product(self.selected_product, NAME_OF_PRODUCT_FIELDS)
        # displays details of product to substitute
        self.menu.display_details_of_substitute(self.selected_substitute, NAME_OF_PRODUCT_FIELDS)

    def select_substitute_of_product(self):
        """  """
        # loads list of substitutes of product in substitutes_list
        substitutes_list = self.load_substitutes_of_product()
        # numbers of finded substitutes
        substitutes_nb = len(substitutes_list)
        # asks to choose a substitute among those found 
        self.display_product_and_substitutes(substitutes_list)
        response = int(input("Sélectionnez un substitut (ou '0' pour revenir au menu) : ") or 9999)
        while response not in range(substitutes_nb + 1):
            # asks to choose a substitute among those found
            self.display_product_and_substitutes(substitutes_list)
            response = int(input("Sélectionnez un substitut (ou '0' pour revenir au menu) : ") or 9999)
        # if response=0 then back to teh main menu
        if response == 0:
            self.main_menu()
        else:
            # else records the selected substitute...
            self.selected_substitute = substitutes_list[response-1]
            # ... and asks if user wants to record it
            self.select_recording_of_substitute()

    def select_recording_of_substitute(self):
        """ asks if user wants to record selected substitute """
        # displays product and her substitut
        self.display_product_and_substitute()
        response = input("Voulez-vous enregistrer ce substitut ? (O/N) : ").upper()
        while response not in ['O', 'N']:
            # displays product and her substitut
            self.display_product_and_substitute()
            response = input("Voulez-vous enregistrer ce substitut ? (O/N) : ").upper()
        # if user wants record the substitute
        if response == 'O':
            # verifies if substitute is not already saved
            if self.exist_in_substitutes_category():
                # if already saved, proposes to choose another
                self.substitute_already_recorded()
            else:
                # else saves the substitute
                self.record_selected_substitute()
        # if user don't want record the substitute
        else:
            self.main_menu()
        
    def exist_in_substitutes_category(self):
        """ tests if 'self.selected_substitute' already exists in Substitutes table
            In reception : nothing
            On return    : 'True' if selected substitute already exists else 'False' 
        """
        # loads all substitutes recorded in table 'Substitutes'
        substitutes_recorded_dico = self.request_sql.load_recorded_substitutes()
        # search duplicate of (origin_id, substitut_id)
        presence = False
        for product in substitutes_recorded_dico:
            if (product == self.selected_product[0]) and (self.selected_substitute[0] in substitutes_recorded_dico[product]):
                presence = True
        return presence

    def substitute_already_recorded(self):
        """ in the event that a substitute is already
            registered, offers to choose another """
        # displays that the substitute is already registered
        self.menu.display_already_record(self.selected_product, self.selected_substitute)
        response = input("Voulez-vous rechercher un autre substitut au produit ? (O/N) : ").upper()
        while response not in ['O', 'N']:
            # displays that the substitute is already registered
            self.menu.display_already_record(self.selected_product, self.selected_substitute)
            response = input("Voulez-vous rechercher un autre substitut au produit ? (O/N) : ").upper()
        # offers to choose another substitute
        if response == 'O':
            self.select_substitute_of_product()
        else:
            self.main_menu()            

    def record_selected_substitute(self):
        """ records the substitute chosen by USER """
        # self.__clear()
        self.filling.fill_substitute_table(self.selected_product[0], self.selected_substitute[0])
        print("Enregistrement du substitut effectué...")
        input("")
        self.main_menu()

    def display_recorded_substitutes(self):
        """ displays all recorded substitutes """
        # loads all substitutes registered from table 'Substitutes'
        substitutes_recorded_dico = self.request_sql.load_recorded_substitutes()
        # displays name and brand of each product with her substitute(s)
        self.__clear()
        # if no substitute has been registered 
        if len(substitutes_recorded_dico) == 0:
            print()
            input(" Aucun substitut n'a été enregistré dans la base de données !")
            self.main_menu()
        else:
            # displays the substituts registered for each product
            print("Affichage des substituts enregistrés pour chaque produit :"), print()
            # substitutes_recorded_dico --> (product_id, substitute_id)
            for product_id in substitutes_recorded_dico:
                # displays 'name' and 'brand' of one product
                print("- " + self.request_sql.get_name_of_product_id(product_id), " :",  end=" ")
                # displays 'name' and 'brand' of product's substitutes
                for substitut_id in substitutes_recorded_dico[product_id]:
                    print(self.request_sql.get_name_of_product_id(substitut_id), end=", ")
                print()
                print()
            print()
            input("(appuyez sur une touche pour revenir au menu principal...)")
            self.main_menu()

    def reinitialisation_BDD_OFF(self):
        """ drop all tables of database
            then recreate and fill them  """
        self.__clear()
        print("reinitialisation de la base de données en cours...")
        # drop all tables of database
        self.tables.drop_all_tables_BDD_OFF()
        # recreate all tables of database
        self.tables.create_all_tables_BDD_OFF()
        # fills Category's table
        self.filling.fill_table_Category(CATEGORIES)
        for catg_id in CATEGORIES:
            # get the products of a category in the API
            infos_of_products = self.request_api.get_products_of_category(
                    CATEGORIES[catg_id], FIELDS_OF_PRODUCTS, PRODUCTS_NB , URL)
            # delete page break "\n" and limits length of "ingredients"
            infos_of_products = self.clean_request_api(infos_of_products)
            # and records datas in Product table
            self.filling.fill_table_Product(catg_id, infos_of_products)
        # at the end return to the main menu
        self.main_menu()

    def clean_request_api(self, infos_of_products):
        """
            cleans items of api's request
            In reception : list of product dictionaries like...
            [{'name': 'TUC', 'brand': 'LU'...}, {'name': 'Gazpacho'...}]
            On return    : same list of dictionaries but cleaned 
        """
        for info in infos_of_products:
            for data in info:
                # limits length of "ingredients
                if len(info[data]) > 350:
                    info[data] = info[data][:350]
                # delete page break "\n"
                my_txt = info[data].maketrans("\n", " ")
                info[data] = info[data].translate(my_txt)
                # delete page break "\n"
                my_txt = info[data].maketrans("\r", " ")
                info[data] = info[data].translate(my_txt)
            try:
                info['url'] = str(info['url']).replace("'", " ")
                info['product_name_fr'] = str(info['product_name_fr']).replace("'", " ")
                info['product_name_fr'] = str(info['product_name_fr']).replace("d'", "d ")
                info['brands'] = str(info['brands']).replace("'", " ")
                info['nutrition_grade_fr'] = str(info['nutrition_grade_fr']).replace("'", " ")
                info['ingredients_text_fr'] = str(info['ingredients_text_fr']).replace("'", " ")
                info['stores'] = str(info['stores']).replace("'", " ")
            except KeyError as msg:
                pass
        return infos_of_products

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
    show = Show()
    show.main_menu()
    