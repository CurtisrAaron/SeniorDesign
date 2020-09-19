from sklearn.utils import Bunch
from sklearn import svm
import numpy as np
from skimage.io import imread
from skimage.transform import resize
import pickle

#predict on individual images

def load_image_file(img_path, dimension=(200, 400)):
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

good_image = load_image_file("img/good/1991436.png")
bad_image = load_image_file("img/bad/1235140.png")

svmfile = open('model.pickle', 'rb')
svm = pickle.load(svmfile)

predict = svm.predict(good_image.data)
print('good ' if predict else 'bad')

predict = svm.predict(bad_image.data)
print('good ' if predict else 'bad')

