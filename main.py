import PySimpleGUI as sg
from webscrapy import Dictionary

sg.theme('Dark')

layout = [
    [sg.T('Search'), sg.In(default_text='', key='input', size=(30,10)), sg.B    (button_text='search', size=(6, 1), key='search'), sg.B(button_text='hear', key='hear')],
    [sg.Multiline(key='answer', size=(65, 10), text_color='Black', background_color='grey', disabled=True)],
    [sg.B('help', key='help')]]

window = sg.Window('Dictionary', layout)

english = Dictionary(False)

while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED:
        break

    if event == 'search':
        if len(values['input']) == 0:
            window['answer'].update('write something')
        else:
            window['answer'].update(english.returnMeaning(values['input']))
    
    if event == 'hear':
        english.playonthesound()
        
    if event == 'help':
        sg.popup('This is a program that searches for any word you choose and shows the meaning found for that word according to the dictionary "https://dictionary.cambridge.org/pt/"', title='help')


english.localquit()