import os

# SRC_PATH = os.getcwd()
# PARENT_DIR = os.path.dirname(SRC_PATH)
PARENT_DIR = os.getcwd()

MODEL_PATH = os.path.join(PARENT_DIR, "collab-filtering-model")
PICKLE_PATH = os.path.join(PARENT_DIR, "pickle-objects")
USER_ENCODER_PATH = os.path.join(PICKLE_PATH, "user_encoder.pkl")
ITEM_ENCODER_PATH = os.path.join(PICKLE_PATH, "item,_encoder.pkl")

COLUMNS = ["customerId", "merchantId", "rating"]

NEW_TRANSACTION_PATH = os.path.join(PARENT_DIR, "csv-files")
NEW_TRANSACTION_FILE = ["new_transaction1.csv", "new_transaction2.csv"]


