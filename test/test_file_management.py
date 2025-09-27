import unittest

from bank.file_management import FileManagement
from bank.custome_exceptions import CustomerNotFoundError


import tempfile
import os


class TestFileManagement(unittest.TestCase):
    def setUp(self):
        
        # self.file = FileManagement("")
        # crediting https://sqlpey.com/python/top-4-methods-to-unit-test-file-writing-functions-in-python-using-unittest/ for the below idea
        # crediting the following for making me understand more:
        # https://www.geeksforgeeks.org/python/create-temporary-files-and-directories-using-python-tempfile/
        # https://docs.python.org/3/library/tempfile.html
        with tempfile.NamedTemporaryFile(mode='w', delete=False, newline='') as temp:
            self.temp = temp
            self.temp.write("account_id,first_name,last_name,password,balance_checking,balance_savings,status\n10001,suresh,sigera,juagw362,2000,10000,active\n10002,james,taylor,idh36%@#FGd,10000,10000,active")
            self.temp.close()
        
        
        self.file = FileManagement(self.temp.name)


        
    def tearDown(self):
        os.remove(self.temp.name)
    
    def test_is_number(self):
        self.assertTrue(self.file.is_number("11"))
        self.assertTrue(self.file.is_number("-11"))
        self.assertFalse(self.file.is_number("hello"))
        
        
    def test_load_data(self):
        # here it checks if file not found the error is raised correctle
        with self.assertRaises(FileNotFoundError):
            FileManagement("non_existent_file.csv")
        # based on the values i populated in the setup , the datalist should have the same values as the one in the file
        expected_content = [{"account_id": 10001, "first_name": "suresh", "last_name": "sigera", "password": "juagw362", "balance_checking": 2000, "balance_savings": 10000, "status": "active"},
                            {"account_id": 10002, "first_name": "james", "last_name": "taylor", "password": "idh36%@#FGd", "balance_checking": 10000, "balance_savings": 10000, "status": "active"}]
        
        self.assertEqual(self.file.data_list, expected_content)
            
            
            
    def test_get_row(self):
        self.file.data_list = [
{'account_id': 10004, 'first_name': 'stacey', 'last_name': 'abrams','password': 'DEU8_qw3y72$', 'balance_checking': 2000, 'balance_savings': 20000, "status": "active"}]
        self.assertEqual(self.file.get_row(10004), self.file.data_list[0])
        # testing when not found
        with self.assertRaises(CustomerNotFoundError):
            self.file.get_row(10070)
    

    def test_write_to_file(self):
        # simplfying the data
        self.file.fields= ["field1", "field2"]
        self.file.data_list = [{"field1":100 , "field2":200}]
        
        # if i called this, it should be written to the file
        self.file.write_to_file()
        
        # obtaining whats written in the file
        with open(self.temp.name, 'r') as f:
            content = f.read()
        # checking if its equal
        self.assertEqual(content,"field1,field2\n100,200\n")
    
    def test_update_row(self):
        # ive already tested if the data list write to the file corectly , so now im juyts testing if the data list updates correctly
        expected_content = [{"account_id": 10001, "first_name": "shouq", "last_name": "sigera", "password": "juagw362", "balance_checking": 2000, "balance_savings": 10000, "status": "active"},
                            {"account_id": 10002, "first_name": "james", "last_name": "taylor", "password": "idh36%@#FGd", "balance_checking": 10000, "balance_savings": 10000, "status": "active"}]
        self.assertNotEqual(self.file.data_list,expected_content)
        self.file.update_row(10001,'first_name',"shouq")
        self.assertEqual(self.file.data_list,expected_content)
        
        with self.assertRaises(CustomerNotFoundError):
            self.file.update_row(10003,'first_name',"nada")
        
    
    def test_add_row(self):
        self.file.add_row(
            account_id=10010,
            first_name="shouq",
            last_name="almutairi",
            password="1@shouq@123",
            balance_checking=300,
            balance_savings=5000000,
            status="active")
        self.assertIn({'account_id': 10010, 'first_name': 'shouq', 'last_name': 'almutairi','password': "1@shouq@123", 'balance_checking': 300, 'balance_savings': 5000000,"status": "active"}, self.file.data_list)
        
        with self.assertRaises(ValueError):
            self.file.add_row(
            account=10010, #i have changed the name here diffrently than the fields withihn the csv file, this will make inconsisities in the dect list
            first_name="shouq",
            last_name="almutairi",
            password="1@shouq@123",
            balance_checking=300,
            balance_savings=5000000,
            status="active")
        
    def test_get_field_info(self):
        self.assertEqual(self.file.get_field_info(10001,'first_name') , "suresh")
        self.assertNotEqual(self.file.get_field_info(10001,'first_name') , "notInFile")
        with self.assertRaises(CustomerNotFoundError):
            self.file.get_field_info(10049,'first_name')
            
            
    def test_get_last_row_id(self):
        expected_value= 10002 #based on the value i populated in the setup
        self.assertEqual(self.file.get_last_row_id(),expected_value)
        
        self.file.data_list=[] #making it empty to test the raising of an error
        with self.assertRaises(ValueError):
            self.file.get_last_row_id()

    def test_convert_data_type(self):
        self.file.data_list = [{"account_id":"100" , "balance_checking":"200","password":"234563"}]
        # this to demenstrate that the method will indeed convert the reqired numbers to int while keeping password as string
        expected_value = [{"account_id":100 , "balance_checking":200,"password":"234563"}]
        self.assertNotEqual(self.file.data_list,expected_value)
        self.file.convert_data_type()
        self.assertEqual(self.file.data_list,expected_value)
        
    def test_add_row_and_get_last_row_id(self):
        # adding new user, other than the ones in the set up
        self.file.add_row(
        account_id=10021,
        first_name="new",
        last_name="Customer",
        password="123",
        balance_checking=100,
        balance_savings=200,
        status="active"
        )
        self.assertEqual(self.file.get_last_row_id(), 10021)

        