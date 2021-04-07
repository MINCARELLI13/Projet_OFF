""" parameters of tables 'Product', 'Category' and 'Substitutes' on database BDD_OFF """
# coding: utf-8
from Model.model_sql import RequestSql


class Product(RequestSql):
    """ defines parameters of table 'Product' """

    def __init__(self):
        RequestSql.__init__(self)
        self.table = "Product"
        self.columns_read = ['id', 'name', 'brand', 'url', 'nutriscore',
                             'ingredients', 'stores', 'category_id']
        self.columns_update = ['name', 'brand', 'url', 'nutriscore',
                               'ingredients', 'stores', 'category_id']
        self.columns_create = "id INT NOT NULL AUTO_INCREMENT,\
                                name VARCHAR(100) NOT NULL,\
                                brand VARCHAR(100) NOT NULL,\
                                url VARCHAR(200) NOT NULL,\
                                nutriscore CHAR(1) NOT NULL,\
                                ingredients VARCHAR(500) NULL DEFAULT NULL,\
                                stores VARCHAR(150) NULL DEFAULT NULL,\
                                category_id INT NOT NULL,\
                                PRIMARY KEY (id),\
                                INDEX fk_Product_category_id (category_id ASC) VISIBLE,\
                                CONSTRAINT fk_Product_category_id\
                                FOREIGN KEY (category_id)\
                                REFERENCES BDD_OFF.Category (id)\
                                ON DELETE NO ACTION\
                                ON UPDATE NO ACTION"
        self.clauses = "WHERE category_id="
        self.catg = ""


class Category(RequestSql):
    """ defines parameters of table 'Category' """

    def __init__(self):
        RequestSql.__init__(self)
        self.table = "Category"
        self.columns_read = ['id', 'name']
        self.columns_update = ['name']
        self.columns_create = "id INT AUTO_INCREMENT,\
                              name VARCHAR(100) NOT NULL UNIQUE,\
                              PRIMARY KEY (id)"
        self.clauses = ""


class Substitute(RequestSql):
    """ defines parameters of table 'Substitutes' """

    def __init__(self):
        RequestSql.__init__(self)
        self.table = "Substitutes"
        self.columns_read = ['Original.name', 'Original.brand',
                             'Substitut.name', 'Substitut.brand']
        self.columns_update = ['original_id', 'substitut_id']
        self.columns_create = "original_id INT NOT NULL,\
                                substitut_id INT NOT NULL,\
                                PRIMARY KEY (original_id, substitut_id),\
                                CONSTRAINT fk_Substitutes_original_id\
                                FOREIGN KEY (original_id)\
                                REFERENCES BDD_OFF.Product (id)\
                                ON DELETE NO ACTION\
                                ON UPDATE NO ACTION,\
                                CONSTRAINT fk_Substitutes_substitut_id\
                                FOREIGN KEY (substitut_id)\
                                REFERENCES BDD_OFF.Product (id)\
                                ON DELETE NO ACTION\
                                ON UPDATE NO ACTION"
        self.clauses = "INNER JOIN Product AS Original \
                        ON Original.id = Substitutes.original_id \
                        INNER JOIN Product As Substitut \
                        ON Substitut.id = Substitutes.substitut_id"
