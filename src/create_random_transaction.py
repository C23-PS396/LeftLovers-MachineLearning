import pandas as pd
import numpy as np
import random

def create_random_transaction():
    c_data = 250
    c_transaction = int(5e5)
    c_user = int(1e4)
    print(f"Expected Sparse : {c_transaction / (c_user * c_data) * 100} %")

    # Read the CSV file using pandas
    data_frame = pd.read_csv('./../data/restaurant-menus.csv')

    # Convert the data frame to a NumPy array
    numpy_array = data_frame.to_numpy()

    original_tags = np.unique(numpy_array[:, 1])
    count_tags = len(original_tags)
    indexes_to_remove = []
    for i in range(count_tags):
        if original_tags[i][0].upper() not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            indexes_to_remove.append(i)
    tags = np.delete(original_tags, indexes_to_remove)

    used_tags = np.sort(np.random.choice(tags, size=c_data, replace=False))
    for tag in used_tags:
        if tag[-1] == "\n":
            tag = tag[:-1]

    i = 0
    ten_percent = c_data // 10
    transaction = np.empty((c_transaction, 3), dtype=int)
    while i < c_transaction:
        user = random.randint(1, c_user)
        food = random.randint(user//ten_percent, user//ten_percent + ten_percent)
        if random.random() <= 0.2:
            food = random.randint(1, c_data) #Change food
            rating = random.randint(4,5)
        else:
            rating = random.randint(1,5-c_user//(c_user // 3))
        transaction[i][0] = user
        transaction[i][1] = food
        transaction[i][2] = rating
        i += 1

    #Randomly generated transaction
    df = pd.DataFrame(transaction)
    df.columns = ["User_id", "Food_id", "Rating"]
    return df
