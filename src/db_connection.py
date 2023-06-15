#!/Users/rainataputra/6th Term/content-based_filtering/bin/python3
import psycopg2
import os
from configparser import ConfigParser
_config = ConfigParser()
_config.read(os.path.join(os.getcwd(), "database.ini"))
_section = "postgresql"
_host = _config.get(_section, "host")
_port = _config.get(_section, "port")
_database = _config.get(_section, "database")
_password = _config.get(_section, "password")
_user = _config.get(_section, "user")

# connect to db
conn = psycopg2.connect(
    host = _host,
    port = _port,
    database = _database,
    password = _password,
    user = _user
)




