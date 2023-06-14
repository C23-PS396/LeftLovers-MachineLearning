import pandas as pd
import numpy as np
import pickle
from collab_constants import MODEL_PATH, USER_ENCODER_PATH, ITEM_ENCODER_PATH, COLUMNS

def retrain_collab_filtering(datas):
    """
    datas : {
        COLUMNS[0] : [] customerId
        COLUMNS[1] : [] merchantId
        COLUMNS[2] : [] rating
    }
    """
    df = df.DataFrame(datas)

    n_users = df[COLUMNS[0]].nunique() + 1
    n_items = df[COLUMNS[1]].nunique() + 1

    user_ids = np.array(df[COLUMNS[0]].values)
    item_ids = np.array(df[COLUMNS[1]].values)
    ratings = np.array(df[COLUMNS[2]].values)

    user_ids_reshaped = user_ids.reshape(-1,1)
    item_ids_reshaped = item_ids.reshape(-1,1)

    


    return None