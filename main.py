import PySimpleGUI as sg
import webscrapy
sg.Input()
sg.theme('Dark')
layout = [
    [sg.T('Search'), sg.In(default_text='', key='input', size=(30,10)), sg.B(button_text='search', size=(6, 1), key='search'), sg.B(button_text='hear', key='hear')],
    [sg.T(key='answer', size=(50, 5), background_color = 'grey', text_color='Black', pad=(50, 13))],
    [sg.B('help', key='help')]]

window = sg.Window('Dictionary', layout)

while True:
    
    event, values = window.read()
    
    if event == sg.WIN_CLOSED:
        break

    if event == 'search':
        if len(values['input']) == 0:
            window['answer'].update('write something')
        else:
            webscrapy.search(values['input'])
            window['answer'].update(webscrapy.returnMeaning())
    
    if event == 'hear':
        webscrapy.playonthesound()
        
    if event == 'help':
        sg.popup('This is a program that searches for any word you choose and shows the first meaning found for that word according to the dictionary "https://dictionary.cambridge.org/pt/"', title='help')


webscrapy.localquit()