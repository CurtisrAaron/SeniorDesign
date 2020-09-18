import requests
import shutil
import os.path
import pymongo
from mongoengine import *
import json
from dbtest1 import *
#params = {'vetted_status' : 'good'}
def downloadImages(numberOfObservations = 100, params = {}, updateFunction = None):
    url = 'https://network.satnogs.org/api/observations/'
    count = 0
    imgCount = 0
    shouldContinue = True
    shouldDownloadImages = True

    connect("Senior-Design-Project", host='mongodb://localhost/test')

    while shouldContinue and count < (numberOfObservations / 25):
        x = requests.get(url, params=params)
        print(x.status_code)


        observations = x.json()

        # add multithreading?

        for observation in observations:
            imgCount += 1
            print("count = ", imgCount)
            if updateFunction is not None:
                updateFunction(imgCount, numberOfObservations)
            if shouldDownloadImages:
                imgURL = observation['waterfall']
                status = observation['vetted_status'] == 'good'
                if imgURL:
                    imgRequest = requests.get(imgURL, stream = True)
                    path = './img/bad/'

                    if status:
                        path = './img/good/'
                    file = open(path + str(observation['id']) + '.png', "wb")
                    file.write(imgRequest.content)
                    file.close()
                    data = metaData(
                        transmitter_mode = observation["transmitter_mode"],
                        status = observation["vetted_status"],
                        Id = observation['id'],
                        waterfall = path + str(observation['id']) + '.png'
                    ).save()
            
        print('len = ' + str(len(x.json())))
        nextPageUrl = x.links['next']['url']
        print('next page = ' + nextPageUrl)
        url = nextPageUrl
        params = {}
        count += 1

        if nextPageUrl:
            shouldContinue = True
        else:
            shouldContinue = False
