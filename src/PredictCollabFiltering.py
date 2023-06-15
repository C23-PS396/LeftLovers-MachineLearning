
import pickle
import numpy as np
import tensorflow as tf
from src.load_collab_filtering import load_collab_filtering
from src.MostPopularRestaurant import MostPopularRestaurant

model, user_encoder, item_encoder = load_collab_filtering()

class PredictCollabFiltering():
    def __init__(self):
        self.mostPopularRestaurant = MostPopularRestaurant()
        self.update()

    def update(self):
        self.mostPopularRestaurant.update()
        self.model, self.user_encoder, self.item_encoder = load_collab_filtering()

    def predict(self, user_id):
        n_item = self.item_encoder.length()
        #new_user
        if not self.user_encoder.key_exist(user_id):
            return self.mostPopularRestaurant.get()
        encoded_id = self.user_encoder.transform(np.array(user_id))
        encoded_id = np.full(n_item, encoded_id)
        res = self.model.predict([np.full(n_item, encoded_id), np.array([i for i in range(n_item)])])
        top_10_index = np.argsort(res, axis=0)[-10:]
        res = self.item_encoder.inverse_transform(top_10_index).tolist()
        res = [item[0] for item in res]
        return res
