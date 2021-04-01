# coding: utf-8
from Database.init_database import Initialise_database


class Model(Initialise_database):
    """ manage all procedure of database BDD_OFF """
    Tables_list = ['Category', 'Product', 'Substitutes']

    def __init__(self):
        Initialise_database.__init__(self)

    def read_table(self, *catg_id):
        """ reads the items contains in the table """
        query = " SELECT " + ",".join(self.columns_read)	# "id, name, brand, url, nutriscore, ingredients, stores, category_id"
        query += " FROM " + self.table					    # "Product"
        if catg_id:
            query += " WHERE category_id=" + str(catg_id[0]) # "category_id='{catg_id}' "
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
    model = Model()
    model.drop_all_tables()
