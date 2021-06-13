import os
import requests
from shutil import copyfileobj, rmtree

from parsel import Selector
from playsound import playsound
from requests_html import HTMLSession

class Pronunciation:
    
    PATH = '.multilanguage_dictionary'
    PATH_AUDIO = PATH + '/audio'
    
    @staticmethod
    def _search(word: str, language: str)->str:
        session = HTMLSession()
        r = session.get(f'https://www.google.com/search?q={word}+pronunciation+{language}&oq={word}+pronuncia+{language}')
        r.html.render()
        return r.text
    
    
    def return_pronounce_spell(self, word: str, language: str)->str:
        element = Selector(text=self._search(word, language))
        html_element = element.css('span.seLqNc[jsname="dDjxrf"]::text').getall()
        if len(pronounce_spell := ' - '.join(html_element)) > 0:
            return pronounce_spell
        else:
            return 'There is not pronounce spell available, put accent when is necessary'
        
    
    def play_audio(self, word: str, language: str)->None:
        word = word.replace(' ', '\ ')
        if language == 'English':
            play_word = word + '_en_us_1.mp3'
        elif language == 'Portuguese':
            play_word = word + '_pt-BR_br_1.mp3'
        elif language == 'Spanish':
            play_word = word + '_es_es_1.mp3'
        play_word_path = f'./{self.PATH_AUDIO}/{play_word}'
        
        if os.path.exists(self.PATH):
            rmtree(self.PATH)
        os.makedirs(self.PATH_AUDIO)
        try:
            url = f'https://ssl.gstatic.com/dictionary/static/pronunciation/2021-03-01/audio/{word[:2]}/{play_word}'
            with requests.get(url, stream=True) as response, \
                open(play_word_path, 'wb') as file:
                copyfileobj(response.raw, file)
            playsound(play_word_path)
        except Exception as error:
            print(error)
        rmtree(self.PATH)

