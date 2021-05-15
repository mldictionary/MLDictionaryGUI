import os, requests
from requests_html import HTMLSession
from parsel import Selector
from playsound import playsound
from shutil import copyfileobj
from sys import path


class Pronunciation:
    
    def _search(self, word, language):
        session = HTMLSession()
        r = session.get(f'https://www.google.com/search?q={word}+pronunciation+{language}&oq={word}+pronuncia+{language}')
        r.html.render()
        return r.text
    
    
    def return_pronounce_spell(self, word, language):
        element = Selector(text=self._search(word, language))
        html_element = element.css('span.seLqNc[jsname="dDjxrf"]::text').getall()
        if len(pronounce_spell := ' - '.join(html_element)) > 0:
            return pronounce_spell
        else:
            return 'There is not pronounce spell available, put accent when is necessary'
        
    
    def play_audio(self, word, language):
        word = word.replace(' ', '\ ')
        if language == 'English':
            play_word = word + '_en_us_1.mp3'
        elif language == 'Portuguese':
            play_word = word + '_pt-BR_br_1.mp3'
        elif language == 'Spanish':
            play_word = word + '_es_es_1.mp3'
        try:
            response = requests.get(f'https://ssl.gstatic.com/dictionary/static/pronunciation/2021-03-01/audio/{word[:2]}/{play_word}', stream=True)
            play_word_path = f'{path[0]}/{play_word}'
            with open(play_word_path, 'wb') as file:
                copyfileobj(response.raw, file)
            playsound(play_word_path)
            os.remove(play_word_path)
        except:
            ...
        
