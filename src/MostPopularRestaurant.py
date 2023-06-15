from src.db_connection import conn

_table = "\"Transaction\""
_columns = "\"merchantId\", COUNT(\"merchantId\") as count"
_group = "\"merchantId\""
_order = "count" 
_limit = 10
query = f'SELECT {_columns} FROM {_table} GROUP BY {_group} ORDER BY {_order} DESC LIMIT {_limit}'

class MostPopularRestaurant():
    def __init__(self):
        self.cursor = conn.cursor()
        self.most_popular_restaurant = []

    def update(self):
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        self.most_popular_restaurant = []
        for row in res:
            self.most_popular_restaurant.append(row[0])
        return self.most_popular_restaurant

    def get(self, update : bool = False):
        return self.most_popular_restaurant
