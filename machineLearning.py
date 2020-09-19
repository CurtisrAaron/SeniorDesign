from pathlib import Path
from sklearn.utils import Bunch
from sklearn import svm
import numpy as np
from sklearn.model_selection import train_test_split
from skimage.io import imread
from skimage.transform import resize
from sklearn import metrics
import pickle

#823 × 1606

def load_image_files(container_path, dimension=(200, 400)):
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
            img = imread(file)
            img_resized = resize(img, dimension, anti_aliasing=True, mode='reflect')
            flat_data.append(img_resized.flatten()) 
            images.append(img_resized)
            target.append(i)
            count += 1
            if (count % 10 == 0):
                print("count = " + str(count) + " / " + str(totalCount) + " in folder " + str(folderCount) + " / " + str(totalFolders))
        folderCount += 1
    flat_data = np.array(flat_data)
    target = np.array(target)
    images = np.array(images)

    return Bunch(data=flat_data,
                 target=target,
                 target_names=categories,
                 images=images,
                 DESCR=descr)

image_dataset = load_image_files("img/")

print(image_dataset)

#Create a svm Classifier-
clf = svm.SVC(kernel='linear') # Linear Kernel

X_train, X_test, y_train, y_test = train_test_split(image_dataset.data, image_dataset.target, test_size=0.3,random_state=109)

#Train the model using the training sets
clf.fit(X_train, y_train)

print(clf)

#Predict the response for test dataset
y_pred = clf.predict(X_test)

print(X_train)

print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

with open('model.pickle', 'wb') as handle:
    pickle.dump(clf, handle, protocol=pickle.HIGHEST_PROTOCOL)
