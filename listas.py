import argparse
import sys
from decouple import config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class GoogleGroup:
    def __init__(self, grupo, dominio):
        self.grupo = grupo
        self.dominio = dominio
        login = config('LOGIN')
        password = config('PASSWORD')
        url = 'https://groups.google.com/a/'+self.dominio+'/forum/#!managemembers/'+self.grupo+'/add'

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

        self.browser = browser
        self.wait = wait

    def subscribe(self, emails):
        browser = self.browser
        wait = self.wait

        # groups interface
        element = wait.until(ec.presence_of_element_located((By.CLASS_NAME, "gwt-TextArea")))
        for email in emails:
            element.send_keys(email)
            element.send_keys(Keys.ENTER)
        element = wait.until(ec.presence_of_element_located((By.CLASS_NAME, "jfk-button-action")))
        element.click()

        # espera carregar e fecha
        element = wait.until(ec.presence_of_element_located((By.CLASS_NAME, "F0XO1GC-Nb-e")))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("lista", help="endereço da lista de email")
    parser.add_argument("emails", nargs='?', help="arquivo de emails")
    args = parser.parse_args()

    grupo, dominio = args.lista.split('@')
    mailfile = args.emails

    if (args.emails):
        emails = open(mailfile, 'r').read().splitlines()
    else:
        emails = [line.rstrip() for line in sys.stdin]

    google = GoogleGroup(grupo, dominio)
    google.subscribe(emails)
    google.browser.close()

if __name__ == "__main__":
    main()
