import numpy as np
import pickle
import sys

from pathlib import Path
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.utils import Bunch
from skimage.io import imread
from skimage.transform import resize
from sklearn import metrics
from datetime import datetime
from resize import *

# machineLearning trains an SVM model using sklearn

#823 × 1606

def load_image_files(container_path, dimension=(400, 800)):
    """
    Load image files with categories as subfolder names 
    which performs like scikit-learn sample dataset
    
    Parameters
    ----------
    container_path : string or unicode
        Path to the main folder holding one subfolder per category
    dimension : tuple
        size to which image are adjusted to
        
    Returns
    -------
    Bunch
    """
    
    image_dir = Path(container_path)
    folders = [directory for directory in image_dir.iterdir() if directory.is_dir()]
    categories = [fo.name for fo in folders]

    descr = "A image classification dataset"
    images = []
    flat_data = []
    target = []
    folderCount = 1
    totalFolders = len(folders)
    for i, direc in enumerate(folders):
        totalCount = len(list(direc.glob('*')))
        count = 0
        for file in direc.iterdir():
            #img = imread(file)

            img = np.array(modifiedImage(file))

            img_resized = resize(img, dimension, anti_aliasing=True, mode='reflect')
            flat_data.append(img_resized.flatten()) 
            images.append(img_resized)
            target.append(i)
            count += 1
            if (count % 10 == 0):
                dotTotal = 100
                dotCount = int((count / totalCount) * dotTotal)
                dots = ' ['
                for j in range(dotCount):
                    dots = dots + '.'
                for j in range(dotTotal - dotCount):
                    dots = dots + ' '
                dots = dots + ']'
                sys.stdout.write("\rcount = " + str(count) + " / " + str(totalCount) + " in folder " + str(folderCount) + " / " + str(totalFolders) + dots + '\t')
                sys.stdout.flush()

        folderCount += 1
    flat_data = np.array(flat_data)
    target = np.array(target)
    images = np.array(images)

    return Bunch(data=flat_data,
                 target=target,
                 target_names=categories,
                 images=images,
                 DESCR=descr)

resolution = (160,320)

image_dataset = load_image_files("img/", resolution)

print(image_dataset)

#Create a svm Classifier-
clf = svm.SVC(kernel='linear') # Linear Kernel

X_train, X_test, y_train, y_test = train_test_split(image_dataset.data, image_dataset.target, test_size=0.1,random_state=101)

#Train the model using the training sets
clf.fit(X_train, y_train)

print(clf)

#Predict the response for test dataset
y_pred = clf.predict(X_test)

print(X_train)

print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

# lets save the model
with open(('sk-' + str(resolution[0]) + 'x' + str(resolution[1]) + '-' + datetime.now().strftime("%m-%d_%H:%M:%S") + 'model.pickle'), 'wb') as handle:
    pickle.dump(clf, handle, protocol=pickle.HIGHEST_PROTOCOL)
