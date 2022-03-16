from django.test import LiveServerTestCase, SimpleTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep

class TestLogin(SimpleTestCase):
    def testform(self):
        #Choose your url to visit
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        selenium = webdriver.Chrome(executable_path='/home/albert/Documents/Mansei/mms2/chromedriver', chrome_options=chrome_options)
        
        selenium.get('http://127.0.0.1:8000/login')

        username = selenium.find_element_by_name('username')
        password = selenium.find_element_by_name('password')

        loginBtn = selenium.find_element_by_id('submitBtn')

        username.send_keys('mike')
        password.send_keys('1234')
        loginBtn.click()

        sleep(5)

        assert "Welcome" in selenium.page_source