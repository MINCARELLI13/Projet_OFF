# coding: utf-8
from Database.init_database import Initialise_database
from API.api_requests import Request_Api


class Filling(Initialise_database):
    """ contains all the requests to fill database BDD_OFF """

    def __init__(self):
        Initialise_database.__init__(self)
        self.request_api = Request_Api()
    
    def fill_substitute_table(self, original_id, substitute_id):
        """ Inserts the substitute of a product in database BDD_OFF
            In reception : product_id and her substitute_id 
            On return    : nothing
        """
        query = f"INSERT INTO Substitutes (original_id, substitut_id) \
                VALUES ('{original_id}', '{substitute_id}')"
        # print("def filling_table_Substitutes(self, original_id, substitute_id):")
        # input("")
        self.cursor.execute(query)
        self.cnx.commit()
    
    def fill_table_Category(self, categories):
        """ Insertion of the types of categories in database BDD_OFF
        (Snacks salés, Gâteaux, Sodas...) """
        for catg in categories:
            query = f"INSERT INTO Category (name) VALUES ('{categories[catg]}')"
            self.cursor.execute(query)
            self.cnx.commit()

    def fill_table_Product(self, catg_id, infos_of_products):
        """ For each category of products
        makes a request to OpenFoodFacts API
        and fills the 'Product' table of BDD_OFF """
        # selects only usables informations
        for info in infos_of_products:
            try:
                # if each field of product is not empty
                if info['url'] \
                and info['product_name_fr'] \
                and info['brands'] \
                and info['nutrition_grade_fr'] \
                and info['ingredients_text_fr'] \
                and info['stores'] \
                and ('Chargement' not in info['product_name_fr'][0:10]):
                    # insertion of products of category in "BDD_OFF.Product"
                    query = f"INSERT INTO Product ( \
                            name, brand,url, nutriscore, \
                            ingredients, stores, category_id) \
                            VALUES ('{info['product_name_fr']}', \
                                '{info['brands']}', '{info['url']}', \
                                '{info['nutrition_grade_fr']}', \
                                '{info['ingredients_text_fr']}', \
                                '{info['stores']}', '{catg_id}')"
                    self.cursor.execute(query)
                    self.cnx.commit()

                    # URL_nb = str(info['url'])
                    # Nom = str(info['product_name_fr'])
                    # Marque = str(info['brands'])
                    # Nutriscore = str(info['nutrition_grade_fr'])
                    # Ingredients = str(info['ingredients_text_fr'])
                    # Magasins = str(info['stores'])
                    # # insertion of products of category in "BDD_OFF.Product"
                    # query = f"INSERT INTO Product ( \
                    #         name, brand,url, nutriscore, \
                    #         ingredients, stores, category_id) \
                    #         VALUES ('{Nom}', '{Marque}', \
                    #         '{URL_nb}', '{Nutriscore}', \
                    #         '{Ingredients}',' {Magasins}', '{catg_id}')"
                    # self.cursor.execute(query)
                    # self.cnx.commit()


            except KeyError as msg:
                pass
                # !!!  à supprimer avant la présentation  !!!
                print("     Il manque la clé", msg)


if __name__=='__main__':
    fill = Filling()
    fill.filling_table_Product()

