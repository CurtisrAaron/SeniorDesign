import PySimpleGUI as sg
import PIL.Image
import io
import base64
import mongoengine
from DbModels import *

#img = Image.open('img/good/2799468.png')
#img.show()

def convert_to_bytes(file_or_bytes, resize=None):
    '''
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    '''
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()


connect("Senior-Design-Project", host='mongodb://localhost/test')

observations = MetaData.objects()

obvIndex = 0

framewidth = 40
imgSize = (300, 600)
framelayout = [[sg.Text('Transmitter mode = {0}\n\nSatnogs Vetted Status = {1}\n\nUser Vetted Status = {2}\n\nModel Vetted Status = {3}'.format(observations[obvIndex]['transmitter_mode'], observations[obvIndex]['status'], observations[obvIndex]['user_vetted_status'], observations[obvIndex]['model_vetted_status']), key = 'metadata' , size = (framewidth,8))] , [ sg.Button('Good' , size = (framewidth,4))] , [ sg.Button('Bad' , size = (framewidth,4))] , [ sg.Button('Next' , size = (framewidth,4))] , [ sg.Button('Back' , size = (framewidth,4))]]
layout = [[sg.Text('Observation ID: {0}'.format(observations[obvIndex]['Id']), key = 'observation_id')],[sg.Image(data=convert_to_bytes(observations[obvIndex]['waterfall'], imgSize), size = imgSize, key = 'image'), sg.Frame('' , framelayout)]]
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
        if obvIndex > 1:
            obvIndex -= 1
        print ('Event is Back')
    if event == 'Next':
        if obvIndex < len(observations) - 1:
            obvIndex += 1
        print ('Event is Next')
    window['image'].update(data=convert_to_bytes(observations[obvIndex]['waterfall'], imgSize))
    window['observation_id'].update(value='Observation ID: {0}'.format(observations[obvIndex]['Id']))
    window['metadata'].update(value='Transmitter mode = {0}\n\nSatnogs Vetted Status = {1}\n\nUser Vetted Status = {2}\n\nModel Vetted Status = {3}'.format(observations[obvIndex]['transmitter_mode'], observations[obvIndex]['status'], observations[obvIndex]['user_vetted_status'], observations[obvIndex]['model_vetted_status']))

window.close()



