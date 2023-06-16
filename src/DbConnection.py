#!/Users/rainataputra/6th Term/content-based_filtering/bin/python3
import psycopg2
import os
from configparser import ConfigParser

config_file = "database.ini"

class DbConnection():
    def __init__(self):
        self._config = ConfigParser()
        self._config.read(os.path.join(os.getcwd(), config_file))
        self._section = "postgresql"
        self._host = self._config.get(self._section, "host")
        self._port = self._config.get(self._section, "port")
        self._database = self._config.get(self._section, "database")
        self._password = self._config.get(self._section, "password")
        self._user = self._config.get(self._section, "user")
        self.connect()

    def connect(self):
        # connect to db
        self._conn = psycopg2.connect(
            host = self._host,
            port = self._port,
            database = self._database,
            password = self._password,
            user = self._user)

    def execute(self, query, categories=""):
        """
        execute the query
        return the result (fetchAll result)
        """
        try:
            cursor = self._conn.cursor()
            if categories == "":
                cursor.execute(query)
            else:
                cursor.execute(query, categories)
        except psycopg2.InterfaceError as e:
            self.connect()
            cursor = self._conn.cursor()
            cursor.execute(query)
        return cursor.fetchall()
    
    def commit(self):
        self._conn.commit()



