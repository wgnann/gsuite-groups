import argparse
import csv
import pickle
import requests
import sys
from decouple import config
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

class GoogleGroup:
    def __init__(self, grupo, dominio, dologin=True):
        self.grupo = grupo
        self.dominio = dominio
        self.browser = None
        self.wait = None

        if (dologin):
            self.browser, self.wait = self.login()

    def login(self):
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

        return browser, wait

    def subscribe(self, emails):
        wait = self.wait

        # neste trecho, estamos na página de subscribe

        # groups interface
        element = wait.until(ec.presence_of_element_located((By.CLASS_NAME, "gwt-TextArea")))
        for email in emails:
            element.send_keys(email)
            element.send_keys(Keys.ENTER)
        element = wait.until(ec.presence_of_element_located((By.CLASS_NAME, "jfk-button-action")))
        element.click()

        # espera carregar e fecha
        element = wait.until(ec.presence_of_element_located((By.CLASS_NAME, "F0XO1GC-Nb-e")))

    def list(self, dologin=True):
        if (dologin):
            cookies = self.browser.get_cookies()
            with open(config('COOKIE'), "wb") as fd:
                pickle.dump(cookies, fd)
        else:
            with open(config('COOKIE'), "rb") as fd:
                cookies = pickle.load(fd)

        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])
        url = 'https://groups.google.com/a/'+self.dominio+'/forum/exportmembers/'+self.grupo

        request = session.get(url)

        raw = csv.reader(request.text.splitlines())
        membros = [r for r in raw]
        membros.pop(0)
        return [membro[0] for membro in membros if membro[2] != 'banido']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action='store_true', help="debug")
    subparsers = parser.add_subparsers(title="command", dest="command", required=True)

    # subscribe
    parser_subscribe = subparsers.add_parser('subscribe')
    parser_subscribe.add_argument("lista", help="endereço da lista de email")
    parser_subscribe.add_argument("emails", nargs='?', help="arquivo de emails")

    # list
    parser_list = subparsers.add_parser('list')
    parser_list.add_argument("lista", help="endereço da lista de email")
    parser_list.add_argument("-l", "--login", action='store_true', help="faz login")

    args = parser.parse_args()
    grupo, dominio = args.lista.split('@')

    if (not args.debug):
        display = Display()
        display.start()

    if (args.command == "subscribe"):
        google = GoogleGroup(grupo, dominio)
        if (args.emails):
            emails = open(args.emails, 'r').read().splitlines()
        else:
            emails = [line.rstrip() for line in sys.stdin]
        google.subscribe(emails)

    elif (args.command == "list"):
        google = GoogleGroup(grupo, dominio, dologin=args.login)
        for member in google.list(dologin=args.login):
            print (member)

    else:
        print("modo inválido.")

    if (google.browser):
        google.browser.close()
    if (not args.debug):
        display.stop()

if __name__ == "__main__":
    main()
