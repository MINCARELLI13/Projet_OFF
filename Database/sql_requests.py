# coding: utf-8
from Database.init_database import Initialise_database


class Request_Sql(Initialise_database):
    """ contains all the requests 'SELECT' to practice on database BDD_OFF """

    def __init__(self):
        """ to use self.cnx and self.cursor for requests on MySQL """
        Initialise_database.__init__(self)

    def loads_products_of_category(self, catg_id):
        """ loads all products from category_id
            In reception : the id of chosen category
            On return    : list of tuple like...
            [(31, 'Gazpacho', 'Alvalle', ...), (32, 'Le Ravioli', 'Panzani', ...)]
        """
        query = f" SELECT id, name, brand, url, nutriscore, ingredients, stores, category_id \
                FROM Product WHERE Product.category_id='{catg_id}' "
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def load_recorded_substitutes(self):
        """ gets all substituts of database BDD_OFF
            In reception : nothing
            On return    : dictionnary for which key = product_id and values = substitutes_id
            like {1: [6], 32: [31, 38], 34: [31, 33, 38, 39]} """
        query = f"SELECT original_id, substitut_id FROM Substitutes"
        self.cursor.execute(query)
        # sets results in dictionnary "substitutes_recorded_dico"
        substitutes_recorded_dico = {}
        # groups all substitutes by product in the dictionnary 'substitutes_recorded_dico'
        for curseur in self.cursor:
            # if product_id is already in the dictionnary...
            if (curseur[0] in substitutes_recorded_dico):
                # ...adds other substitute
                substitutes_recorded_dico[curseur[0]] = substitutes_recorded_dico[curseur[0]] + [curseur[1]]
            else:
                # else creates new key (= product_id)
                substitutes_recorded_dico[curseur[0]] = [curseur[1]]
        return substitutes_recorded_dico

    def get_name_of_product_id(self, product_id):
        """ gets name and brand of product with her product_id
            In reception : receives the 'id' of one product
            On return    : return a tuple (name, brand) of this product
                            like ('Gazpacho', 'Alvalle')
        """
        query = f"SELECT name, brand FROM Product WHERE id = '{product_id}'"
        self.cursor.execute(query)
        product = self.cursor.fetchone()
        return product[0] + " (" + product[1] + ")"


if __name__=='__main__':
    pass
