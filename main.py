import PySimpleGUI as sg
from webscrapy import English, Portuguese

sg.theme('Dark')

layout = [
    [sg.T('Search'), sg.In(default_text='', key='input', size=(30,10)), sg.B    (button_text='search', size=(6, 1), key='search'), sg.B(button_text='hear', key='hear'), sg.DropDown(['English', 'Portuguese'], default_value='English', key='options', enable_events=True)],
    [sg.Multiline(key='answer', size=(65, 10), text_color='Black', background_color='grey', disabled=True)],
    [sg.B('help', key='help')]]

window = sg.Window('MultiLanguage Dictionary', layout)

english = English()
language = list()
while True:
    event, values = window.read()
    
    try:
        language.append(values['options'])
    except:
        ...
        
    if event == sg.WIN_CLOSED:
        break

    if event == 'options':
        new_language = values['options']
        if language != new_language:
            if new_language == 'Portuguese':
                del english
                portuguese = Portuguese()
            else:
                del portuguese
                english = English()
        else:
            ...
            
        while True:
            if len(language) == 1:
                break
            language.pop(0)
                        
    if event == 'search':
        if len(values['input']) == 0:
            window['answer'].update('write something')
        else:
            if language[0] == 'English':
                window['answer'].update(english.returnMeaning(values['input']))
            elif language[0] == 'Portuguese':
                window['answer'].update(portuguese.returnMeaning(values['input']))
    
    if event == 'hear':
        if language[0] == 'English':
            english.playonthesound()
        elif language[0] == 'Portuguese':
            sg.popup('The sound is not working in Portuguese', title='warning')
                 
    if event == 'help':
        sg.popup('This is the Multi language program that take your language choice and one word this language and show your definition, able play the word\'s sound\nlanguage options: English and Portuguese', title='help')


try:
    del portuguese
except:
    del english