""" this module is only used to display messages   """
# coding: utf-8
import os


class Show:
    """ this class is used to display messages   """

    def main_menu(self):
        """ displays the main menu """
        self.__clear()
        print(
            "1 - Rechercher un produit \n"
            "2 - Afficher les produits substitués \n"
            "3 - Réinitialiser la base de données \n"
            "4 - Quitter le programme \n"
            )
        print()

    def category_menu(self, catg):
        """ displays stored categories """
        self.__clear()
        [print(key, '- ', catg[key]) for key in catg.keys()]
        print()

    def display_recorded_substitutes(self, substitutes_recorded_dico):
        """ displays all recorded substitutes """
        self.__clear()
        # if no substitute has been registered
        if len(substitutes_recorded_dico) == 0:
            print()
            print("Aucun substitut n'a été enregistré dans la base de données !")
            print()
        else:
            # displays the substituts registered for each product
            print("Affichage des substituts enregistrés pour chaque produit :")
            print()
            # substitutes_recorded_dico --> (product_id, substitute_id)
            for product in substitutes_recorded_dico:
                # displays 'name' and 'brand' of one product
                print("- " + product[0] + " (" +  product[1], ") :", end=" ")
                # displays 'name' and 'brand' of product's substitutes
                for substitut in substitutes_recorded_dico[product]:
                    print(substitut[0] + " (" +  substitut[1], "), ", end=" ")
                print()
                print()
            print()
        input("(Appuyez sur une touche pour revenir au menu principal...)")

    def display_products_of_category(self, products_list):
        """ displays finded products of choosed category """
        self.__clear()
        increment = 1
        for product in products_list:
            print("{}- {} de '{}' (nutriscore {}) : {}.".format(str(increment),
                    product[1], product[2], product[4], product[5]))
            increment = increment + 1
        print()

    def display_details_of_product(self, product, name_of_product_fields, *title):
        """ displays details of a 'product' """
        self.__clear()
        if title:
            print("Produit à remplacer par un substitut :")
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
        for i in range(1, 7):
            print('  ', name_of_product_fields[i-1], ' :', substitute[i])
        print()

    def display_already_record(self, product, substitute):
        """ indicates that the selected substitute has already
        been registered for this product
        In reception : 'product' and 'subbstitute' which contain
            name and brand of those
        On return	 : nothing
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
        # displays each product with substitute(s)
        for product in products_substitutes_result:
            print("* Substitut(s) au produit", product, " :")
            # displays the substitute(s) of a product
            for substitute in products_substitutes_result[product]:
                print("-", substitute)
                print()
        print()

    def display_reinitialisation_database(self):
        """ displays the reinitialisation of the database  """
        self.__clear()
        print()
        print("reinitialisation de la base de données en cours...")
        print()

    def display_end_of_program(self):
        """ displays the end of program """
        self.__clear()
        print('Arrêt du programme demandé...')
        print()

    def __clear(self):
        """ Clear screen """
        os.system('cls||clear')


if __name__=='__main__':
    pass
