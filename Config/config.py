# coding: utf-8

""" Categories proposed to users """
CATEGORIES = {1: 'Snacks salés', 2: 'Gâteaux',3: 'Sodas',4: 'Desserts glacés',5: 'Plats préparés'}

""" number of products to load per category """
PRODUCTS_NB = 10

""" user of MySQL """
USER = 'root'

""" password of connexion to SQL """
PASSWORD = '123ab456'

""" host of connexion to SQL """
HOST = 'localhost'
 
""" database used """
DATABASE = 'BDD_OFF'

""" begin of URL of API """
URL = 'https://fr.openfoodfacts.org/cgi/search.pl'

""" fields of the products to load """
FIELDS_OF_PRODUCTS = ('url', 'product_name_fr',
                    'brands', 'nutrition_grade_fr',
                    'ingredients_text_fr', 'stores')

NAME_OF_PRODUCT_FIELDS = ('nom', 'marque', 'url', 'nutriscore', 'ingrédients', 'magasins')

NB_OF_SUBSTITUTS = 10
