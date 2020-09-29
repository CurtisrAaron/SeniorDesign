from sklearn.utils import Bunch
from sklearn import svm
import numpy as np
from skimage.io import imread
from skimage.transform import resize
import pickle
from mongoengine import *
from DbModels import *

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


observations = MetaData.objects.filter(Q(model_vetted_status = 'not vetted') | Q(model_vetted_status = None))

observations = MetaData.objects()

print('len = ' + str(len(observations)))

svmfile = open('model.pickle', 'rb')
svm = pickle.load(svmfile)
count = 0
for observation in observations:
    #print(observation.waterfall)
    image = load_image_file(observation.waterfall, dimension = (200, 400))
    observation.model_vetted_status = 'good' if svm.predict(image.data) else 'bad'
    observation.save()
    if count % 10 == 0:
        print('{0} / {1}'.format(count, len(observations)))
    count += 1
