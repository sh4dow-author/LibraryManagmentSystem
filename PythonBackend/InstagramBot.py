from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common import keys
import time


class InstagramBot:
    def __init__(self):
        self.browser = webdriver.Firefox(executable_path='../driver/geckodriver')
        self.browser.maximize_window()

    def closeBrowser(self):
        self.browser.close()
        self.browser.quit()

    def openInstagram(self):
        self.browser.get('https://www.instagram.com/')
        time.sleep(1)

    def logIn(self, login, password):
        login_field = self.browser.find_element_by_xpath(
            '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input')
        password_field = self.browser.find_element_by_xpath(
            '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input')
        login_field.clear()
        password_field.clear()
        login_field.send_keys(login)
        password_field.send_keys(password)
        self.browser.find_element_by_xpath(
            '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div').click()
        time.sleep(5)

    def sendMessage(self, usr, msg):
        self.browser.get(f'https://www.instagram.com/{usr}/')
        try:
            message_button = self.browser.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[1]/div/button')
            self.__writing(msg)
        except NoSuchElementException:
            try:
                follow_button = self.browser.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button')
                self.browser.find_elements_by_xpath(
                    '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[2]/button')
                follow_button.click()
                time.sleep(2)
                self.__writing(msg)
            except NoSuchElementException:
                with open('../logs/logs.txt', 'a') as f:
                    f.write(f"We can't write message to user {usr}.\n")
        time.sleep(10)

    def __writing(self, message):
        message_button = self.browser.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[1]/div/button')
        message_button.click()
        time.sleep(2)
        self.browser.find_element_by_xpath(
            '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea').send_keys(
            message + keys.Keys.ENTER)
