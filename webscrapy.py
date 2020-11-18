from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True 
driver = webdriver.Chrome(executable_path='chrome/chromedriver', options=options)
    
def search(word):
    driver.get(f'https://dictionary.cambridge.org/pt/dicionario/ingles/{word}')


    
def returnMeaning():
    try:
        return driver.find_element_by_class_name('db').text
    except:
        return 'Not found'



def playonthesound():
    try:
        hear = driver.find_element_by_class_name('i-volume-up')
        hear.click()
    except:
        ...
    

    
def localquit():
    driver.quit()