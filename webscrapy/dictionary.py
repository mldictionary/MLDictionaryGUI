import requests, re
from parsel import Selector
from abc import ABC, abstractmethod
from typing import List
# from multiprocessing import Process

class Dictionary(ABC):
    URL: str
    XPATH: str
    
    @abstractmethod
    def __repr__(self):
        ...

    
    @classmethod
    def _search(cls, word: str)->str:
        return requests.get(cls.URL.format(word), headers={'User-Agent': 'Mozilla/5.0'}).text

    @classmethod
    def _get_meanings(cls, word: str)->List[str]:
        response = Selector(text=cls._search(word))
        return response.xpath(cls.XPATH).getall()


    @abstractmethod
    def return_meaning(self, word):
        ...


class English(Dictionary):
    URL = 'https://dictionary.cambridge.org/us/dictionary/english/{}'
    XPATH = '//div[has-class("def", "ddef_d", "db")]'
    
    def __repr__(self):
        return 'English'


    def return_meaning(self, word):
        try:
            if len(text := self._get_meanings(word))>0:
                text = list(map(lambda arr: re.sub('<[^>]*>', '', arr), text))
                formatted_text = ''
                how_many = 0
                for i in range(len(text)):
                    if text[i] in formatted_text:
                        how_many+=1
                        continue
                    else:
                        formatted_text += f'{i+1-how_many}º: ' + text[i].replace(':', '.') + '\n\n'
                if len(formatted_text)>0:
                    return True, formatted_text.replace('\n        \n         ', ':  ')
                else:
                    return False, 'not found'
            else:
                return False, 'not found'
        except Exception as error:
            print(error)
            return False, error


class Portuguese(Dictionary):
    URL = 'https://www.dicio.com.br/{}/'
    XPATH = '//p[@itemprop="description"]/span'
    
    def __repr__(self):
        return 'Portuguese'


    def return_meaning(self, word):
        import unicodedata
        word = unicodedata.normalize('NFD', word)
        word = re.sub('[\u0300-\u036f]', '', word)
    
        try:
            if len(text := self._get_meanings(word))>0:
                formatted_text = ''
                which_one = 0
                def text_formatter(arr)->str:
                    nonlocal which_one
                    if 'class="cl"' in arr or 'class="etim"' in arr:
                        return ''
                    which_one+=1
                    return f'{which_one}º: {re.sub("<[^>]*>", "", arr)}\n\n'
                if len(formatted_text := ''.join(list(map(text_formatter, text))))>0:
                    return True, formatted_text
                else:
                    return False, 'not found'
            else:
                return False, 'not found'
        except Exception as error:
            print(error)
            return False, error
        

class Spanish(Dictionary):
    URL = 'https://www.wordreference.com/definicion/{}'
    XPATH = '//ol[@class="entry"]//li'
    
    def __repr__(self):
        return 'Spanish'
    
    
    def return_meaning(self, word):
        import unicodedata
        word = unicodedata.normalize('NFD', word)
        word = re.sub('[\u0300-\u036f]', '', word)
        try:
            if len(text := self._get_meanings(word))>0:
                which_one = 0
                def text_formatter(arr)->str:
                    nonlocal which_one
                    which_one+=1
                    arr = arr.replace('<br>', '\n\t\t')
                    return f'{which_one}º:' + re.sub("<[^>]*>", "", arr)
                if len(formatted_text := '\n\n'.join(list(map(text_formatter, text))))>0:
                    return True, formatted_text
                else:
                    return False, 'Not found'
            else:
                return False, 'not found'
        except Exception as error:
            print(error)
            return False, error

