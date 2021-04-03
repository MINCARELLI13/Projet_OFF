# coding: utf-8
from Model.init_database import Initialise_database


class RequestSql(Initialise_database):
# class Model(Initialise_database):
    """ manage all procedure of database BDD_OFF """
    Tables_list = ['Category', 'Product', 'Substitutes']

    def __init__(self):
        Initialise_database.__init__(self)

    def read_table(self, *option):
        """ reads the items contains in the table """
        if isinstance(option[0], tuple):
            query = " SELECT " + ",".join(self.columns_recorded)
        else:
            query = " SELECT " + ",".join(self.columns_read)
        query += " FROM " + self.table + " "
        if option:
            if isinstance(option[0], int):
                query += " WHERE category_id=" + str(option[0])
            elif isinstance(option[0], tuple):
                query += option[0][0] + " " + option[0][1]
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_table(self, values_dico, *category_id):
        """ records in the table the information transmitted in 'values_dico' """
        # tuple of the columns to fill (name, brand, ...)
        columns = ' (' + ",".join(self.columns_update) + ')'
        # values to set in columns of table
        values = ",".join(["'" + values_dico[key] + "'" for key in values_dico])
        if category_id:
            values +=  ',' + str(category_id[0])
        query = " INSERT INTO " + self.table +  columns + " VALUES (" + values + ")"
        self.cursor.execute(query)
        self.cnx.commit()

    def drop_all_tables(self):
        """ drop tables Category, Product and Substitutes if exist """
        # deactivates the FOREIGN_KEYs to permit to drop all tables
        query = " SET FOREIGN_KEY_CHECKS = 0 "
        self.cursor.execute(query)
        # drop all tables : Category, Product and Substitutes
        for table in self.Tables_list:
            query = " DROP TABLE IF EXISTS BDD_OFF." + table
            self.cursor.execute(query)

    def create_table(self):
        """ creation of tables Category, Product and Substitutes """
        query = " CREATE TABLE " + self.table + "(" + \
                 self.columns_create + ")" + " ENGINE = InnoDB "
        self.cursor.execute(query)


if __name__ == '__main__':
    pass
