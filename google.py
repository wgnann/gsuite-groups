import hashlib
import pickle
import time
from decouple import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

class Google:
    def __init__(self, dologin=True):
        self.browser = None
        self.cookies = None
        self.wait = None

        if (dologin):
            self.browser, self.wait = self.login()
        else:
            with open(config('COOKIE'), "rb") as fd:
                self.cookies = pickle.load(fd)

    def login(self):
        login = config('LOGIN')
        password = config('PASSWORD')
        url = 'https://accounts.google.com'

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

        # cookies
        time.sleep(10) # should use wait.until cookie
        self.cookies = browser.get_cookies()
        with open(config('COOKIE'), "wb") as fd:
            pickle.dump(self.cookies, fd)

        return browser, wait

    def get_cookie(self, name):
        for cookie in self.cookies:
            if name in cookie['name']:
                return cookie['value']
        return None

    def SAPISID_hash(self, origin):
        sapisid = self.get_cookie('SAPISID')
        now = str(round(time.time()))
        salted = now + ' ' + sapisid + ' ' + origin
        return now + '_' + hashlib.sha1(salted.encode()).hexdigest()
