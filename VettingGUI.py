import PySimpleGUI as sg
framewidth = 25
framelayout = [[sg.Text('Text' , size = (framewidth,4))] , [ sg.Button('Good' , size = (framewidth,4))] , [ sg.Button('Bad' , size = (framewidth,4))] , [ sg.Button('Next' , size = (framewidth,4))] , [ sg.Button('Back' , size = (framewidth,4))]]
layout = [[sg.Text('Observation ID:')],[sg.Image('img/good/2806813.png' , size = (300,600)) , sg.Frame('' , framelayout)]]
window = sg.Window('Vetting GUI',layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == 'Good':
        print ('Event is Good')
    if event == 'Bad':
        print ('Event is Bad')
    if event == 'Back':
        print ('Event is Back')
    if event == 'Next':
        print ('Event is Next')

window.close()
