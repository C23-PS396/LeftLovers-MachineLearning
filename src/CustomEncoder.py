import numpy as np

class CustomEncoder():
    def __init__(self):
        self.transform_dict = {}
        self.inverse_dict = {}
        self.count = 0

    def length(self):
        