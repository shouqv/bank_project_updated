import unittest
import tempfile
from bank.file_management import FileManagement
from bank.checking_account import CheckingAccount
from bank.custome_exceptions import OverdraftRejectedError , OverdraftLimitExceededError , InactiveAccountError ,AccountIsNoneError
import os

# to check later https://www.geeksforgeeks.org/python/python-testing-output-to-stdout/


class TestCheckingAccount(unittest.TestCase):
    def setUp(self):

        with tempfile.NamedTemporaryFile(mode='w', delete=False, newline='') as temp:
            self.temp = temp
            # i removed some fields to simplfy test
            self.temp.write("account_id,first_name,balance_checking,balance_savings,status\n10001,suresh,2000,10000,active\n10002,james,10000,10000,active")
            self.temp.close()
        
        # needed to be passed 
        self.file = FileManagement(self.temp.name)
        self.account = CheckingAccount()

        
    def tearDown(self):
        os.remove(self.temp.name)
        
        
    def test_withdraw(self):
        # in the expected value i subtracted the checking balance of the id 10001 you csan see its diffrent from the inital set up value
        expected_value = [{"account_id": 10001, "first_name": "suresh","balance_checking": 0.0, "balance_savings": 10000.0, "status": "active"},
                            {"account_id": 10002, "first_name": "james","balance_checking": 10000.0, "balance_savings": 10000.0, "status": "active"}]
        # normal case
        self.assertNotEqual(self.file.data_list , expected_value)
        result = self.account.withdraw(self.file, 10001, 2000 )
        self.assertEqual(self.file.data_list , expected_value)
        self.assertEqual(result , "The new checking balance: 0.0")
        
        # subtracting more than the allowed limit of an overdraft = -100 including fee, it will be rejected
        with self.assertRaises(OverdraftRejectedError):
            self.account.withdraw(self.file, 10001, 200 )
        
        # now testing that the overdraft fee is added 
        result = self.account.withdraw(self.file, 10001, 10 )
        expected_value = [{"account_id": 10001, "first_name": "suresh","balance_checking": -45.0, "balance_savings": 10000.0, "status": "active"},
                            {"account_id": 10002, "first_name": "james","balance_checking": 10000.0, "balance_savings": 10000.0, "status": "active"}]
        self.assertEqual(self.file.data_list , expected_value)
        self.assertEqual(result ,"Overdraft! 35 fee applied\nThe new checking balance: -45.0")
        
        self.account.withdraw(self.file, 10001, 10 )
        expected_value = [{"account_id": 10001, "first_name": "suresh","balance_checking": -90.0, "balance_savings": 10000.0, "status": "active"},
                            {"account_id": 10002, "first_name": "james","balance_checking": 10000.0, "balance_savings": 10000.0, "status": "active"}]
        self.assertEqual(self.file.data_list , expected_value)
        
        # now testing if he did 2 overdraft attemppt, and tried to attempt to overdraft again the attempt limit error will be raised and the status changes to inactive 
        with self.assertRaises(OverdraftLimitExceededError):
            self.account.withdraw(self.file, 10001, 1 )
        expected_value = [{"account_id": 10001, "first_name": "suresh","balance_checking": -90.0, "balance_savings": 10000.0, "status": "inactive"},
                            {"account_id": 10002, "first_name": "james","balance_checking": 10000.0, "balance_savings": 10000.0, "status": "active"}]
        self.assertEqual(self.file.data_list , expected_value)
        
        #  now if he tried to do an operation on an inactive account, it will raise InactiveAccountError error 
        with self.assertRaises(InactiveAccountError):
            self.account.withdraw(self.file, 10001, 10 )
        
        # testing if the account at first was chosen to be none (no account) and the user tried to do an operation
        self.file.data_list = [{"account_id": 10001, "first_name": "suresh","balance_checking": "none", "balance_savings": 10000.0, "status": "active"},
                            {"account_id": 10002, "first_name": "james","balance_checking": 10000.0, "balance_savings": 10000.0, "status": "active"}]
        with self.assertRaises(AccountIsNoneError):
            self.account.withdraw(self.file, 10001, 10 )
        
        
        
        
        
    
    def test_deposit(self):
        # testing normal case of depositing
        expected_value = [{"account_id": 10001, "first_name": "suresh","balance_checking": 2750.0, "balance_savings": 10000.0, "status": "active"},
                            {"account_id": 10002, "first_name": "james","balance_checking": 10000.0, "balance_savings": 10000.0, "status": "active"}]
        result = self.account.deposit(self.file ,10001 , 750)
        self.assertEqual(self.file.data_list ,expected_value )
        self.assertEqual(result ,"The new checking balance: 2750.0" )
        
        # testing thst if the user payed what he owed, the account will be activated again
        self.file.data_list =  [{"account_id": 10001, "first_name": "suresh","balance_checking": -100.0, "balance_savings": 10000.0, "status": "inactive"}]
        expected_value = [{"account_id": 10001, "first_name": "suresh","balance_checking": 0.0, "balance_savings": 10000.0, "status": "active"}]
        result = self.account.deposit(self.file ,10001 , 100)
        self.assertEqual(self.file.data_list ,expected_value )
        self.assertEqual(result , "Checking account reactivated\nThe new checking balance: 0.0")
        self.assertEqual(CheckingAccount.overdrafts_count[10001], 0) #to ensure the overdraft is rested
        
        # testing if his account was none, meaning wasnt created in the first place and was tryint to use it
        self.file.data_list = [{"account_id": 10001, "first_name": "suresh","balance_checking": "none", "balance_savings": 10000.0, "status": "active"}]
        with self.assertRaises(AccountIsNoneError):
            self.account.deposit(self.file, 10001, 10 )
        
        
    # no need to repeat test below as the called methods are already tested:)
    def test_transfer(self):
        pass
    
    # same here, it calls a function in file management that was already tested
    def test_get_current_checking_balance(self):
        pass
    
    # here it checks if it exist meaning is it set to none or has a baklnce
    def test_check_if_account_exist(self):
        self.file.data_list = [{"account_id": 10001, "first_name": "suresh","balance_checking": "none", "balance_savings": 10000, "status": "active"},
                            {"account_id": 10002, "first_name": "james","balance_checking": 10000, "balance_savings": 10000, "status": "active"}]
        self.assertFalse(self.account.check_if_account_exist(self.file,10001))
        self.assertTrue(self.account.check_if_account_exist(self.file,10002))