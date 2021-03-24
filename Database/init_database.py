# coding: utf-8
import mysql.connector
from Config.config import user, password, host, database


class Initialise_database:

    def __init__(self):
        self.cnx = mysql.connector.connect(
            user = user,
            password = password,
            host = host,
            database = database
            )
        self.cursor = self.cnx.cursor()

