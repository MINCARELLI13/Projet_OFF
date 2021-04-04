""" parameters of table 'Product' on database BDD_OFF """
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
