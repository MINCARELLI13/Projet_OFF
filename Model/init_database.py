# coding: utf-8
import mysql.connector
from Config.config import USER, PASSWORD, HOST, DATABASE


class Initialise_database:

    def __init__(self):
        self.cnx = mysql.connector.connect(
            user = USER,
            password = PASSWORD,
            host = HOST,
            database = DATABASE
            )
        self.cursor = self.cnx.cursor()


if __name__=='__main__':
    pass
