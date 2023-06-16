import os
import pandas as pd
import random
import string

from src.db_connection import conn
from src.collab_constants import COLUMNS

characters = string.ascii_letters + string.digits
columns = COLUMNS

def generate_random(n_user=1000, n_merchant=100, n_transaction=10000):
    length = 16
    users = []
    for _ in range(n_user):
        users.append(''.join(random.choice(characters) for _ in range(length)))
    merchants = []
    for _ in range(n_merchant):
        merchants.append(''.join(random.choice(characters) for _ in range(length)))
    transactions = []
    for _ in range(n_transaction):
        transactions.append([random.choice(users), random.choice(merchants), random.randint(1,5)])
    df_temp = pd.DataFrame(transactions)
    df_temp.columns = columns
    return df_temp


def get_all_rating(get_from_db : bool = True, do_generate_random : bool = False):
    df = pd.DataFrame(columns=columns)
    if get_from_db:
        query = ' SELECT "customerId", "merchantId", "rating" FROM "Review" WHERE "rating" > -1 '
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        df_temp = pd.DataFrame(result)
        df_temp.columns = columns
        df = pd.concat([df, df_temp], ignore_index=True)
    if do_generate_random:
        df_temp = generate_random(n_user = 1000, n_merchant = 100, n_transaction=10000)
        
        df = pd.concat([df, df_temp], ignore_index=True)
    return df

