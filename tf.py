import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf
import pathlib

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from datetime import datetime

# tf is a tensor flow training script that trains a CNN model

startime = datetime.now()

data_dir = pathlib.Path('./img')

image_count = len(list(data_dir.glob('*/*.png')))

print(f'number of datapoints = {image_count}'')

batch_size = 32
img_height = 400
img_width = 200

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  seed=146,
  image_size=(img_height, img_width),
  batch_size=batch_size)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=146,
  image_size=(img_height, img_width),
  batch_size=batch_size)

class_names = train_ds.class_names
AUTOTUNE = tf.data.experimental.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

normalization_layer = layers.experimental.preprocessing.Rescaling(1./255)

normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
image_batch, labels_batch = next(iter(normalized_ds))
first_image = image_batch[0]

num_classes = 2

# This is the CNN Model, The general philosophy is to start with shallow layers and as pooling goes on have deeper layers.
model = Sequential([
  layers.experimental.preprocessing.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
  layers.Conv2D(32, 3, padding='same', activation='relu'),
  layers.Dropout(rate=0.3),
  layers.MaxPooling2D(),
  layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.Conv2D(128, 3, padding='same', activation='relu'),
  layers.Dropout(rate=0.3),
  layers.MaxPooling2D(),
  layers.Conv2D(256, 3, padding='same', activation='relu'),
  layers.Dropout(rate=0.5),
  layers.MaxPooling2D(),
  layers.Flatten(),
  layers.Dense(12, activation='relu'),
  layers.Dense(num_classes - 1 ,activation='sigmoid'),
])

model.compile(optimizer=tf.keras.optimizers.SGD(),
              loss=tf.keras.losses.binary_crossentropy,
              metrics=["binary_accuracy"])

model.summary()

epochs=35
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)

acc = history.history['val_binary_accuracy']
val_acc = history.history['val_accuracy']

loss=history.history['loss']
val_loss=history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

# lets save the model with its resolution noted so we can run it in the future
filename = 'tf-' + str(img_width) + 'x' + str(img_height) + '-' + datetime.now().strftime("%m-%d-%H-%M-%S") + 'model'
model.save(filename)

print('elapsed time = ' + str(datetime.now() - starttime))