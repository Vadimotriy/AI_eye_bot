import tensorflow
import numpy as np
import easyocr
import requests
from googletrans import Translator


from PIL import Image, ImageDraw
from io import BytesIO

from database.constants import LANGUAGES_FOR_PHOTOES
from database.functions import open_file


class AI:  # класс, для работы с нейросетями
    def __init__(self, api, secret):  # инициализация
        self.api, self.secret = api, secret
        self.model = tensorflow.keras.models.load_model('data/nums1.keras')
        self.session = None
        self.translator = Translator()

        self.update()

    def update(self):
        self.translation, self.conf = open_file()

    def predict_nums(self, image, better):  # использование нашей модели
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

    def get_text(self, image, src: str):  # использование EasyOCR
        languages = []
        for i in src:
            languages.append(LANGUAGES_FOR_PHOTOES[i.capitalize()])

        self.reader = easyocr.Reader(languages, gpu=True)
        result = self.reader.readtext(image, paragraph=True)
        text = []

        # обводка текста
        draw = ImageDraw.Draw(image)
        for i in result:
            points, words = i
            text.append(words)
            polygon = [(int(x), int(y)) for (x, y) in points]
            draw.polygon(polygon, outline="red", width=2)
        img_byte = BytesIO()
        image.save(img_byte, format="PNG")
        img_byte.seek(0)

        return text, img_byte

    def get_tags(self, image):  # распознание объектов на фото
        response = requests.post(
            'https://api.imagga.com/v2/tags',
            auth=(self.api, self.secret),
            files={'image': image})
        data = response.json()

        text = ''
        for i in data['result']['tags']:
            conf = float(i['confidence'])
            if conf < self.conf:
                break

            if self.translation:
                rus = self.translator.translate(i['tag']['en'], src='en', dest='ru').text
                text += f"<b>{i['tag']['en']} ({rus})</b> - вероятность {round(conf, 1)}%\n".capitalize()
            else:
                text += f"<b>{i['tag']['en']}</b> - вероятность {round(conf, 1)}%\n".capitalize()

        return text
