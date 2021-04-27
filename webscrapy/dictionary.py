import requests, re
from parsel import Selector
from abc import ABC, abstractmethod

class Dictionary(ABC):
    def __init__(self):
        self.response = None


    @abstractmethod
    def __repr__(self):
        ...

        
    @abstractmethod
    def search(self, word):
        ...


    @abstractmethod
    def returnMeaning(self, word):
        ...


class English(Dictionary):
    def __init__(self):
        super().__init__()

   
    def __repr__(self):
        return 'English'
    
  
    def search(self, word):
        return requests.get(f'https://dictionary.cambridge.org/us/dictionary/english/{word}', headers={'User-Agent': 'Mozilla/5.0'}).text

    def returnMeaning(self, word):
        try:
            response = Selector(text=self.search(word))
            text = response.xpath('//div[has-class("def", "ddef_d", "db")]').getall()
            if len(text)>0:
                text = list(map(lambda arr: re.sub('<[^>]*>', '', arr), text))
                formatted_text = ''
                how_many = 0
                for i in range(len(text)):
                    if text[i] in formatted_text:
                        how_many+=1
                    else:
                        formatted_text += f'{i+1-how_many}º: ' + text[i] + '\n\n'
                if len(formatted_text)>0:
                    return True, formatted_text.replace(':', '. ').replace('\n        \n         ', ':  ')
                else:
                    return False, 'not found'
            else:
                return False, 'not found'
        except Exception as error:
            print(error)
            return False, error


class Portuguese(Dictionary):
    def __init__(self):
        super().__init__()


    def __repr__(self):
        return 'Portuguese'

    
    def search(self, word):
        return requests.get(f'https://www.dicio.com.br/{word}/', headers={'User-Agent': 'Mozilla/5.0'}).text

    
    def returnMeaning(self, word):
        import unicodedata
        word = unicodedata.normalize('NFD', word)
        word = re.sub('[\u0300-\u036f]', '', word)
       
        try:
            response = Selector(text=self.search(word))
            text = response.xpath('//p[@itemprop="description"]/span').getall()
            if len(text)>0:
                formatted_text = ''
                global which_one
                which_one = 0
                def text_formatter(arr)->str:
                    global which_one
                    if 'class="cl"' in arr or 'class="etim"' in arr:
                        return ''
                    which_one+=1
                    return f'{which_one}º: {re.sub("<[^>]*>", "", arr)}\n\n'
                formatted_text = ''.join(list(map(text_formatter, text)))
                if len(formatted_text)>0:
                    return True, formatted_text
                else:
                    return False, 'not found'
            else:
                return False, 'not found'
        except Exception as error:
            print(error)
            return False, error
        

class Spanish(Dictionary):
    def __init__(self):
        super().__init__()
    

    def __repr__(self):
        return 'Spanish'
    
   
    def search(self, word):
        return requests.get(f'https://www.wordreference.com/definicion/{word}', headers={'User-Agent': 'Mozilla/5.0'}).text
        
    
    def returnMeaning(self, word):
        import unicodedata
        word = unicodedata.normalize('NFD', word)
        word = re.sub('[\u0300-\u036f]', '', word)
        try:
            response = Selector(text=self.search(word))
            text = response.xpath('//ol[@class="entry"]//li').getall()
            if len(text)>0:
                global which_one
                which_one = 0
                def text_formatter(arr)->str:
                    global which_one
                    which_one+=1
                    arr = arr.replace('<br>', '\n\t\t')
                    return f'{which_one}º:' + re.sub("<[^>]*>", "", arr)
                formatted_text = '\n\n'.join(list(map(text_formatter, text)))
                if len(formatted_text)>0:
                    return True, formatted_text
                else:
                    return False, 'Not found'
            else:
                return False, 'not found'
        except Exception as error:
            print(error)
            return False, error

