"""
A py program to create collab filtering tf file
input : all new transaction
output : collab-filtering.json
"""
import numpy as np
import pandas as pd
import tensorflow as tf
import sys
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
import pickle

from src.get_all_rating import get_all_rating
from src.collab_constants import MODEL_PATH, USER_ENCODER_PATH, ITEM_ENCODER_PATH, COLUMNS
from src.CustomEncoder import CustomEncoder

def train_collab_filtering():
    # ---<Input>---

    # dataframe of transaction
    df = get_all_rating(get_from_db=True, do_generate_random=False)

    # ---<Input>---


    # Data Preprocessing


    n_users = df[COLUMNS[0]].nunique() + 1
    n_items = df[COLUMNS[1]].nunique() + 1


    user_ids = np.array(df[COLUMNS[0]].values)
    item_ids = np.array(df[COLUMNS[1]].values)
    ratings = np.array(df[COLUMNS[2]].values)

    user_encoder = CustomEncoder()
    item_encoder = CustomEncoder()
    user_encoder.fit(user_ids)
    item_encoder.fit(item_ids)

    user_ids = user_encoder.transform(user_ids)
    item_ids = item_encoder.transform(item_ids)

    # user_ids = np.array(user_ids, dtype=np.int32)
    # item_ids = np.array(item_ids, dtype=np.int32)
    ratings = np.array(df[COLUMNS[2]], dtype=np.int32)




    # Splitting into Training and Test sets
    train_user_ids, test_user_ids, train_item_ids, test_item_ids, train_ratings, test_ratings = train_test_split(
        user_ids, item_ids, ratings, test_size=0.2, random_state=42
    )


    # ---<Model Architecture Start>---
    # Define the model architecture
    latent_dim = 5
    regularization = 0.01

    user_input = tf.keras.layers.Input(shape=(1,))
    item_input = tf.keras.layers.Input(shape=(1,))

    user_embedding = tf.keras.layers.Embedding(n_users, latent_dim, input_length=1,
                                            embeddings_regularizer=tf.keras.regularizers.l2(regularization))(user_input)
    item_embedding = tf.keras.layers.Embedding(n_items, latent_dim, input_length=1,
                                            embeddings_regularizer=tf.keras.regularizers.l2(regularization))(item_input)

    user_vec = tf.keras.layers.Flatten()(user_embedding)
    item_vec = tf.keras.layers.Flatten()(item_embedding)

    concatenated_vec = tf.keras.layers.Concatenate()([user_vec, item_vec])

    hidden_layer = tf.keras.layers.Dense(256, activation='relu')(concatenated_vec)
    hidden_layer = tf.keras.layers.Dense(128, activation='relu')(hidden_layer)
    hidden_layer = tf.keras.layers.Dense(64, activation='relu')(hidden_layer)
    hidden_layer = tf.keras.layers.Dense(32, activation='relu')(hidden_layer)
    hidden_layer = tf.keras.layers.Dropout(0.2)(hidden_layer)
    hidden_layer = tf.keras.layers.Dense(8, activation="relu")(hidden_layer)
    output = tf.keras.layers.Dense(1)(concatenated_vec)

    model = tf.keras.Model(inputs=[user_input, item_input], outputs=output)
    model.compile(optimizer='adam', loss='mean_squared_error')

    # ---<Model Architecture End>---

    """
    Will stop if there is no improvement after "patience" times
    """
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=5, mode='min', verbose=1)


    # Model Training
    model.fit([train_user_ids, train_item_ids], train_ratings, epochs=100, batch_size=100, callbacks=[early_stopping], verbose=1)

    # Model Evaluation
    test_loss = model.evaluate([test_user_ids, test_item_ids], test_ratings)
    print("Test Loss:", test_loss)
    temp = model.predict([np.array([0]), np.array([0])])
    model.save(MODEL_PATH)
    with open(os.path.join(USER_ENCODER_PATH), "wb") as f:
        pickle.dump(user_encoder, f)
    with open(os.path.join(ITEM_ENCODER_PATH), "wb") as f:
        pickle.dump(item_encoder, f)

train_collab_filtering()