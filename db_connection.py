#!/Users/rainataputra/6th Term/content-based_filtering/bin/python3
import psycopg2

# connect to db
_conn = psycopg2.connect(
    host = "34.101.83.17",
    port = "5432",
    database = "capstone-db",
    password = "^tm6apIk)Z3p%K.[",
    user = "postgres"
)

# open cursor
cursor = _conn.cursor()



