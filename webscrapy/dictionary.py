import requests, re
from parsel import Selector
from abc import ABC, abstractmethod
# from multiprocessing import Process

class Dictionary(ABC):
    
    @abstractmethod
    def __repr__(self):
        ...

    
    @staticmethod
    @abstractmethod
    def _search(word):
        ...


    @abstractmethod
    def return_meaning(self, word):
        ...


class English(Dictionary):
   
    def __repr__(self):
        return 'English'
    
    @staticmethod
    def _search(word):
        return requests.get(f'https://dictionary.cambridge.org/us/dictionary/english/{word}', headers={'User-Agent': 'Mozilla/5.0'}).text

    def return_meaning(self, word):
        try:
            response = Selector(text=self._search(word))
            if len(text := response.xpath('//div[has-class("def", "ddef_d", "db")]').getall())>0:
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

    def __repr__(self):
        return 'Portuguese'

    @staticmethod
    def _search(word):
        return requests.get(f'https://www.dicio.com.br/{word}/', headers={'User-Agent': 'Mozilla/5.0'}).text

    
    def return_meaning(self, word):
        import unicodedata
        word = unicodedata.normalize('NFD', word)
        word = re.sub('[\u0300-\u036f]', '', word)
       
        try:
            response = Selector(text=self._search(word))
            text = response.xpath('//p[@itemprop="description"]/span').getall()
            if len(text := response.xpath('//p[@itemprop="description"]/span').getall())>0:
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
   
    def __repr__(self):
        return 'Spanish'
    
    @staticmethod
    def _search(word):
        return requests.get(f'https://www.wordreference.com/definicion/{word}', headers={'User-Agent': 'Mozilla/5.0'}).text
        
    
    def return_meaning(self, word):
        import unicodedata
        word = unicodedata.normalize('NFD', word)
        word = re.sub('[\u0300-\u036f]', '', word)
        try:
            response = Selector(text=self._search(word))
            if len(text := response.xpath('//ol[@class="entry"]//li').getall())>0:
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

