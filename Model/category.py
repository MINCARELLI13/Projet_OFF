""" parameters of table 'Category' on database BDD_OFF """
# coding: utf-8
from Model.model_sql import RequestSql


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
