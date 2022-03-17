from django.test import LiveServerTestCase, SimpleTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep

import random
import string

def generateRandomString(num):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(num))

def setUpTest(self):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    self.driver = webdriver.Chrome(executable_path='/home/albert/Documents/Mansei/mms2/chromedriver', chrome_options=chrome_options)
    self.driver.get('http://127.0.0.1:8000/login')
    username = self.driver.find_element_by_name('username')
    password = self.driver.find_element_by_name('password')
    loginBtn = self.driver.find_element_by_id('submitBtn')
    username.send_keys('mike')
    password.send_keys('1234')
    loginBtn.click()




class TestLogin(SimpleTestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(executable_path='/home/albert/Documents/Mansei/mms2/chromedriver', chrome_options=chrome_options)
        self.driver.get('http://127.0.0.1:8000/login')
        username = self.driver.find_element_by_name('username')
        password = self.driver.find_element_by_name('password')
        loginBtn = self.driver.find_element_by_id('submitBtn')
        username.send_keys('mike')
        password.send_keys('1234')
        loginBtn.click()

    def test_if_welcome_in_dashboard(self):
        assert "Welcome" in self.driver.page_source
        self.driver.close()




class TestAddingInventory(SimpleTestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(executable_path='/home/albert/Documents/Mansei/mms2/chromedriver', chrome_options=chrome_options)
        self.driver.get('http://127.0.0.1:8000/login')
        username = self.driver.find_element_by_name('username')
        password = self.driver.find_element_by_name('password')
        loginBtn = self.driver.find_element_by_id('submitBtn')
        username.send_keys('mike')
        password.send_keys('1234')
        loginBtn.click()

    def test1_check_warehouse(self):
        self.driver.get('http://127.0.0.1:8000/warehouse')

        table = self.driver.find_element_by_tag_name('table')
        if len(table.find_elements_by_tag_name('td')):
            for td in table.find_elements_by_tag_name('td'):
                print(td.text)
        else: 
            self.assertEqual(1, 2)
        self.driver.close()

    def test2_adding_inventory(self):
        d = self.driver
        d.get('http://127.0.0.1:8000/merchinventory/')

        d.find_element_by_id('addInventoryBtn').click()

        sleep(2)

        

        d.find_element_by_id('id_code').send_keys(f'Auto-Test-{random.randint(0,999)}')
        d.find_element_by_id('id_name').send_keys(f'Auto-Test-{generateRandomString(5)}')
        d.find_element_by_id("id_classification").send_keys(f'Auto-Test-{generateRandomString(5)}')
        d.find_element_by_id('id_type').send_keys(f'Auto-Test-{generateRandomString(5)}')
        d.find_element_by_id('id_length').send_keys(random.randint(0, 9999))
        d.find_element_by_id('id_width').send_keys(random.randint(0, 9999))
        d.find_element_by_id('id_thickness').send_keys(random.randint(0, 9999))
        select = d.find_element_by_id('id_warehouse')

        for option in select.find_elements_by_tag_name('option'):
            option.click()
            break
        d.find_element_by_id('id_inventoryDate').send_keys('01012022')

        d.find_element_by_id('id_submit_add').click()

        sleep(3)

        assert "Success" in d.page_source




class TestQuotations(SimpleTestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(executable_path='/home/albert/Documents/Mansei/mms2/chromedriver', chrome_options=chrome_options)
        self.driver.get('http://127.0.0.1:8000/login')
        username = self.driver.find_element_by_name('username')
        password = self.driver.find_element_by_name('password')
        loginBtn = self.driver.find_element_by_id('submitBtn')
        username.send_keys('mike')
        password.send_keys('1234')
        loginBtn.click()
    
    def test_create_quotations(self):
        d = self.driver
        d.get('http://127.0.0.1:8000/sales-quotations/')

        sleep(2)

        customer = d.find_element_by_id('id_customer')
        for option in customer.find_elements_by_tag_name('option'):
            option.click()
        
        for idx, option in enumerate(d.find_element_by_id('id_merchInventory_0').find_elements_by_tag_name('option')):
            if idx == 1:
                option.click()
                break

        d.find_element_by_id('id_quantity_0').send_keys(2)
        d.find_element_by_id('id_sellingPrice_0').send_keys(10000)
        for option in d.find_element_by_id('id_atc').find_elements_by_tag_name('option'):
            option.click()
            break

        d.find_element_by_id('id_remarks').send_keys('AUTO-TEST')

        d.find_element_by_id('id_submitBtn').click()

        sleep(3)

        assert "Success" in d.page_source

    def test_approve_qq(self):
        d = self.driver
        d.get('http://127.0.0.1:8000/qq-nonapproved/')

        for td in d.find_element_by_tag_name('table').find_elements_by_tag_name('td'):
            td.click()
            break