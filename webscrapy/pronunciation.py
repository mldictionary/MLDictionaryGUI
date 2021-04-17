from requests_html import HTMLSession
import os

from parsel import Selector

class Pronunciation:

    def search(self, word, language):
        session = HTMLSession()
        r = session.get(f'https://www.google.com/search?q={word}+pronunciation+{language}&oq={word}+pronuncia+{language}')
        r.html.render()
        return r.text
    
    
    def return_pronounce_spell(self, word, language):
        element = Selector(text=self.search(word, language))
        html_element = element.css('span.seLqNc[jsname="dDjxrf"]::text').getall()
        pronounce_spell = ' - '.join(html_element)
        if len(pronounce_spell.strip()) > 0:
            return pronounce_spell
        else:
            return 'There is not pronounce spell available, put accent when is necessary'
        
    
    def play_audio(self, word, language):
        if language == 'English':
            play_word = word + '_en_us_1.mp3'
        elif language == 'Portuguese':
            play_word = word + '_pt-BR_br_1.mp3'
        elif language == 'Spanish':
            play_word = word + '_es_es_1.mp3'
        else:
            return
        try:
            os.system(f'wget https://ssl.gstatic.com/dictionary/static/pronunciation/2021-03-01/audio/{word[:2]}/{play_word}; mpg123 {play_word}; rm {play_word}')
        except:
            ...
        
