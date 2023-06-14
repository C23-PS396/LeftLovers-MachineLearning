
import pickle
import numpy as np
import tensorflow as tf

folder = "../collab-filtering-model"

def predict_collab_filtering(user_id):
    model = tf.keras.models.load_model(folder)
    with open(f"{folder}/user_encoder.pkl", "rb") as f:
        user_encoder = pickle.load(f)
    with open(f"{folder}/item_encoder.pkl", "rb") as f:
        item_encoder = pickle.load(f)
    print(user_encoder.categories_)
    n_item = len(item_encoder.categories_[0])
    # print(item_encoder.transform(np.array(item_encoder.categories_).reshape(-1,1)))
    try:
        encoded_id = user_encoder.transform(np.array([user_id]).reshape(-1,1))
    except ValueError as e:
        return [] # new user
    res = model.predict([np.full(n_item, encoded_id), np.array([i for i in range(n_item)])])
    top_10_index = np.argsort(res, axis=0)[-10:].flatten()
    print(item_encoder.inverse_transform(top_10_index.reshape(-1,1)))

predict_collab_filtering("00YynWowFHP29y9P")