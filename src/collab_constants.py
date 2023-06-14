import os

SRC_PATH = os.getcwd()
PARENT_DIR = os.path.dirname(SRC_PATH)

MODEL_PATH = os.path.join(PARENT_DIR, "collab-filtering-model")
PICKLE_PATH = os.path.join(PARENT_DIR, "pickle-objects")
USER_ENCODER_PATH = os.path.join(PARENT_DIR, "user_encoder.pkl")
ITEM_ENCODER_PATH = os.path.join(PARENT_DIR, "item,_encoder.pkl")

COLUMNS = ["customerId", "merchantId", "rating"]