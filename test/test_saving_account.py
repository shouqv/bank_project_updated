import unittest
import tempfile
from bank.file_management import FileManagement
from bank.saving_account import SavingAccount
from bank.custome_exceptions import OverdraftRejectedError ,AccountIsNoneError
import os


# not sure if this testing necessary as it really similar to checking class hmmm

class TestSavingAccount(unittest.TestCase):
    def setUp(self):

        with tempfile.NamedTemporaryFile(mode='w', delete=False, newline='') as temp:
            self.temp = temp
            # i removed some fields to simplfy test
            self.temp.write("account_id,first_name,balance_checking,balance_savings,status\n10001,suresh,2000,10000,active")
            self.temp.close()
        
        # the file needed to be passed later for the SavingAccount functions
        self.file = FileManagement(self.temp.name)
        self.account = SavingAccount()

        
    def tearDown(self):
        os.remove(self.temp.name)
        
        
    def test_withdraw(self):
        # the below expected_value shows the result of what expected to happen after i do withdraw
        expected_value = [{"account_id": 10001, "first_name": "suresh","balance_checking": 2000, "balance_savings": 4000, "status": "active"}]
        # normal case
        self.assertNotEqual(self.file.data_list , expected_value) #if i didnt withdraw yet, the amount not similar 
        result = self.account.withdraw(self.file, 10001, 6000 )
        self.assertEqual(self.file.data_list , expected_value)
        self.assertEqual(result , "The new saving balance: 4000")
        
        # when trying to do an overdraft, it will raise the rejected oversdaraft error since its a saving account
        with self.assertRaises(OverdraftRejectedError):
            self.account.withdraw(self.file, 10001, 4001 )
        

        
        # testing if the account at first was chosen to be none (no account) and the user tried to do an operation
        self.file.data_list = [{"account_id": 10001, "first_name": "suresh","balance_checking": 2000, "balance_savings": "none", "status": "active"}]
        with self.assertRaises(AccountIsNoneError):
            self.account.withdraw(self.file, 10001, 10 )
        
        
        
        
        
    
    def test_deposit(self):
        # testing normal case of depositing
        expected_value = [{"account_id": 10001, "first_name": "suresh","balance_checking": 2000, "balance_savings": 13700, "status": "active"}]
        result = self.account.deposit(self.file ,10001 , 3700)
        self.assertEqual(self.file.data_list ,expected_value )
        self.assertEqual(result ,"The new saving balance: 13700" )
        
        
        # testing if his account was none, meaning wasnt created in the first place and was tryint to use it
        self.file.data_list = [{"account_id": 10001, "first_name": "suresh","balance_checking": 2000, "balance_savings": "none", "status": "active"}]
        with self.assertRaises(AccountIsNoneError):
            self.account.deposit(self.file, 10001, 10 )
        
        
    # no need to repeat test below as the called methods are already tested:)
    def test_transfer(self):
        pass
    
    # same here, it calls a function in file management that was already tested
    def test_get_current_saving_balance(self):
        pass
    
    # here it checks if it exist meaning is it set to none or has a baklnce
    def test_check_if_account_exist(self):
        self.file.data_list = [{"account_id": 10001, "first_name": "suresh","balance_checking": 200, "balance_savings": "none", "status": "active"},
                            {"account_id": 10002, "first_name": "james","balance_checking": 200, "balance_savings": 10000, "status": "active"}]
        self.assertFalse(self.account.check_if_account_exist(self.file,10001))
        self.assertTrue(self.account.check_if_account_exist(self.file,10002))