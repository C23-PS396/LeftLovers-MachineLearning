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
import datetime
from db_connection import cursor, conn
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
      s_20 = [f"\"u{i+1}\"" for i in range(20)]
      cursor.execute(f"SELECT {','.join(s_20)} FROM \"UserProfile\" WHERE \"id\"=" + '%s', (user_id,))
      user_profile = np.array([list(cursor.fetchall()[0])])
      content_restaurant_ids = get_contbased_recoms(user_profile)
      categories = restaurant_df.loc[restaurant_df.id.isin(content_restaurant_ids)].category.values
      clean_categories = set([x.strip() for x in ",".join([str(x) for x in list(categories)]).split(',')])

      return json.dumps({
            "category": ",".join(list(clean_categories))
      })


if __name__ == "__main__":
      port = int(os.environ.get('PORT', 5000))
      run(app, host="localhost", port=5023)

