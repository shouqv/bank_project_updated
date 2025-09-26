from .file_management import FileManagement
# crediting https://www.geeksforgeeks.org/python/get-current-date-and-time-using-python/
import datetime
class Transaction():
    def __init__(self):
        self.transaction_file = FileManagement("data/transaction.csv")
        pass
    def add_transaction(self,account_id,name,operation_detail,before_balance,affected_account,new_balance,transfer_flag = False):
        if transfer_flag:
            operation_id = self.get_last_operation_id(account_id) #so that if someone transfered between his accounts, both the transaction will have the same operation id
        else:
            operation_id = self.get_last_operation_id(account_id) + 1 
            
        self.transaction_file.add_row(
            account_id = account_id,
            operation_id = operation_id,
            name = name,
            operation_detail = operation_detail,
            time = datetime.datetime.now(),
            before_balance = before_balance,
            affected_account = affected_account,
            new_balance=new_balance
        )

    def get_last_operation_id(self,customer_id):
        # if not self.transaction_file.data_list: #if list is empty return 0, cyus it will be his first operation
        #     return 0
        for row in reversed(self.transaction_file.data_list):  
            if row["account_id"] == customer_id:
                return row["operation_id"]
        return 0