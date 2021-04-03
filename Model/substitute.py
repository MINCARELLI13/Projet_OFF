""" parameters of table 'Substitutes' on database BDD_OFF """
# coding: utf-8
from Model.model_sql import RequestSql


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
        self.inner_join = "INNER JOIN Product AS Original \
                          ON Original.id = Substitutes.original_id \
                          INNER JOIN Product As Substitut \
                          ON Substitut.id = Substitutes.substitut_id"
