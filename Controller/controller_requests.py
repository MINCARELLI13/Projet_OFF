""" Manage all the requests of MySQL and API's OpenFoodFacts """
# coding: utf-8
from Config.config import CATEGORIES, FIELDS_PRODUCTS_API, PRODUCTS_NB, URL, FIELDS_SQL_API
from Model.model_api import RequestApi
from Model.category import Category
from Model.product import Product
from Model.substitute import Substitute
from Model.model_sql import RequestSql


class Request:
    """ contains all the requests on database BDD_OFF """

    def loads_products_of_category(self, catg_id):
        """ loads all products from category_id
            In reception : the id of chosen category 
            On return    : list of tuple like...
            [(31, 'Gazpacho', 'Alvalle', ...), (32, 'Le Ravioli', 'Panzani', ...)]
        """
        return Product().read_table(catg_id)

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

    def reinitialisation_database(self):
        """ drop all tables of database
            then recreate and fill them  """
        # drop all tables of database
        RequestSql().drop_all_tables()
        # recreate all tables of database
        Category().create_table()
        Product().create_table()
        Substitute().create_table()
        # fills Category's table
        self.fill_table_category()
        # fills Product's table
        self.fill_table_product()

    # def record_selected_substitute(self):
    def fill_table_substitutes(self, product_id, substitut_id):
        """ records the substitute chosen by USER """
        # data formatting 
        values_dico = {'original_id': str(product_id), 'substitut_id': str(substitut_id)}
        # recording in database
        Substitute().update_table(values_dico)

    def fill_table_category(self):
        """ fills table Category with categories
            Snacks salés','Gâteaux','Sodas',...
        """
        categorie = Category()
        for catg in CATEGORIES:
            dico = {}
            dico[catg] = CATEGORIES[catg]
            # dico = {5: 'Plats préparés'}
            categorie.update_table(dico)

    def fill_table_product(self):
        """ 
            fills table 'Product' with items loaded from API
            {'product_name_fr': 'Gazpacho',  'brands': 'Alvalle', ...}
        """
        produit = Product()
        keys_list = ['product_name_fr', 'brands', 'url', 'nutrition_grade_fr', 'ingredients_text_fr', 'stores']
        for catg_id in CATEGORIES:
            # get the products of a category in the API
            request_api = RequestApi()
            list_of_dicos = request_api.get_products_of_category(
                    CATEGORIES[catg_id], FIELDS_PRODUCTS_API, PRODUCTS_NB, URL)
            # delete page break "\n" and limits length of "ingredients"
            list_of_dicos = request_api.clean_request_api(list_of_dicos)
            # product = {'product_name_fr': 'Gazpacho',  'brands': 'Alvalle', ...}
            for product in list_of_dicos:
                dico = {}
                # if no product is empty 
                # and each key has a value
                # and all keys are present
                # and no product with the name 'Chargement' 
                if product\
                    and self.is_dict_full(product)\
                    and self.have_all_keys(product, keys_list)\
                    and ('Chargement' not in product['product_name_fr'][0:10]):
                    try:
                        # FIELDS_SQL_API = {'name': 'product_name_fr',
                        #                   'brand': 'brands',...   }
                        for field in FIELDS_SQL_API:
                            # dico = {'name': 'Gazpacho', 'brand': 'Alvalle', ...}
                            dico[field] = product[FIELDS_SQL_API[field]]
                    except KeyError:
                        pass
                    produit.update_table(dico, catg_id)

    def is_dict_full(self, dico):
        """ checks that each key in the
            dictionary has a value
            In reception : dico = dict of results API
            On return    : True or Flase
        """
        boolean = True
        for item in dico:
            if not dico[item]:
                boolean = False
        return boolean

    def have_all_keys(self, dico, keys_list):
        """ checks that each result of the API request
            (in 'dico') has all the expected keys (=fields) 
            (= 'name', 'brand', 'url', ...)
            In reception : dico = dict of results API
                           keys_list = list of expected keys
            On return    : True or Flase
        """
        if sorted(list(dico.keys())) != sorted(keys_list):
            return False
        return True


if __name__=='__main__':
    pass
