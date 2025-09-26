# crediting https://codingtechroom.com/question/test-if-another-method-was-called 
# for knowing how to test if a method is called correctly, as im not intrested in the logic cus its alresady was tested

import unittest
from bank.customer import Customer
import tempfile
from unittest.mock import MagicMock
import os
from bank.custome_exceptions import AccountIsNoneError,InvalidChoiceError


class TestCustomer(unittest.TestCase):
    def setUp(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, newline='') as temp:
            self.temp = temp
            self.temp.write("account_id,first_name,last_name,password,balance_checking,balance_savings,status\n10001,suresh,sigera,juagw362,2000,10000,active\n10002,james,taylor,idh36%@#FGd,none,10000,active")
            self.temp.close()
        # the temp file is needed by customer constructor/init
        self.customer = Customer(self.temp.name)
        
    def tearDown(self):
        os.remove(self.temp.name)
    
    # i have already tested that add_row really works, so here im just testing if its been called thanks to the resource :)
    def test_add_new_customer(self):
        self.customer.file_manager.add_row = MagicMock()
        self.customer.add_new_customer(10001,"sh","al","123",200,200,-100)
        self.customer.file_manager.add_row.assert_called_once()
        
    def test_login(self):
        # i will try to login as if im suresh
        self.assertTrue(self.customer.login(10001,"juagw362"))
        self.assertFalse(self.customer.login(10001,"juaGW362"))

    # no need to test for ther actual functionality as they are already tested in checking and saving test files
    def test_withdraw(self):
        with self.assertRaises(InvalidChoiceError):
            self.customer.withdraw(10001,"wrong",100000)
    def test_deposit(self):
        with self.assertRaises(InvalidChoiceError):
            self.customer.deposit(10001,"wrong",100000)
        
        
    def test_transfer(self):
        # testing c errors, as the methods called are already tested
        with self.assertRaises(InvalidChoiceError):
            self.customer.transfer(10001,"c",100)
        with self.assertRaises(ValueError):
            self.customer.transfer(10001,"c",100,"checking")
        with self.assertRaises(AccountIsNoneError):
            self.customer.transfer(10001,"c",100,"checking",10002) #10002 id account have checking as none, so cant transfer to him
        with self.assertRaises(InvalidChoiceError):
            self.customer.transfer(10001,"j",100,"checking",10002)
            
    def test_customer_greetings(self):
        self.assertEqual(self.customer.customer_greetings(10001), "suresh sigera")
        
    def test_customer_generated_id(self):
        self.assertEqual(self.customer.customer_generated_id(),10003)

