from fastapi import FastAPI, responses
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
import numpy as np
import tensorflow as tf
import pandas as pd
import os
import asyncio
import sys
import json
import pickle
import sklearn
import datetime

# sys.path.append("src")
from src.db_connection import conn
from src.predict_collab_filtering import predict_collab_filtering
from src.collab_constants import *
# to run python3 -m uvicorn main:app --reload

app = FastAPI()

ORIGINS = ['*']
METHODS = ['*']
HEADERS = ['*']

cwd = os.getcwd()

PICKLE_PATH = os.path.join(cwd, "pickle-objects")
CSV_PATH = os.path.join(cwd, "csv-files")


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
      # model = tf.keras.models.load_model(os.path.join(cwd, "content-based-model"))
      model = ""
      scaler_user = load_pickle(os.path.join(PICKLE_PATH, "scaler_user.pkl"))
      scaler_target = load_pickle(os.path.join(PICKLE_PATH, "scaler_target.pkl"))
      item_vector = load_pickle(os.path.join(PICKLE_PATH, "item_vector.pkl"))
      restaurant_df = pd.read_csv(os.path.join(CSV_PATH, "restaurant_recommended.csv"))
      return model, scaler_user, scaler_target, item_vector, restaurant_df


model, scaler_user, scaler_target, item_vector, restaurant_df = load_assests()


def get_contbased_recoms(user_profile):
      user_arr = user_profile
      scaled_user = scaler_user.transform(user_arr)
      n_restaurant = item_vector.shape[0]
      user_vector = np.tile(scaled_user, (n_restaurant,1))

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

lock = [asyncio.Lock(), asyncio.Lock()]
# new_transaction = [open(os.path.join(NEW_TRANSACTION_PATH, NEW_TRANSACTION_FILE[0])), open(os.path.join(NEW_TRANSACTION_PATH, NEW_TRANSACTION_FILE[1]))]
index = 0
index_lock = asyncio.Lock()
@app.get("/newTransaction")
async def new_transaction(customerId, merchantId, rating):
      if not bool(customerId) or not bool(merchantId) or not bool(rating):
            return "400"
      await index_lock.acquire()
      try:
            acquired = lock[index].acquire_nowait()
      finally:
            index_lock.release()
      if acquired:
            try:
                  # call retrain_collab_filtering.py
                  pass
            finally:
                  acquired.release()
                  return "201"
                  #train complete
      

      print(f"Customer : {customerId}, Merchant : {merchantId}, Rating : {rating}")
      return "200"


@app.get("/updateUserProfile")
async def update_user_profile(user_id: str, cuisine: str):
      cuisine_arr = [x.strip().lower() for x in cuisine.split(',')]
      res_cui_arr = ['burgers','fast food','sandwich','healthy','asian','comfort food','family meals','mexican','breakfast and brunch','desserts','pizza','salads','chicken','convenience','italian','everyday essentials','wings','family friendly','latin american','snacks']
      temp = [0] * 20
      s_20 = [f"\"u{i+1}\"" for i in range(20)]
      for cui in cuisine_arr:
            if cui in res_cui_arr:
                  ind = res_cui_arr.index(cui)
                  temp[ind] += 1
      cursor = conn.cursor()
      cursor.execute(f"SELECT {','.join(s_20)} FROM \"UserProfile\" WHERE \"id\"=" + '%s', (user_id,))
      res = cursor.fetchall()[0]
      
      for i in range(len(res)):
            temp[i] += res[i]

      values = temp
      columns = ", ".join([f'"u{i+1}"=%s' for i in range(20)])
      res = cursor.execute('UPDATE "UserProfile" SET ' + columns + ' WHERE "id" = %s;', values + [user_id])
      conn.commit()
      return '200'


@app.get("/getPrediction")
async def get_prediction(user_id: str):
      cursor = conn.cursor()
      if not bool(user_id):
            return []
      s_20 = [f"\"u{i+1}\"" for i in range(20)]
      cursor.execute(f"SELECT {','.join(s_20)} FROM \"UserProfile\" WHERE \"id\"=" + '%s', (user_id,))
      user_profile = np.array([list(cursor.fetchall()[0])])
      content_restaurant_ids = get_contbased_recoms(user_profile)
      categories = restaurant_df.loc[restaurant_df.id.isin(content_restaurant_ids)].category.values
      categories = [x.strip() for sub_cat in categories for x in sub_cat.split(', ')]
      
      first_line = 'SELECT DISTINCT f."merchantId" from "Food" as f JOIN'
      second_line = [
      '(SELECT cf."B" as "food_id" from "_CategoryToFood" as cf join "Category" as c on c.id = cf."A" where c.name in ',
      f'({", ".join(["%s"] * len(categories))})) as cat on f.id = cat."food_id";'
      ]
      
      query_line = first_line + ''.join(second_line)
      cursor.execute(query_line, categories)
      res = [id[0] for id in cursor.fetchall()]

      collab_res = predict_collab_filtering(user_id)
      res += collab_res
      res = list(set(res))
      return responses.JSONResponse(content=res)


if __name__ == "__main__":
      port = int(os.environ.get('PORT', 5000))
      run(app, host="localhost", port=5023)

