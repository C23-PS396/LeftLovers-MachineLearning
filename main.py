from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
import numpy as np
import tensorflow as tf
import pandas as pd
import os
import json
import pickle
import sklearn
# to run python3 -m uvicorn main:app --reload

app = FastAPI()

ORIGINS = ['*']
METHODS = ['*']
HEADERS = ['*']


PICKLE_PATH = './pickle-objects/'
CSV_PATH = './csv-files/'


app.add_middleware(
      CORSMiddleware,
      allow_origins = ORIGINS,
      allow_credentials = True,
      allow_methods = METHODS,
      allow_headers = HEADERS 
)


def load_pickle(path):
      with open(path, 'rb') as f:
            return pickle.load(f)
            

def load_assests():
      model = tf.keras.models.load_model('./content-based-model')
      scaler_user = load_pickle(PICKLE_PATH + 'scaler_user.pkl')
      scaler_target = load_pickle(PICKLE_PATH + 'scaler_target.pkl')
      item_vector = load_pickle(PICKLE_PATH + 'item_vector.pkl')
      restaurant_df = pd.read_csv(CSV_PATH + 'restaurant_recommended.csv')
      return model, scaler_user, scaler_target, item_vector, restaurant_df


model, scaler_user, scaler_target, item_vector, restaurant_df = load_assests()


def get_contbased_recoms(user_profile):
      user_arr = np.array([[float(x) for x in user_profile.split(',')]])
      scaled_user = scaler_user.transform(user_arr)
      n_restaurant = item_vector.shape[0]
      user_vector = np.tile(user_arr, (n_restaurant,1))

      # predictions
      yp = model.predict([user_vector, item_vector])
      unscale_yp = scaler_target.inverse_transform(yp)

      # get the index
      sorted_index = np.argsort(-unscale_yp,axis=0).reshape(-1).tolist()
      restaurant_ids = restaurant_df.iloc[sorted_index[:10]].id.values
      return restaurant_ids


@app.get("/")
async def root():
      return {"message" : "Selamat Datang!"}


@app.get("/getPrediction")
async def get_prediction(user_profile: str, restaurant_id: int = None):
      n = 10
      content_restaurant_ids = get_contbased_recoms(user_profile)
      result = content_restaurant_ids
      return json.dumps({
            "restaurant_id": ",".join([str(x) for x in list(result)])
      })


if __name__ == "__main__":
      port = int(os.environ.get('PORT', 5000))
      run(app, host="localhost", port=5023)

