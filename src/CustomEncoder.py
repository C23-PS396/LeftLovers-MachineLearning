import numpy as np

class CustomEncoder():
    def __init__(self):
        self._transform_dict = {}
        self._inverse_dict = {}
        self._count = 0

    def length(self):
        return self._count

    def key_exist(self, key):
        if self._transform_dict.get(key) != None:
            return True
        return False

    def fit(self, unique_arr):
        """
        unique_arr : np.array.unique
        it's okay if not unique, but may take longer time
        """
        for new_key in unique_arr:
            if new_key not in self._transform_dict:
                self._transform_dict[new_key] = self._count
                self._inverse_dict[self._count] = new_key
                self._count += 1

    def transform(self, input_arr):
        return np.vectorize(self._transform_dict.get)(input_arr)
        
    def inverse_transform(self, input_arr):
        return np.vectorize(self._inverse_dict.get)(input_arr)

