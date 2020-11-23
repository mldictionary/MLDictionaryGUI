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
        return requests.get(f'https://www.oxfordlearnersdictionaries.com/us/definition/english/{word}?q={word}', headers={'User-Agent': 'Mozilla/5.0'}).text
        

    def returnMeaning(self, word):
        self.response = Selector(text=self.search(word))
        try:
            self.text = self.response.xpath('//span[@class="def"]/text()').getall()
            self.full_text = ''
            self.howmany = 0
            for r in range(len(self.text)):
                if len(self.text[r].split())<3:
                    self.howmany+=1
                    ...
                else:
                    self.full_text = self.full_text + f'{r+1-(self.howmany)}°: ' + self.text[r] + '\n\n'
                
            if len(self.full_text)>0:
                return self.full_text
            else:
                return 'not found'
        except:
                return 'not found'


class Portuguese(Dictionary):
    def __init__(self):
        super().__init__()


    def __repr__(self):
        return 'Portuguese'

    
    def search(self, word):
        return requests.get(f'https://www.dicio.com.br/{word}/', headers={'User-Agent': 'Mozilla/5.0'}).text

    
    def returnMeaning(self, word):
        self.response = Selector(text=self.search(word))
        try:
            self.text = self.response.xpath('//p[@itemprop="description"]/span//text()').getall()
            self.full_text = ''
            self.howmany = 0
            for r in range(1, len(self.text)-1):
                if len(self.text[r].split())<3:
                    self.howmany +=1
                elif 'Etimologia' in self.text[r]:
                    break
                else:
                    self.full_text = self.full_text + f'{r-self.howmany}°: ' + self.text[r] + '\n\n'
                    
            if len(self.full_text)>0:
                return self.full_text
            else:
                return 'not found'
        except:
                return 'not found'
        

class Spanish(Dictionary):
    def __init__(self):
        super().__init__()
    

    def __repr__(self):
        return 'Spanish'
    
   
    def search(self, word):
        return requests.get(f'https://www.wordreference.com/definicion/{word}', headers={'User-Agent': 'Mozilla/5.0'}).text
        
    
    def returnMeaning(self, word):
        self.response = Selector(text=self.search(word))
        try:
            self.text = self.response.xpath('//ol[@class="entry"]//li/text()').getall()
            self.full_text = ''
            self.howmany = 0
            for r in range(len(self.text)):
                if self.text[r] == ' ':
                    self.howmany +=1
                    ...
                elif '♦' in self.text[r]:
                    self.howmany +=1
                    ...
                else:
                    self.full_text = self.full_text + f'{r+1-(self.howmany)}°: ' + self.text[r] + '\n'
            if len(self.full_text)>0:
                return self.full_text
            else:
                return 'Not found'
        except:
            return 'Not found'

