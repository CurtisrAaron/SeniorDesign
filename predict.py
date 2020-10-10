from sklearn.utils import Bunch
from sklearn import svm
from skimage.io import imread
from skimage.transform import resize
from mongoengine import *
from DbModels import *
from resize import *
from tensorflow import keras
from pathlib import Path

import tensorflow as tf
import pickle
import glob, os, os.path
import numpy as np
import sys
import numpy

#predict on individual images

def load_image_file(img_path, dimension=(300, 600)):
    descr = "A single image classification test"
    images = []
    flat_data = []
    
    img = numpy.array(modifiedImage(img_path))
    img_resized = resize(img, dimension, anti_aliasing=True, mode='reflect')
    flat_data.append(img_resized.flatten()) 
    images.append(img_resized)

    flat_data = np.array(flat_data)
    images = np.array(images)

    return Bunch(data=flat_data,
                 images=images,
                 target_names=['bad','good'],
                 DESCR=descr)

connect("Senior-Design-Project", host='mongodb://localhost/test')

skfilelist = glob.glob(os.path.join('./skModels', "*.pickle"))
tffilelist = glob.glob(os.path.join('./tfModels', "*"))

if len(skfilelist) + len(tffilelist)  == 0:
    print("no models found")
    exit()

count = 0
print("models to run - ")

for model in skfilelist:
    print(str(count) + " " + model)
    count += 1

for model in tffilelist:
    print(str(count) + " " + model)
    count += 1

val = -1

while val == -1:
    try:
        val = int(input("Enter number of model you would like to run: "))
        if val < 0 or val > (len(skfilelist)  + len(tffilelist)- 1):
            val = -1
            print("please enter a valid input")
            count = 0
            print("models to run - ")

            for model in filelist:
                print(str(count) + " " + model)
                count += 1
    except:
        pass

sklength = len(skfilelist)

modelname = None
is_tf = False
is_sk = False

if val + 1 > sklength:
    print('is tf')
    is_tf = True
    modelname = tffilelist[val - sklength]
else:
    modelname = skfilelist[val]
    is_sk = True

print(modelname[2:4])


if not is_sk and not is_tf:
    print('no valid models')
    exit()

try:
    resString = modelname.split('-')[1].split('x')
    resolution_height = int(resString[0])
    resolution_width = int(resString[1])
    print(f'img height = {resolution_height}')
    print(f'img width = {resolution_width}')
except:
    print('model name not valid')
    exit()


observations = MetaData.objects.filter(Q(model_vetted_status = 'not vetted') | Q(model_vetted_status = None))
observations = MetaData.objects()
totalCount = len(observations)
print('predicting = ' + str(len(observations)) + ' observations')

if is_sk:
    svmfile = open(modelname, 'rb')
    svm = pickle.load(svmfile)
    count = 0
    correctCount = 0
    for observation in observations:
        #print(observation.waterfall)
        image = load_image_file(observation.waterfall, dimension = (resolution_width, resolution_height))
        observation.model_vetted_status = 'good' if svm.predict(image.data) else 'bad'
        observation.save()
        count += 1
        if observation.model_vetted_status == observation.status:
            correctCount += 1
        if count % 10 == 0:
            dotTotal = 100
            dotCount = int((count / totalCount) * dotTotal)
            dots = ' ['
            for j in range(dotCount):
                dots = dots + '.'
            for j in range(dotTotal - dotCount):
                dots = dots + ' '
            dots = dots + ']'
            sys.stdout.write('\r{0} / {1} accuracy = {2}'.format(count, len(observations), round((correctCount / count), 2)) + dots)
            sys.stdout.flush()
if is_tf:
    model = tf.keras.models.load_model(modelname)
    count = 0
    correctCount = 0
    for observation in observations:
        image = keras.preprocessing.image.load_img(Path(observation.waterfall), target_size=(resolution_height, resolution_width))
        image = keras.preprocessing.image.img_to_array(image)
        image = np.expand_dims(image, axis = 0)
        prediction = model.predict([image], batch_size = 1)
        #print('prediction = ' + str(prediction))
        observation.model_vetted_status = 'good' if (prediction > 0.5) else 'bad'
        if observation.model_vetted_status == observation.status:
            correctCount += 1
        observation.save()
        count += 1
        if count % 10 == 0:
            dotTotal = 100
            dotCount = int((count / totalCount) * dotTotal)
            dots = ' ['
            for j in range(dotCount):
                dots = dots + '.'
            for j in range(dotTotal - dotCount):
                dots = dots + ' '
            dots = dots + ']'
            sys.stdout.write('\r{0} / {1} accuracy = {2}'.format(count, len(observations), round((correctCount / count), 2)) + dots)
            sys.stdout.flush()


