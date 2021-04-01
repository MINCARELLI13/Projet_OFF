""" module Controller to link Model and View modules """
# coding: utf-8
from Config.config import CATEGORIES, FIELDS_PRODUCTS_API, PRODUCTS_NB, URL, FIELDS_SQL_API
from Database.init_database import Initialise_database
from Database.sql_requests import Request_Sql
from API.requests_api import RequestApi
from Model_ORM.category import Category
from Model_ORM.product import Product
from Model_ORM.substitute import Substitute
from Model_ORM.model import Model


class Fill(Initialise_database):

    def __init__(self):
        Initialise_database.__init__(self)

    def reinitialisation_database(self):
        """ drop all tables of database
            then recreate and fill them  """
        # drop all tables of database
        Model().drop_all_tables()
            # self.tables.drop_all_tables_database()
        # recreate all tables of database
        Category().create_table()
        Product().create_table()
        Substitute().create_table()
            # self.tables.create_all_tables_database()
        # fills Category's table
        self.fill_table_category()
        # fills Product's table
        self.fill_table_product()

    # def record_selected_substitute(self):
    def fill_table_substitutes(self, product_id, substitut_id):
        """ records the substitute chosen by USER """
        # data formatting 
        # values_dico = {'original_id': str(self.selected_product[0]), 'substitut_id': str(self.selected_substitute[0])}
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
        produit = Product()
        keys_list = ['product_name_fr', 'brands', 'url', 'nutrition_grade_fr', 'ingredients_text_fr', 'stores']
        for catg_id in CATEGORIES:
            # get the products of a category in the API
            request_api = RequestApi()
            list_of_dicos = request_api.get_products_of_category(
                    CATEGORIES[catg_id], FIELDS_PRODUCTS_API, PRODUCTS_NB, URL)
            # delete page break "\n" and limits length of "ingredients"
            list_of_dicos = self.clean_request_api(list_of_dicos)

            for product in list_of_dicos:
                dico = {}
                # if no product is empty 
                # and each key has a value
                # and all keys are present 
                if product\
                    and self.is_dict_full(product)\
                    and self.have_all_keys(product, keys_list):
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
            except KeyError:
                pass
        return infos_of_products