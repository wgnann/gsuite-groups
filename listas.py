import argparse
import csv
import requests
import sys
from decouple import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

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

        # espera carregar
        element = wait.until(ec.presence_of_element_located((By.CLASS_NAME, "gwt-TextArea")))

        self.browser = browser
        self.wait = wait

    def subscribe(self, emails):
        wait = self.wait

        # neste trecho, estamos na página de subscribe

        # groups interface
        for email in emails:
            element.send_keys(email)
            element.send_keys(Keys.ENTER)
        element = wait.until(ec.presence_of_element_located((By.CLASS_NAME, "jfk-button-action")))
        element.click()

        # espera carregar e fecha
        element = wait.until(ec.presence_of_element_located((By.CLASS_NAME, "F0XO1GC-Nb-e")))

    def list(self):
        browser_cookies = self.browser.get_cookies()
        session = requests.Session()
        cookies = [session.cookies.set(c['name'], c['value']) for c in browser_cookies]
        url = 'https://groups.google.com/a/'+self.dominio+'/forum/exportmembers/'+self.grupo

        request = session.get(url)

        membros = csv.reader(request.text.splitlines())
        for membro in membros:
            print(membro[0])

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
