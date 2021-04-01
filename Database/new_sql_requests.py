# coding: utf-8
from Model_ORM.category import Category
from Model_ORM.product import Product
from Model_ORM.substitute import Substitute
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
        return Product().read_table(catg_id)
        # query = f" SELECT id, name, brand, url, nutriscore, ingredients, stores, category_id \
        #         FROM Product WHERE Product.category_id='{catg_id}' "
        # self.cursor.execute(query)
        # return self.cursor.fetchall()

    def load_recorded_substitutes(self):
        """ gets all substituts of database BDD_OFF
            In reception : nothing
            On return    : dictionnary for which key = product_id and values = substitutes_id
            like {1: [6], 32: [31, 38], 34: [31, 33, 38, 39]} """
        # option for request to table 'Substitutes' of database BDD_OFF
        option = "INNER JOIN Product AS Original     ON Original.id = Substitutes.original_id",\
                  "INNER JOIN Product As Substitut    ON Substitut.id = Substitutes.substitut_id"
        # SEND REQUEST to table 'Substitutes'
        my_cursor = Substitute().read_table(option)
        substitutes_recorded_dico = {}
        # puts results in dictionnary "substitutes_recorded_dico"
        for curseur in my_cursor:
            # if (Product.name, Product.brand) exists already in the dictionnary...
            if ((curseur[0],curseur[1]) in substitutes_recorded_dico):
                # ...adds other substitute
                substitutes_recorded_dico[(curseur[0],curseur[1])] = substitutes_recorded_dico[(curseur[0],curseur[1])] + [(curseur[2], curseur[3])]
            else:
                # else creates new key (= product.name, product.brand)
                substitutes_recorded_dico[(curseur[0], curseur[1])] = [(curseur[2], curseur[3])]
        return substitutes_recorded_dico


if __name__=='__main__':
    pass
