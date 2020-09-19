import requests
import shutil
import os.path
import pymongo
from mongoengine import *
import json
from DbModels import *
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
        badCount = 0

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
                    else:
                        badCount += 1
                        print("number of bad = " + str(badCount))
                    file = open(path + str(observation['id']) + '.png', "wb")
                    file.write(imgRequest.content)
                    file.close()
                    data = MetaData(
                        transmitter_mode = observation["transmitter_mode"],
                        status = observation["vetted_status"],
                        Id = observation['id'],
                        waterfall = path + str(observation['id']) + '.png'
                    ).save()
            
        print('len = ' + str(len(x.json())))
        if 'next' in x.links:
            nextPageUrl = x.links['next']['url']
            print('next page = ' + nextPageUrl)
            url = nextPageUrl
            params = {}
            count += 1
            shouldContinue = True
        else:
            shouldContinue = False
