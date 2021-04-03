# coding: utf-8
from Model_ORM.model import Model


class Category(Model):

    def __init__(self):
        Model.__init__(self)
        self.table = "Category"
        self.columns_read = ['id', 'name']
        self.columns_update = ['name']
        self.columns_create =  "id INT AUTO_INCREMENT,\
                                name VARCHAR(100) NOT NULL UNIQUE,\
                                PRIMARY KEY (id)"
