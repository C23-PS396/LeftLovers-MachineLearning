
import pickle
import numpy as np
import tensorflow as tf
from collab_constants import MODEL_PATH, USER_ENCODER_PATH, ITEM_ENCODER_PATH

def predict_collab_filtering(user_id):
    model = tf.keras.models.load_model(MODEL_PATH)
    with open(USER_ENCODER_PATH, "rb") as f:
        user_encoder = pickle.load(f)
    with open(ITEM_ENCODER_PATH, "rb") as f:
        item_encoder = pickle.load(f)
    # print(user_encoder.categories_)
    # print(item_encoder.categories_)
    n_item = len(item_encoder.categories_[0])
    try:
        encoded_id = user_encoder.transform(np.array([user_id]).reshape(-1,1))
    except ValueError as e:
        return [] # new user
    res = model.predict([np.full(n_item, encoded_id), np.array([i for i in range(n_item)])])
    top_10_index = np.argsort(res, axis=0)[-10:].flatten()
    res = item_encoder.inverse_transform(top_10_index.reshape(-1,1)).tolist()
    res = [item[0] for item in res]
    return res


