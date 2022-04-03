from django.test import SimpleTestCase, TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from .models import *
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import random
import string

def generateRandomString(num):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(num))

def setUpTest(self):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    self.driver = webdriver.Chrome(executable_path='/home/albert/Documents/Mansei/mms2/chromedriver', chrome_options=chrome_options)
    self.driver.get('%s%s'%(self.live_server_url, '/login/'))
    username = self.driver.find_element_by_name('username')
    password = self.driver.find_element_by_name('password')
    loginBtn = self.driver.find_element_by_id('submitBtn')
    username.send_keys('mike')
    password.send_keys('1234')
    loginBtn.click()




class TestLogin(StaticLiveServerTestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(executable_path='/home/albert/Documents/Mansei/mms2/chromedriver', chrome_options=chrome_options)
        self.driver.get('%s%s'%(self.live_server_url, '/login/'))
        username = self.driver.find_element_by_name('username')
        password = self.driver.find_element_by_name('password')
        loginBtn = self.driver.find_element_by_id('submitBtn')
        username.send_keys('mike')
        password.send_keys('1234')
        loginBtn.click()

    def test1_if_welcome_in_dashboard(self):
        assert "Welcome" in self.driver.page_source
        self.driver.close()




class TestAddingInventory(StaticLiveServerTestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(executable_path='/home/albert/Documents/Mansei/mms2/chromedriver', chrome_options=chrome_options)
        self.driver.get('%s%s'%(self.live_server_url, '/login/'))
        username = self.driver.find_element_by_name('username')
        password = self.driver.find_element_by_name('password')
        loginBtn = self.driver.find_element_by_id('submitBtn')
        username.send_keys('mike')
        password.send_keys('1234')
        loginBtn.click()

    def test1_check_warehouse(self):
        self.driver.get('%s%s'%(self.live_server_url, '/warehouse/'))

        table = self.driver.find_element_by_tag_name('table')
        if len(table.find_elements_by_tag_name('td')):
            for td in table.find_elements_by_tag_name('td'):
                print(td.text)
        else: 
            self.assertEqual(1, 2)
        self.driver.close()

    def test2_adding_inventory(self):
        d = self.driver
        d.get('%s%s'%(self.live_server_url, '/merchinventory/'))

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




class TestQuotations(StaticLiveServerTestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(executable_path='/home/albert/Documents/Mansei/mms2/chromedriver', chrome_options=chrome_options)
        self.driver.get('%s%s'%(self.live_server_url, '/login/'))
        username = self.driver.find_element_by_name('username')
        password = self.driver.find_element_by_name('password')
        loginBtn = self.driver.find_element_by_id('submitBtn')
        username.send_keys('mike')
        password.send_keys('1234')
        loginBtn.click()
    
    def test_create_and_approve_quotations(self):
        d = self.driver
        d.get('%s%s'%(self.live_server_url, '/sales-quotations/'))

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

        ##### APPROVING #####

        d = self.driver
        d.get('%s%s'%(self.live_server_url, '/qq-nonapproved/'))

        for td in d.find_element_by_tag_name('table').find_elements_by_tag_name('td'):
            td.click()
            break

        sleep(1)

        d.find_element_by_id('btn-approved').click()

        sleep(1)

        assert "Success" in d.page_source


####################################################################################
##### CREATE A TEST FOR ALL SALES AND CHECK WHETHER THEIR JOURNALS ARE CORRECT #####
####################################################################################


##### SALES ORDER #####

# TEST 1: CREATE AN SC AND ASSERT THAT THE TOTAL AMOUNT IS CORRECT
# TEST 2: APPROVE SC AND ASSERT THAT AMOUNTS MATCH THEIR CORRESPONDING ACCOUNTS
# TEST 3: VOID SC AND ASSERT THAT AMOUNTS MATCH THEIR CORRESPONDING ACCOUNTS

# DO IT TO ALL SALES
class TestSalesContract(StaticLiveServerTestCase):
    reset_sequences = False
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(executable_path='/home/albert/Documents/Mansei/mms2/chromedriver', chrome_options=chrome_options)
        self.driver.get('%s%s'%(self.live_server_url, '/login/'))
        username = self.driver.find_element_by_name('username')
        password = self.driver.find_element_by_name('password')
        loginBtn = self.driver.find_element_by_id('submitBtn')
        username.send_keys('mike')
        password.send_keys('1234')
        loginBtn.click()

        ##### INITIALIZE ACCOUNTS NEEDED FOR AN SC TRANSACTION #####
        # CREDIT OTHER INCOME
        # CREDIT OUTPUT VAT
        # CREDIT SALES
        # CREDIT MERCHANDISE INVENTORY
        # DEBIT ACCOUNTS RECEIVABLE
        # DEBIT COST OF SALES
        self.branch = Branch.objects.get(name='Test2')
        dChildAccount = self.branch.branchProfile.branchDefaultChildAccount
        

        self.initOtherIncome = dChildAccount.otherIncome
        self.initOutputVat = dChildAccount.outputVat
        self.initSales = dChildAccount.sales
        self.initMerchInventory = dChildAccount.merchInventory
        self.initAr = AccountChild.objects.get(name="Trade Receivable", branch=self.branch)
        self.initCostOfSales = dChildAccount.costOfSales

    def test1_create_sc(self):
        print(self.initOtherIncome.amount)
        print(self.initOutputVat.amount)
        print(self.initSales.amount)
        print(self.initMerchInventory.amount)
        print(self.initAr.amount)
        print(self.initCostOfSales.amount)

        d = self.driver
        d.get('%s%s'%(self.live_server_url, '/sales-contract/'))

        sleep(1)

        for idx, option in enumerate(d.find_element_by_id('id_customer').find_elements_by_tag_name('option')):
           if idx == 1:
                option.click()
                break

        for idx, option in enumerate(d.find_element_by_id('id_merchInventory').find_elements_by_tag_name('option')):
            if idx == 1:
                option.click()
                break

        d.find_element_by_id('id_qty').send_keys(2)
        d.find_element_by_id('id_sellingPrice').send_keys(10000)

        for idx, option in enumerate(d.find_element_by_id('id_atc').find_elements_by_tag_name('option')):
            if idx == 0:
                option.click()
                break

        d.find_element_by_id('id_submitBtn').click()

        sleep(5)

        print('---------------------------\n')

        ##### APPROVALS #####

        d = self.driver
        d.get('%s%s'%(self.live_server_url, '/sc-nonapproved/'))

        for td in d.find_element_by_tag_name('table').find_elements_by_tag_name('td'):
            td.click()
            break

        sleep(2)

        d.find_element_by_id('id_approve').click()
        sleep(2)
        d.get('%s%s'%(self.live_server_url, '/journal/'))

        sleep(5)


        self.branch = Branch.objects.get(name='Test2')
        dChildAccount = self.branch.branchProfile.branchDefaultChildAccount

        print(dChildAccount.otherIncome.amount)
        print(dChildAccount.outputVat.amount)
        print(dChildAccount.sales.amount)
        print(dChildAccount.merchInventory.amount)
        print(AccountChild.objects.get(name="Trade Receivable", branch=self.branch).amount)
        print(dChildAccount.costOfSales.amount)


        print('---------------------------\n')

        print(abs(Decimal(self.initOtherIncome.amount) - Decimal(dChildAccount.otherIncome.amount)))
        print(abs(Decimal(self.initOutputVat.amount) - Decimal(dChildAccount.outputVat.amount)))
        print(abs(Decimal(self.initSales.amount) - Decimal(dChildAccount.sales.amount)))
        print(abs(Decimal(self.initMerchInventory.amount) - Decimal(dChildAccount.merchInventory.amount)))
        print(abs(Decimal(self.initCostOfSales.amount) - Decimal(dChildAccount.costOfSales.amount)))