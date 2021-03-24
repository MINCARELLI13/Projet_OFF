# coding: utf-8
from Database.init_database import Initialise_database


class Filling(Initialise_database):
    """ contains all the requests to fill database BDD_OFF """

    def __init__(self):
        Initialise_database.__init__(self)
    
    def fill_substitutes_table(self, original_id, substitute_id):
        """ Inserts the substitute of a product in database BDD_OFF
            In reception : product_id and her substitute_id 
            On return    : nothing
        """
        query = f"INSERT INTO Substitutes (original_id, substitut_id) \
                VALUES ('{original_id}', '{substitute_id}')"
        # print("def filling_table_Substitutes(self, original_id, substitute_id):")
        # input("")
        self.cursor.execute(query)
        self.cnx.commit()
        print()
        print("Enregistrement du substitut effectué !")
