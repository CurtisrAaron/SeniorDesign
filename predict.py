from sklearn.utils import Bunch
from sklearn import svm
from skimage.io import imread
from skimage.transform import resize
from mongoengine import *
from DbModels import *

import pickle
import glob, os, os.path
import numpy as np
import sys

#predict on individual images

def load_image_file(img_path, dimension=(300, 600)):
    descr = "A single image classification test"
    images = []
    flat_data = []
    
    img = imread(img_path)
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

filelist = glob.glob(os.path.join('.', "*.pickle"))

if len(filelist) == 0:
    print("no models found")
    exit()

count = 0
print("models to run - ")

for model in filelist:
    print(str(count) + " " + model)
    count += 1

val = -1

while val == -1:
    try:
        val = int(input("Enter number of model you would like to run: "))
        if val < 0 or val > (len(filelist) - 1):
            val = -1
            print("please enter a valid input")
            count = 0
            print("models to run - ")

            for model in filelist:
                print(str(count) + " " + model)
                count += 1
    except:
        pass

modelname = filelist[val]

print(modelname[2:4])

is_tf = modelname[2:4] == 'tf'
is_sk = modelname[2:4] == 'sk'

if not is_sk and not is_tf:
    print('no valid models')
    exit()

try:
    resString = modelname.split('-')[1].split('x')
    resolution_height = int(resString[0])
    resolution_width = int(resString[1])
    print(resolution_height)
    print(resolution_width)
except:
    print('model name not valid')
    exit()


observations = MetaData.objects.filter(Q(model_vetted_status = 'not vetted') | Q(model_vetted_status = None))
observations = MetaData.objects()

print('predicting = ' + str(len(observations)) + ' observations')

if is_sk:
    svmfile = open(modelname, 'rb')
    svm = pickle.load(svmfile)
    count = 0
    for observation in observations:
        #print(observation.waterfall)
        image = load_image_file(observation.waterfall, dimension = (resolution_width, resolution_height))
        observation.model_vetted_status = 'good' if svm.predict(image.data) else 'bad'
        observation.save()
        if count % 10 == 0:
            sys.stdout.write('\r{0} / {1}'.format(count, len(observations)))
            sys.stdout.flush()
        count += 1
