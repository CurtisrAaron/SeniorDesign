import PySimpleGUI as sg
import json
from imageDownload import *
#sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.


def printCount(count, totalCount):
    print(layout[0])
    window['progress text'].update('progress = ' +  str(count) + ' / ' + str(totalCount))
    window.refresh()


with open('params.json') as f:
  params = json.load(f)



layout = [  [sg.Text('Some text on Row 1', font=("Helvetica", 25), text_color='black')]]

for field in params:
    layout.append([sg.Text(field, font=("Helvetica", 25), text_color='black')])
    print(params[field])
    layout.append([sg.Listbox(values=params[field], size=(30,4), font=("Helvetica", 25), key = field)])

layout.append([sg.Text("number of results", font=("Helvetica", 25), text_color='black')])

resultsNumber = []

for x in range(1, 50 + 1):
    resultsNumber.append(x * 200)

layout.append([sg.Listbox(values=resultsNumber, size=(30,4), font=("Helvetica", 25), key='obvsNumber')])


layout.append([sg.Button('Ok', size = (4, 2), font=("Helvetica", 25)), sg.Button('Cancel', size = (10, 2), font=("Helvetica", 25))])

layout.append([sg.Text('', font = ("Helvetica", 25), key = 'progress text', size = (30,2))])

# Create the Window
window = sg.Window('Window Title', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == 'Ok':
        apiParams = {}
        for field in params:
            print(values[field])
            if len(values[field]) == 1:
                apiParams[field] = values[field][0]
        obvsNumber = 25
        if len(values['obvsNumber']) == 1:
            obvsNumber = values['obvsNumber'][0]
        downloadImages(params = apiParams, numberOfObservations = obvsNumber, updateFunction = printCount)
        sg.Popup('Alert!', 'Done!')
    


window.close()
