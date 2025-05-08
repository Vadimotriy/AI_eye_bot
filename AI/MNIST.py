import tensorflow.keras as keras

from keras.utils import to_categorical
from keras import models, layers

(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Преобразует массив пикселей в нужный формата
x_train = x_train.reshape((60000, 28, 28, 1))
x_train = x_train.astype('float32') / 255

# Переход к оттенкам серого
x_test = x_test.reshape((10000, 28, 28, 1))
x_test = x_test.astype('float32') / 255

# преобразование в категориальные признаки
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# 8-слояная модель
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, 'relu'),
    layers.Dense(10, 'softmax')
])

# Компеляция и обучение
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=100, batch_size=32)

# Итоговая точность модели
test_loss, test_acc = model.evaluate(x_test, y_test)
print(test_acc)  # +- 9904999732971191

# Сохранение
model.save('data/nums2.keras')
