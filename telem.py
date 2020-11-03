import PySimpleGUI as sg
import json
import threading
import queue

from imageDownload import *

#sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.

callback_queue = queue.Queue()

def from_dummy_thread():
    callback_queue.put(printCount)

def from_main_thread_blocking():
    callback = callback_queue.get() #blocks until an item is available
    callback()

# method for updating download progress
class CountTacker:
    downloadedCount = 0
    totalToDownloadCount = 0

countTracker = CountTacker()

def printCount():
    countTracker.downloadedCount += 1
    window['progress text'].update('progress = ' +  str(countTracker.downloadedCount) + ' / ' + str(countTracker.totalToDownloadCount))
    window.refresh()

# lets read the params
with open('params.json') as f:
  params = json.load(f)

layout = [[sg.Text('Telem Download tool', font=("Helvetica", 25), text_color='black')]]

# lets add status params
layout.append([sg.Text("Status", font=("Helvetica", 25), text_color='black')])
layout.append([sg.Listbox(values=["good", "bad", "failed", "unknown"], size=(30,4), font=("Helvetica", 25), key = 'status', select_mode=sg.SELECT_MODE_MULTIPLE)])


# lets add the other params to the GUI
for field in params:
    layout.append([sg.Text(field, font=("Helvetica", 25), text_color='black')])
    layout.append([sg.Listbox(values=params[field], size=(30,4), font=("Helvetica", 25), key = field)])

# lets see how many observations to download
layout.append([sg.Text("number of results", font=("Helvetica", 25), text_color='black')])
resultsNumber = []
for x in range(1, 50 + 1):
    resultsNumber.append(x * 200)

layout.append([sg.Listbox(values=resultsNumber, size=(30,4), font=("Helvetica", 25), key='obvsNumber')])
layout.append([sg.Button('Ok', size = (4, 2), font=("Helvetica", 25)), sg.Button('Cancel', size = (10, 2), font=("Helvetica", 25))])
layout.append([sg.Text('', font = ("Helvetica", 25), key = 'progress text', size = (30,2))])

# lets figure out how big our window should be
screenWidth, screenHeight = sg.Window.get_screen_size()
scalingFactor = 0.7
windowSize = (screenHeight*(scalingFactor / 2), screenHeight*scalingFactor)

# Create the Window
window = sg.Window('Telem Download Tool', [[sg.Column(layout, size=windowSize, scrollable=True)]])

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == 'Ok':
        # lets check which statuses to download
        apiParams = {}
        for field in params:
            print(values[field])
            if len(values[field]) == 1:
                apiParams[field] = values[field][0]
        obvsNumber = 25
        if len(values['obvsNumber']) == 1:
            obvsNumber = values['obvsNumber'][0]
        
        countTracker.totalToDownloadCount = obvsNumber

        # lets download an even amount of each status
        obvsPerStatus = obvsNumber / len(values['status'])
        threadNumber = 1
        threads = []
        for status in values['status']:
            apiParams['status'] = status
            print(f'making thread for {status}')
            print(apiParams)
            threads.append(threading.Thread(target=downloadImages, kwargs=dict(params = apiParams.copy(), numberOfObservations = obvsPerStatus, updateFunction = from_dummy_thread)))
            print(f'thread made for {status}')
        
        for thread in threads:
            print('thread started')
            thread.start()
        
        while countTracker.downloadedCount < obvsNumber:
            from_main_thread_blocking()

        for thread in threads:
            thread.join()

        print('done')

        # if the specificity of the download status doesn't matter lets just download some observations
        if len(values['status']) == 0:
            downloadImages(params = apiParams, numberOfObservations = obvsNumber, updateFunction = printCount)
        sg.Popup('Alert!', 'Done!')

window.close()
