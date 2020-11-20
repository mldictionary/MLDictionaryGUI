from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep
from abc import ABC, abstractmethod


class Dictionary(ABC):
    def __init__(self, options=True):
        self.option = Options()
        self.option.headless = options
        self.browser = Chrome('chrome/chromedriver', options=self.option)
        
    @abstractmethod
    def search(self, word):
        ...

    @abstractmethod
    def returnMeaning(self, word):
        ...

    @abstractmethod
    def playonthesound(self):
        ...
            
           
    def localquit(self):
        self.browser.quit()


class English(Dictionary):
    def __init__(self, options=True):
        super().__init__(options)
        
    def search(self, word):
        self.browser.get(f'https://dictionary.cambridge.org/pt/dicionario/ingles/{word}')
        
    
    def returnMeaning(self, word):
        self.search(word)
        sleep(2)
        try:
            self.text = self.browser.find_elements_by_class_name('ddef_d')
            self.full_text = ''
            for r in range(len(self.text)):
                self.full_text = self.full_text + f'{r+1}°: ' + self.text[r].text + '\n\n'
                
            if len(self.full_text)>0:
                return self.full_text
            else:
                return 'not found'
        except:
                return 'not found'
            
        
    def playonthesound(self):
        try:
            self.hear = self.browser.find_element_by_xpath('//*[@id="page-content"]/div[2]/div[1]/div[2]/div/div[3]/div/div/div/div[2]/span[2]/span[2]/div')
            self.hear.click()
        except:
            self.hear = self.browser.find_element_by_class_name('i-volume-up')
            try:
                self.hear.click()
            except:
                ...
        else:
            ...


