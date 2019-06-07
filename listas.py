from decouple import config
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

login = config('LOGIN')
password = config('PASSWORD')
grupo, dominio = input('digite o endereço da lista: ').split('@')
mailfile = input("digite o caminho do arquivo de emails: ")
url = 'https://groups.google.com/a/'+dominio+'/forum/#!managemembers/'+grupo+'/add'
emails = open(mailfile, 'r').read().splitlines()

# browser
browser = webdriver.Firefox()
browser.get(url)
wait = WebDriverWait(browser, 30)

# google login
element = wait.until(ec.presence_of_element_located((By.ID, "identifierId")))
element.send_keys(login)
element.send_keys(Keys.ENTER)

# idpcafe login
element = wait.until(ec.presence_of_element_located((By.ID, "username")))
element.send_keys(login)
element = wait.until(ec.presence_of_element_located((By.ID, "password")))
element.send_keys(password)
element.send_keys(Keys.ENTER)

# groups interface
element = wait.until(ec.presence_of_element_located((By.CLASS_NAME, "gwt-TextArea")))
for email in emails:
    element.send_keys(email)
    element.send_keys(Keys.ENTER)
element = wait.until(ec.presence_of_element_located((By.CLASS_NAME, "jfk-button-action")))
element.click()

# espera carregar e fecha
element = wait.until(ec.presence_of_element_located((By.CLASS_NAME, "F0XO1GC-Nb-e")))
browser.close()
