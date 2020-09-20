import mongoengine
import glob, os, os.path
from DbModels import *

# Delete all images and clear the database

connect("Senior-Design-Project", host='mongodb://localhost/test')

MetaData.objects.delete()

filelist = glob.glob(os.path.join('img/good', "*.png"))
for f in filelist:
    os.remove(f)

filelist = glob.glob(os.path.join('img/bad', "*.png"))
for f in filelist:
    os.remove(f)

os.rmdir('img/good')
os.rmdir('img/bad')

os.mkdir('img/good')
os.mkdir('img/bad')

