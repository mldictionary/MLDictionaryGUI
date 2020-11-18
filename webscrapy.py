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
        hear = driver.find_element_by_xpath('//*[@id="page-content"]/div[2]/div[1]/div[2]/div/div[3]/div/div/div/div[2]/span[2]/span[2]/div')
        hear.click()
    except:
        ...
    

    
def localquit():
    driver.quit()