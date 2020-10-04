import tensorflow as tf
from pathlib import Path
#from PIL import Image
from tensorflow import keras
import numpy as np

model = tf.keras.models.load_model('tf-200x400-10-04-11-05-06model')

img_width = 200
img_height = 400

testimg = keras.preprocessing.image.load_img(Path('img\\good\\2856588.png'), target_size=(img_width, img_height))
testimg = keras.preprocessing.image.img_to_array(testimg)
testimg = np.expand_dims(testimg, axis=0)

print(model.predict([testimg], batch_size = 1))
