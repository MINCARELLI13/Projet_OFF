""" This module is used to manage products and substitutes database """
# coding: utf-8
from Config.config import Tables_list
from Model.init_database import InitialiseDatabase


class RequestSql(InitialiseDatabase):
    """ manage all procedure of database BDD_OFF """

    def __init__(self):
        InitialiseDatabase.__init__(self)

    def read_table(self):
        """
            reads the items contains in a table
            reads each product or substitute
            one after the other
            In reception : self.columns_read, self.table,
                           self.clauses and self.catg
        """
        query = " SELECT " + ",".join(self.columns_read)
        query += " FROM " + self.table + " "
        query += self.clauses
        # to load products from a single category
        if self.table == 'Product':
            query += str(self.catg)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_table(self, values_dico):
        """
            records in the table the informations transmitted in 'values_dico'
            In reception : self.columns_update, values_dico, self.table
        """
        # tuple of the columns to fill (name, brand, ...)
        columns = ' (' + ",".join(self.columns_update) + ')'
        # values to set in columns of table
        values = ",".join(["'" + values_dico[key] + "'" for key in values_dico])
        query = " INSERT INTO " + self.table + columns + " VALUES (" + values + ")"
        self.cursor.execute(query)
        self.cnx.commit()

    def drop_all_tables(self):
        """ drop tables Category, Product and Substitutes if exist """
        # deactivates the FOREIGN_KEYs to permit to drop all tables
        query = " SET FOREIGN_KEY_CHECKS = 0 "
        self.cursor.execute(query)
        # drop all tables : Category, Product and Substitutes
        for table in Tables_list:
            query = " DROP TABLE IF EXISTS BDD_OFF." + table
            self.cursor.execute(query)

    def create_table(self):
        """
            creation of tables Category, Product and Substitutes
            In reception : self.table, self.columns_create
        """
        query = " CREATE TABLE " + self.table + "(" + \
                self.columns_create + ")" + " ENGINE = InnoDB "
        self.cursor.execute(query)


if __name__ == '__main__':
    pass
