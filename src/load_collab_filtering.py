import pickle
from tensorflow.keras.models import load_model
from src.collab_constants import MODEL_PATH, USER_ENCODER_PATH, ITEM_ENCODER_PATH

def load_collab_filtering():
    model = load_model(MODEL_PATH)
    with open(USER_ENCODER_PATH, "rb") as f:
        user_encoder = pickle.load(f)
    with open(ITEM_ENCODER_PATH, "rb") as f:
        item_encoder = pickle.load(f)
    return (model, user_encoder, item_encoder)