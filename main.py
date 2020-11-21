import PySimpleGUI as sg
from webscrapy import English, Portuguese, Spanish

sg.theme('Dark')

layout = [
    [sg.T('Search'), sg.In(default_text='', key='input', size=(30,10)), sg.B    (button_text='search', size=(6, 1), key='search'), sg.B(button_text='hear', key='hear'), sg.DropDown(['English', 'Portuguese', 'Spanish'], default_value='English', key='options', enable_events=True)],
    [sg.Multiline(key='answer', size=(65, 10), text_color='Black', background_color='grey', disabled=True)],
    [sg.B('help', key='help')]]

window = sg.Window('MultiLanguage Dictionary', layout)

dictionary = English()

while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED:
        break

    if event == 'options':
        new_language = values['options']
        if dictionary.__repr__() != new_language:
            if new_language == 'Portuguese':
                del dictionary
                dictionary = Portuguese()
            elif new_language == 'English':
                del dictionary
                dictionary = English()
            
            else:
                del dictionary
                dictionary = Spanish()
                
        else:
            ...
                                                      
    if event == 'search':
        if len(values['input']) == 0:
            window['answer'].update('write something')
        else:
            window['answer'].update(dictionary.returnMeaning(values['input']))

    
    if event == 'hear':
        if dictionary.__repr__() == 'English':
            dictionary.playonthesound()
        elif dictionary.__repr__() == 'Portuguese' or dictionary.__repr__() == 'Spanish':
            sg.popup('The sound is not working in Portuguese/Spanish', title='warning')
                 
    if event == 'help':
        sg.popup('This is the Multi language program that take your language choice and one word this language and show your definition, able play the word\'s sound\nlanguage options: English, Portuguese and Spanish', title='help')


del dictionary