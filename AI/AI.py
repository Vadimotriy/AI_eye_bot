import tensorflow
import numpy as np

from PIL import Image


class AI:
    def __init__(self):
        self.model = tensorflow.keras.models.load_model('data/nums1.keras')

    def predict_nums(self, image, better):
        image = Image.open(image)
        image = image.convert("L")
        image = image.resize((28, 28))

        if better:
            pixels = image.load()
            for y in range(image.height):
                for x in range(image.width):
                    color = pixels[y, x]
                    color = 256 if color >= 128 else 0
                    pixels[y, x] = color

        image_array = np.array(image)
        image_array = image_array.reshape((1,) + image_array.shape + (1,))  # (1, 101, 101, 1)
        image_array = image_array.astype("float32") / 255.0

        res = list(*self.model.predict(image_array))
        d = {}
        for num, per in enumerate(res):
            d[num] = per

        return d

