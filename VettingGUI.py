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
obvCount = len(observations)
obvIndex = 0

framewidth = 40
imgSize = (300, 600)
framelayout = [[sg.Text('Transmitter mode = {0}\n\nSatnogs Vetted Status = {1}\n\nUser Vetted Status = {2}\n\nModel Vetted Status = {3}'.format(observations[obvIndex]['transmitter_mode'], observations[obvIndex]['status'], observations[obvIndex]['user_vetted_status'], observations[obvIndex]['model_vetted_status']), key = 'metadata' , size = (framewidth,8))] , [ sg.Button('Good' , size = (framewidth,4))] , [ sg.Button('Bad' , size = (framewidth,4))] , [ sg.Button('Next' , size = (framewidth,4))] , [ sg.Button('Back' , size = (framewidth,4))]]
ModelFilterLayout = [[sg.Text('Model Vetted Status')],[sg.Checkbox('good', key="filter-model-good"), sg.Checkbox('bad', key="filter-model-bad")]]
UserFilterLayout = [[sg.Text('User Vetted Status')],[sg.Checkbox('good', key="filter-user-good"), sg.Checkbox('bad', key="filter-user-bad")]]
SatnogsFilterLayout = [[sg.Text('Satnog Vetted Status')],[sg.Checkbox('good', key="filter-satnogs-good"), sg.Checkbox('bad', key="filter-satnogs-bad")]]
layout = [[sg.Text('Observation ID: {0}'.format(observations[obvIndex]['Id']), key = 'observation_id'), sg.Text('{0} / {1}'.format(obvIndex, obvCount), key = 'observation_count', size = (65, 1)), sg.Button('filters'), sg.Button('refresh')],[sg.Frame('',[[sg.Frame('' , UserFilterLayout, visible=False, key='userfilterlayout', size=(60,10)),sg.Frame('' , ModelFilterLayout, visible=False, key='modelfilterlayout', size=(60,10)),sg.Frame('' , SatnogsFilterLayout, visible=False, key='satnogsfilterlayout', size=(60,10))]],size= (80,20))],[sg.Image(data=convert_to_bytes(observations[obvIndex]['waterfall'], imgSize), size = imgSize, key = 'image'), sg.Frame('' , framelayout)]]
window = sg.Window('Vetting GUI',layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == 'Good':
        observation = observations[obvIndex]
        observation.user_vetted_status = 'good'
        observation.save()
        print ('Event is Good')
    if event == 'filters':
        window['userfilterlayout'].update(visible=True)
        window['modelfilterlayout'].update(visible=True)
        window['satnogsfilterlayout'].update(visible=True)
        print ('Event is filters')
    if event == 'refresh':
        print(window['filter-user-good'].get())
        print(window['filter-user-bad'].get())
        query = Q(status='')
        #query = (Q(model_vetted_status='good') & Q(status='bad')) | (Q(model_vetted_status='bad') & Q(status='good'))
        #query = query & Q(user_vetted_status='good')
        if window['filter-user-good'].get():
            print("Good is checked")
            query = query | Q(user_vetted_status='good')
        if window['filter-user-bad'].get():
            print("Bad is checked")
            query = query | Q(user_vetted_status='bad')
        if window['filter-model-good'].get():
            print("Good is checked")
            query = query | Q(model_vetted_status='good')
        if window['filter-model-bad'].get():
            print("Bad is checked")
            query = query | Q(model_vetted_status='bad')
        if window['filter-satnogs-good'].get():
            print("Good is checked")
            query = query | Q(status='good')
        if window['filter-satnogs-bad'].get():
            print("Bad is checked")
            query = query | Q(status='bad')
        observations = MetaData.objects(query)
        obvCount = len(observations)
        obvIndex = 0
        print('len = ' + str(obvCount))
    if event == 'Bad':
        observation = observations[obvIndex]
        observation.user_vetted_status = 'bad'
        observation.save()
        print ('Event is Bad')
    if event == 'Back':
        if obvIndex > 0:
            obvIndex -= 1
        print ('Event is Back')
    if event == 'Next':
        if obvIndex < len(observations) - 1:
            obvIndex += 1
        print ('Event is Next')
    if obvCount != 0:
        window['image'].update(data=convert_to_bytes(observations[obvIndex]['waterfall'], imgSize), visible=True)
        window['observation_id'].update(value='Observation ID: {0}'.format(observations[obvIndex]['Id']))
        window['observation_count'].update(value = '{0} / {1}'.format(obvIndex, obvCount))
        window['metadata'].update(value='Transmitter mode = {0}\n\nSatnogs Vetted Status = {1}\n\nUser Vetted Status = {2}\n\nModel Vetted Status = {3}'.format(observations[obvIndex]['transmitter_mode'], observations[obvIndex]['status'], observations[obvIndex]['user_vetted_status'], observations[obvIndex]['model_vetted_status']))
    else:
        window['image'].update(visible=False)

window.close()



