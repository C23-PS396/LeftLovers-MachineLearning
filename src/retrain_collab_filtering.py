import pandas as pd
import numpy as np
import pickle
import os
from tensorflow.keras.callbacks import EarlyStopping
from src.collab_constants import MODEL_PATH, USER_ENCODER_PATH, ITEM_ENCODER_PATH, COLUMNS
from src.load_collab_filtering import load_collab_filtering

def retrain_collab_filtering(index_csv):
    """
    """
    datas = {}
    df = df.DataFrame(datas)
    model, user_encoder, item_encoder = load_collab_filtering()


    user_ids = np.array(df[COLUMNS[0]].values)
    item_ids = np.array(df[COLUMNS[1]].values)
    ratings = np.array(df[COLUMNS[2]].values)

    user_encoder.fit(user_ids)
    item_encoder.fit(item_ids)

    user_ids = user_encoder.transform(user_ids)
    item_ids = item_encoder.transform(item_ids)
    ratings = np.array(df[COLUMNS[2]], dtype=np.int32)

    # Splitting into Training and Test sets
    train_user_ids, test_user_ids, train_item_ids, test_item_ids, train_ratings, test_ratings = train_test_split(
        user_ids, item_ids, ratings, test_size=0.2, random_state=42
    )

    """
    Will stop if there is no improvement after "patience" times
    """
    early_stopping = EarlyStopping(monitor='loss', patience=5, mode='min', verbose=1)


    # Model Training
    model.fit([train_user_ids, train_item_ids], train_ratings, epochs=100, batch_size=100, callbacks=[early_stopping], verbose=1)

    # Model Evaluation
    test_loss = model.evaluate([test_user_ids, test_item_ids], test_ratings)
    print("Test Loss:", test_loss)

    model.save(MODEL_PATH)
    with open(os.path.join(USER_ENCODER_PATH), "wb") as f:
        pickle.dump(user_encoder, f)
    with open(os.path.join(ITEM_ENCODER_PATH), "wb") as f:
        pickle.dump(item_encoder, f)
