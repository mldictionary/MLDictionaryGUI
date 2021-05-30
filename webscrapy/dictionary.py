import requests, re, unicodedata
from parsel import Selector
from abc import ABC, abstractmethod
from typing import List, Union

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
    def _get_meanings(cls, word: str)->List[str]:
        response = Selector(text=cls._search(word))
        return response.xpath(cls.XPATH).getall()


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
            if len(text := self._get_meanings(word))>0:
                text = list(map(lambda mean: re.sub('<[^>]*>', '', mean), text))
                formatted_text = ''
                how_many = 0
                for i in range(len(text)):
                    if text[i] in formatted_text:
                        how_many+=1
                        continue
                    else:
                        formatted_text += f'{i+1-how_many}º: ' + text[i].replace(':', '.') + '\n\n'
                return formatted_text.replace('\n        \n         ', ':  ') or False
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
            if len(text := self._get_meanings(word))>0:
                which_one = 0
                def text_formatter(mean: str)->str:
                    nonlocal which_one
                    if 'class="cl"' in mean or 'class="etim"' in mean:
                        return ''
                    which_one+=1
                    return f'{which_one}º: {re.sub("<[^>]*>", "", mean)}\n\n'
                return ''.join(list(map(text_formatter, text))) or False
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
            if len(text := self._get_meanings(word))>0:
                which_one = 0
                def text_formatter(mean: str)->str:
                    nonlocal which_one
                    which_one+=1
                    mean = mean.replace('<br>', '\n\t\t')
                    return f'{which_one}º:' + re.sub("<[^>]*>", "", mean)
                return '\n\n'.join(list(map(text_formatter, text))) or False
            else:
                return False
        except Exception as error:
            print(error)
            return False
