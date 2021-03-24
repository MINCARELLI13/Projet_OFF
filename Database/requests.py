# coding: utf-8
from Database.init_database import Initialise_database


class Request(Initialise_database):
    """ contains all the requests 'SELECT' to practice on database BDD_OFF """

    def __init__(self):
        Initialise_database.__init__(self)

    def loads_products_of_category(self, catg_id):
        """ loads all products from category_id """
        query = f" SELECT id, name, brand, url, nutriscore, ingredients, stores, category_id \
                FROM Product WHERE Product.category_id='{catg_id}' "
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    # def loads_substitutes_of_product(self, catg_id):
    #     """ loads all substitutes from category_id of a product """
    #     return self.loads_products_of_category(catg_id)
    
    def load_recorded_substitutes(self):
        """ loads all substituts of database BDD_OFF
            In reception : nothing
            On return    : dictionnary for which key = product_id and values = substitutes_id
            like {1: [6], 32: [31, 38], 34: [31, 33, 38, 39]} """
        query = f"SELECT original_id, substitut_id FROM Substitutes"
        self.cursor.execute(query)
        # set results in dictionnary "substitutes_recorded_dico"
        substitutes_recorded_dico = {}
        # groups all substitutes by product in the dictionnary 'substitutes_recorded_dico'
        for curseur in self.cursor:
            if (curseur[0] in substitutes_recorded_dico):
                # print('clé déjà existante :', substitutes_recorded_dico[curseur[0]], [curseur[1]])
                substitutes_recorded_dico[curseur[0]] = substitutes_recorded_dico[curseur[0]] + [curseur[1]]
            else:
                # print('clé inexistante :', curseur[1])
                substitutes_recorded_dico[curseur[0]] = [curseur[1]]
        # print('Sorted :', substitutes_recorded_dico)
        return substitutes_recorded_dico




