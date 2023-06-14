#!/Users/rainataputra/6th Term/content-based_filtering/bin/python3
import psycopg2
import os
from configparser import ConfigParser
_config = ConfigParser()
_config.read(os.path.join(os.getcwd(), "database.ini"))

_host = _config.get("postgresql", "host")
_port = _config.get("postgresql", "port")
_database = _config.get("postgresql", "database")
_password = _config.get("postgresql", "password")
_user = _config.get("postgresql", "user")

# connect to db
conn = psycopg2.connect(
    host = _host,
    port = _port,
    database = _database,
    password = _password,
    user = _user
)




