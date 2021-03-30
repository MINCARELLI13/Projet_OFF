""" This module is used to fill the tables of database """
# coding: utf-8
from Database.init_database import Initialise_database


class Filling(Initialise_database):
    """ contains all the requests to fill tables of BDD_OFF """

    def __init__(self):
        Initialise_database.__init__(self)

    def fill_substitute_table(self, original_id, substitute_id):
        """ Inserts the substitute of a product in database BDD_OFF
            In reception : product_id and her substitute_id
            On return    : nothing
        """
        query = f"INSERT INTO Substitutes (original_id, substitut_id) \
                VALUES ('{original_id}', '{substitute_id}')"
        self.cursor.execute(query)
        self.cnx.commit()

    def fill_table_category(self, categories):
        """ Insertion of the types of categories in database BDD_OFF
        (Snacks salés, Gâteaux, Sodas...) """
        # for each category of products
        for catg in categories:
            query = f"INSERT INTO Category (name) VALUES ('{categories[catg]}')"
            self.cursor.execute(query)
            self.cnx.commit()

    def fill_table_product(self, catg_id, infos_of_products):
        """ For each category of products,
            fill in the 'Product' table of BDD_OFF using
            the list of 'infos_of_products' dictionaries
            (each 'info' is a dictionary of the details of a product)
            like {'product_name_fr': 'Gazpacho', 'brands': 'Alvalle'...}
        """
        # selects only usables informations
        for info in infos_of_products:
            try:
                # verifies if no field of product is empty
                if info['url'] \
                and info['product_name_fr'] \
                and info['brands'] \
                and info['nutrition_grade_fr'] \
                and info['ingredients_text_fr'] \
                and info['stores'] \
                and ('Chargement' not in info['product_name_fr'][0:10]):
                    query = f"INSERT INTO Product (\
                        name, brand, url, nutriscore,\
                        ingredients, stores, category_id)\
                        VALUES ('{info['product_name_fr']}', \
                                '{info['brands']}', '{info['url']}', \
                                '{info['nutrition_grade_fr']}', \
                                '{info['ingredients_text_fr']}', \
                                '{info['stores']}', '{catg_id}')"
                    self.cursor.execute(query)
                    self.cnx.commit()
            except KeyError:
                pass


if __name__=='__main__':
    pass
