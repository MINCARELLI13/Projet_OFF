""" module Controller to link Model and View modules """
# coding: utf-8
import sys
from Config.config import CATEGORIES, NAME_OF_PRODUCT_FIELDS
from View.show import Show
from Controller.controller_requests import Request


class Control:
    """ this class is used to link Model and View modules """

    def __init__(self):
        """ initializes variables """
        self.selected_category_id = 99999
        self.selected_product = []
        self.selected_substitute = []
        self.show = Show()
        self.request = Request()

    def main_menu(self):
        """ displays actions of the main menu
            and launches the chosen one
            In reception : nothing
            On return    : displays the menu and
                            triggers chosen action
        """
        # displays the main menu
        self.show.main_menu()
        response = self.input_int("Sélectionnez une action : ")
        # only 4 possibles actions
        while response not in range(1, 5):
            self.show.main_menu()
            response = self.input_int("Sélectionnez une action (1 à 4) : ")
        # the previous choice launches one of 4 actions
        actions = {
                1: self.category_menu,
                2: self.recorded_substitutes,
                3: self.reinitialisation_database,
                4: self.quit_program
                }
        actions[response]()

    def category_menu(self):
        """ displays all categories from which
            the user must choose one
        """
        # displays all categories
        self.show.category_menu(CATEGORIES)
        response = self.input_int("Sélectionnez une catégorie de produits : ")
        while response not in range(1, 6):
            self.show.category_menu(CATEGORIES)
            response = self.input_int("Sélectionnez une catégorie"
                                      " de produits (1 à 5) : ")
        # save the chosen category
        self.selected_category_id = response
        # launches the display of all the products of the chosen category
        self.products_of_category()

    def products_of_category(self):
        """ displays all products of the category
            from which the user must choose one product
        """
        # loads all products of selected category_id
        products_of_catg = self.request.loads_products_of_category(
                            self.selected_category_id)
        # number of products loaded
        prod_nb = len(products_of_catg)
        # displays products of category...
        self.show.display_products_of_category(products_of_catg)
        # ... and asks to select one of them
        response = self.input_int("Sélectionnez un produit : ")
        while response not in range(1, prod_nb + 1):
            self.show.display_products_of_category(products_of_catg)
            response = self.input_int(f"Sélectionnez un produit (1 à {prod_nb}) : ")
        # save the chosen product
        self.selected_product = products_of_catg[response-1]
        # launches the display of chosen product as well as the possible substitutes
        self.find_substitut()

    def find_substitut(self):
        """ displays the product selected
            as well as the possible substitutes
            from which the user must choose one
        """
        # displays details of the product selected
        self.show.display_details_of_product(
            self.selected_product, NAME_OF_PRODUCT_FIELDS)
        response = input("Souhaitez-vous trouver un substitut ? (O/N) : ").upper()
        while response not in ['O', 'N']:
            self.show.display_details_of_product(
                self.selected_product, NAME_OF_PRODUCT_FIELDS)
            response = input("Souhaitez-vous trouver un substitut ? (O/N) : ").upper()
        actions = {'O': self.select_substitute_of_product, 'N': self.main_menu}
        # launches action chosen
        actions[response]()

    def select_substitute_of_product(self):
        """
            displays a product and all her possible substitutes
            and asks to chose one of them
        """
        # loads list of substitutes of product in substitutes_list
        substitutes_list = self.load_substitutes_of_product()
        # numbers of finded substitutes
        substitutes_nb = len(substitutes_list)
        # asks to choose a substitute among those found
        self.display_product_and_substitutes(substitutes_list)
        response = self.input_int("Sélectionnez un substitut"
                                  " (ou '0' pour revenir au menu) : ")
        while response not in range(substitutes_nb + 1):
            # displays the product and her substitutes
            self.display_product_and_substitutes(substitutes_list)
            # asks to choose a substitute among those found
            response = self.input_int("Sélectionnez un substitut "
                                      "(ou '0' pour revenir au menu) : ")
        # if response=0 then back to the main menu
        if response == 0:
            self.main_menu()
        else:
            # else select the substitute = (38, 'Gazpacho', 'Alvalle'...)
            self.selected_substitute = substitutes_list[response-1]
            # ... and asks if user wants to record it
            self.select_recording_substitute()

    def load_substitutes_of_product(self):
        """ loads only the 'good' substitutes of the product selected """
        # loads products of category_id from DATABASE (= substitutes)
        substitutes_list = self.request.loads_products_of_category(
                           self.selected_category_id)
        # selects only useful substituts and puts them in 'substitutes_list'
        substitutes_list = self.cleaning_of_substitutes(substitutes_list)
        return substitutes_list

    def display_product_and_substitutes(self, substitutes_list):
        """ displays a product and the finded substitutes for this product """
        # displays details of product to substitute
        title = "Produit à remplacer par un substitut : "
        self.show.display_details_of_product(self.selected_product,
                                             NAME_OF_PRODUCT_FIELDS, title)
        if substitutes_list:
            # displays all substitutes of product
            self.show.display_substitutes_of_product(substitutes_list)
        # if no substitutes to propose
        else:
            print("Aucun substitut n'a été trouvé pour le produit ci-dessus !")
            print()

    def display_product_and_substitute(self):
        """ displays a product and the selected substitute """
        # displays details of product to substitute
        title = "Produit à remplacer par un substitut : "
        self.show.display_details_of_product(self.selected_product,
                                             NAME_OF_PRODUCT_FIELDS, title)
        # displays details of product to substitute
        self.show.display_details_of_substitute(self.selected_substitute,
                                                NAME_OF_PRODUCT_FIELDS)

    def cleaning_of_substitutes(self, substitutes_list):
        """ keeps only the substitutes whose nutriscore
            is lower than that of the product and drop
            the substitute identical to the product
            In reception : list of substitutes
            like -> [(32, 'Gazpacho', 'Alvalle',...),...]
            On return    : list of substitutes
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

    def test_useful_substitutes(self, substitutes_list, nutri_test):
        """ return the substitutes whose nutriscore
            is lower than a nutriscore_test
            In reception : list of substitutes
            like -> [(32, 'Gazpacho', 'Alvalle',...),...]
                           nutriscore test like 'a'
            On return    : list of substitutes
        """
        results_list = []
        # saves only the substitutes whose nutriscore is lower than 'nutri_test'
        for data in substitutes_list:
            if data[4] <= nutri_test:
                results_list.append(data)
        return results_list

    def select_recording_substitute(self):
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
            if self.substitute_already_recorded():
                # if already saved, proposes to choose another
                self.propose_another_substitut()
            else:
                # else SAVES the substitute
                self.request.fill_table_substitutes(self.selected_product[0],
                                                    self.selected_substitute[0])
                # then back to main menu
                self.main_menu()
        # if user don't want record the substitute
        else:
            self.main_menu()

    def substitute_already_recorded(self):
        """ tests if 'self.selected_substitute' already exists in Substitutes table
            In reception : nothing
            On return    : 'True' if selected substitute already exists else 'False'
        """
        # loads all substitutes recorded in table 'Substitutes'
        substitutes_recorded_dico = self.request.load_recorded_substitutes()
        # search duplicate of (origin_id, substitut_id)
        presence = False
        # substitute_name_brand = ('Gazpacho', 'Alvalle')
        substitute_name_brand = (self.selected_substitute[1],
                                 self.selected_substitute[2])
        # tests if substitute is already recorded
        for product in substitutes_recorded_dico:
            if (product[0] == self.selected_product[1]) and\
            (substitute_name_brand in substitutes_recorded_dico[product]):
                presence = True
        return presence

    def propose_another_substitut(self):
        """ in the event that a substitute is already
            registered, offers to choose another """
        # displays that the substitute is already registered
        self.show.display_already_record(self.selected_product,
                                         self.selected_substitute)
        response = input("Voulez-vous rechercher un autre "
                         "substitut au produit ? (O/N) : ").upper()
        while response not in ['O', 'N']:
            # displays that the substitute is already registered
            self.show.display_already_record(self.selected_product,
                                             self.selected_substitute)
            response = input("Voulez-vous rechercher un autre "
                             "substitut au produit ? (O/N) : ").upper()
        # offers to choose another substitute
        if response == 'O':
            self.select_substitute_of_product()
        else:
            self.main_menu()

    def recorded_substitutes(self):
        """ displays all recorded substitutes """
        # loads all substitutes registered from table 'Substitutes'
        substitutes_recorded_dico = self.request.load_recorded_substitutes()
        # displays name and brand of each product with her substitute(s)
        self.show.display_recorded_substitutes(substitutes_recorded_dico)
        # back to main menu
        self.main_menu()

    def reinitialisation_database(self):
        """ drop all tables of database
            then recreate and fill them  """
        self.show.display_reinitialisation_database()
        self.request.reinitialisation_database()
        self.main_menu()

    def input_int(self, message):
        """ this is equivalent to doing int(input("...")) """
        try:
            response = int(input(message) or 99999)
        except ValueError:
            response = 99999
        return response

    def quit_program(self):
        """ end of program """
        self.show.display_end_of_program()
        sys.exit()


if __name__ == '__main__':
    pass
