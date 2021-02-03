import requests
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
            text = response.xpath('//div[has-class("def", "ddef_d", "db")]//text()').getall()
            concatenater, helper = [], ['']
            full_text = ''
            howmany = 0
            for r in range (len(text)):
                if text[r] == ': ' or r==len(text)-1:
                    if helper[howmany] in concatenater:
                        helper.pop()
                        howmany-=1
                    else:
                        concatenater.append(helper[howmany])
                    howmany+=1
                    helper.append('')
                else:
                    helper[howmany] = helper[howmany] + text[r]
            for r in range(len(concatenater)):
                full_text = full_text + f'{r+1}°: ' + concatenater[r] + '\n\n'
                
            if len(full_text)>0:
                return True, full_text
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
        import re
        word = unicodedata.normalize('NFD', word)
        word = re.sub('[\u0300-\u036f]', '', word)
       
        try:
            response = Selector(text=self.search(word))
            text = response.xpath('//p[@itemprop="description"]/span').getall()
            full_text, helper = '', ''
            howmany = 0
            for r in range (1, len(text) -1):
                text[r] = text[r].replace('<span>', '').replace('</span>', '').replace('<span class="tag">', '').replace('<i>', '').replace('</i>', '').replace('<a href="', '').replace('</a>', '')
                if 'class="etim"' in text[r]:
                    break
                elif 'class="cl"' in text[r]:
                    howmany +=1
                else:
                    while '>' in text[r]:
                        where = text[r].find('>')
                        helper = text[r][where+1:]
                        where = text[r].find('/')
                        text[r] = text[r][:where] + ' ' + helper
                    full_text = full_text + f'{r-howmany}°: ' + text[r] + '\n\n'
            if len(full_text)>0:
                return True, full_text
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
        import re
        word = unicodedata.normalize('NFD', word)
        word = re.sub('[\u0300-\u036f]', '', word)
        try:
            response = Selector(text=self.search(word))
            text = response.xpath('//ol[@class="entry"]//li').getall()
            full_text, helper = '', ''
            for r in range(len(text)):
                text[r] = text[r].replace('<li>', '').replace('</li>', '').replace('<br>', '\n\t\t').replace('</span>', '').replace('<span>', '').replace('<i>', '').replace('</i>', '')
                while '<span' in text[r]:
                    where = text[r].find('<')
                    helper = text[r][:where]
                    where = text[r].find('>')
                    text[r] = helper + ' ' + text[r][where+1:]
                full_text = full_text + f'{r+1}°: ' + text[r] + '\n\n'
            if len(full_text)>0:
                return True, full_text
            else:
                return False, 'Not found'
        except Exception as error:
            print(error)
            return False, error

