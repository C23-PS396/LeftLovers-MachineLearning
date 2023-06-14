"""
A py program to create collab filtering tf file
input : all new transaction
output : collab-filtering.json
"""

import pandas as pd
import tensorflow as tf
import sys
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import json

from create_random_transaction import create_random_transaction

def train_collab_filtering():
    # ---<Input>---

    # dataframe of transaction
    df = create_random_transaction()

    # ---<Input>---


    # Data Preprocessing


    n_users = df['User_id'].nunique()
    n_items = df['Food_id'].nunique()

    user_encoder = LabelEncoder()
    item_encoder = LabelEncoder()
    user_encoder.fit(n_users)
    item_encoder.fit(n_items)


    n_users = user_encoder.transform(n_users) + 1
    n_items = user_encoder.transform(n_items) + 1


    user_ids = user_encoder.transform(df['User_id'].values)
    item_ids = user_encoder.transform(df['Food_id'].values)
    ratings = df['Rating'].values

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


    model.save('collab-filtering-model')
    with open("collab-filtering-model/user_encoder.json", "w") as f:
        json_data = json.dumps(user_encoder)
        f.write(json_data)
    with open("collab-filtering-model/item_encoder.json", "w") as f:
        json_data = json.dumps(item_encoder)
        f.write(json_data)