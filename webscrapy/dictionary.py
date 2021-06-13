from abc import ABC, abstractmethod
import unicodedata
import re
import requests
from typing import Set, Union

from parsel import Selector

class Dictionary(ABC):
    URL: str
    XPATH: str
    
    @abstractmethod
    def __repr__(self)->str:
        return 'Dictionary'

    
    @classmethod
    def _search(cls, word: str)->str:
        with requests.get(cls.URL.format(word), \
                            headers={'User-Agent': 'Mozilla/5.0'}) as response:
            return response.text
        
        
    @classmethod
    def _get_meanings(cls, word: str)->Set[str]:
        response = Selector(text=cls._search(word))
        meanings = response.xpath(cls.XPATH).getall()
        return set(map(lambda mean: re.sub('<[^>]*>', '', mean), meanings))


    @abstractmethod
    def return_meaning(self, word: str)->Union[str, bool]:
        ...


class English(Dictionary):
    URL = 'https://dictionary.cambridge.org/us/dictionary/english/{}'
    XPATH = '//div[has-class("def", "ddef_d", "db")]'
    
    def __repr__(self)->str:
        return 'English'


    def return_meaning(self, word: str)->Union[str, bool]:
        try:
            if len(meanings := self._get_meanings(word))>0:
                how_many = 0
                def text_formatter(mean: str)->str:
                    nonlocal how_many
                    how_many += 1
                    mean = mean.replace('\n    \t                ', '').replace(':', '.')
                    return f'{how_many}°: ' + mean
                return '\n\n'.join(list(map(text_formatter, meanings))).replace('\n        \n         ', ':  ') or False
            else:
                return False
        except Exception as error:
            print(error)
            return False


class Portuguese(Dictionary):
    URL = 'https://www.dicio.com.br/{}/'
    XPATH = '//p[@itemprop="description"]/span'
    
    def __repr__(self)->str:
        return 'Portuguese'


    def return_meaning(self, word: str)->Union[str, bool]:
        word = unicodedata.normalize('NFD', word)
        word = re.sub('[\u0300-\u036f]', '', word)
        try:
            if len(meanings := self._get_meanings(word))>0:
                index = 0
                def text_formatter(mean: str)->str:
                    nonlocal index
                    if 'class="cl"' in mean or 'class="etim"' in mean:
                        return ''
                    index+=1
                    return f'{index}º: ' + mean
                return '\n\n'.join(list(map(text_formatter, meanings))) or False
            else:
                return False
        except Exception as error:
            print(error)
            return False
        

class Spanish(Dictionary):
    URL = 'https://www.wordreference.com/definicion/{}'
    XPATH = '//ol[@class="entry"]//li'
    
    def __repr__(self)->str:
        return 'Spanish'
    
    
    def return_meaning(self, word: str)->Union[str, bool]:
        word = unicodedata.normalize('NFD', word)
        word = re.sub('[\u0300-\u036f]', '', word)
        try:
            if len(meanings := self._get_meanings(word))>0:
                index = 0
                def text_formatter(mean: str)->str:
                    nonlocal index
                    index+=1
                    mean = mean.replace('<br>', '\n\t\t')
                    return f'{index}º: ' + mean
                return '\n\n'.join(list(map(text_formatter, meanings))) or False
            else:
                return False
        except Exception as error:
            print(error)
            return False
