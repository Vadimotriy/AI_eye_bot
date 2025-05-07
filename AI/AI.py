import tensorflow
import numpy as np

from PIL import Image


class AI:
    def __init__(self):
        self.model = tensorflow.keras.models.load_model('data/nums.keras')

    def predict_nums(self, image):
        image = Image.open(image)
        image = image.convert("L")
        image = image.resize((28, 28))

        image_array = np.array(image)
        image_array = image_array.reshape((1,) + image_array.shape + (1,))  # (1, 101, 101, 1)
        image_array = image_array.astype("float32") / 255.0

        res = list(*self.model.predict(image_array))

        return res.index(max(res))
