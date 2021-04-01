# coding: utf-8
from ORM.model import Model


class Substitute(Model):

    def __init__(self):
        Model.__init__(self)
        self.table = "Substitutes"
        self.columns_read = ['original_id', 'substitut_id']
        self.columns_update = ['original_id', 'substitut_id']
        self.columns_create =  "original_id INT NOT NULL, \
                                substitut_id INT NOT NULL, \
                                PRIMARY KEY (original_id, substitut_id), \
                                CONSTRAINT fk_Substitutes_original_id \
                                FOREIGN KEY (original_id) \
                                REFERENCES BDD_OFF.Product (id) \
                                ON DELETE NO ACTION \
                                ON UPDATE NO ACTION, \
                                CONSTRAINT fk_Substitutes_substitut_id \
                                FOREIGN KEY (substitut_id) \
                                REFERENCES BDD_OFF.Product (id) \
                                ON DELETE NO ACTION \
                                ON UPDATE NO ACTION"