from .file_management import FileManagement
from .checking_account import CheckingAccount
from .saving_account import SavingAccount
from .custome_exceptions import AccountIsNoneError,InvalidChoiceError
from .transactions import Transaction

class Customer():
    
    def __init__(self, file_name):
        self.file_manager = FileManagement(file_name)
        self.checking_account = CheckingAccount()
        self.saving_account = SavingAccount()
        
        self.transaction = Transaction()
        
    def add_new_customer(self, account_id, first_name, last_name, password, balance_checking, balance_savings):
        status = "active"
        self.file_manager.add_row(
            account_id=account_id,
            first_name=first_name,
            last_name=last_name,
            password=password,
            balance_checking=balance_checking,
            balance_savings=balance_savings,
            status=status)
        
        
        
    def login(self,account_id, password):
        regestired_password = self.file_manager.get_field_info(account_id , "password")
        if password == regestired_password:
            return True
        else:
            return False

    def withdraw(self,account_id , account, amount ):
        account = account.lower()
        if account == "checking":
            return self.checking_account.withdraw(self.file_manager ,account_id, amount)
        elif account == "saving":
            return self.saving_account.withdraw(self.file_manager ,account_id , amount)
        else:
            raise InvalidChoiceError(f"The option:{account}, is invalid! Try again")
        
    # def withdraw(self,account_id , account, amount ):
    #     account = account.lower()
    #     account_map = {
    #     "checking": self.checking_account,
    #     "saving": self.saving_account
    #     } 
        
    #     if account not in account_map:
    #         raise InvalidChoiceError(f"The option: {account}, is invalid! Try again")
            
            
    #     before_balance = self.get_current_balance(account_id, account)
    #     result = account_map[account].withdraw(self.file_manager, account_id, amount)
    #     new_balance = self.get_current_balance(account_id, account)

    #     # Record the transaction for both account
    #     self.transaction.add_transaction(account_id,self.customer_greetings(account_id),f"withdraw {amount}",before_balance,account,new_balance)

    #     return result
            
    def deposit(self, account_id,account, amount):
        account = account.lower()
        if account == "checking":
            return self.checking_account.deposit(self.file_manager ,account_id , amount)
        elif account == "saving":
            return self.saving_account.deposit(self.file_manager ,account_id, amount)
        else:
            raise InvalidChoiceError(f"The option:{account}, is invalid! Try again")
            
    
    def transfer(self,account_id , choice, amount, from_account=None, other_customer=None):
        #
        if choice == "c" and (from_account !="checking" and from_account != "saving"): 
            raise InvalidChoiceError(f"The account:{from_account}, is invalid! Try again")
        
        match choice:
            case "a":
                return self.saving_account.transfer(self.file_manager,account_id,self.checking_account,amount)
            case "b":
                return self.checking_account.transfer(self.file_manager,account_id,self.saving_account,amount)
            case "c":
                if not from_account or not other_customer:
                    raise ValueError("the account to transfer from and the id of the other customer must be provided for this choice")
                
                if not self.checking_account.check_if_account_exist(self.file_manager,other_customer):
                    raise AccountIsNoneError(f"The customer {other_customer} does not have an account, cant transfer!")
                
                
                if other_customer != account_id:
                    result = self.withdraw(account_id , from_account, amount)
                    self.checking_account.deposit(self.file_manager ,other_customer,amount, False)
                return result
            case _:
                raise InvalidChoiceError(f"The option:{choice}, is invalid! Try again")
            
                
    def get_current_balance(self ,account_id , account ):
        if account == "checking":
            return self.checking_account.get_current_checking_balance(self.file_manager ,account_id )
        elif account == "saving":
            return self.saving_account.get_current_saving_balance(self.file_manager ,account_id)
        else:
            raise InvalidChoiceError(f"The option:{account}, is invalid! Try again")
        
    def create_account(self, account_id, field, new_balance_checking ):
        self.file_manager.update_row(account_id,field,new_balance_checking)
    
    def customer_generated_id(self):
        return self.file_manager.get_last_row_id() + 1
    
    def customer_greetings(self, account_id):
        message = self.file_manager.get_field_info(account_id,"first_name")
        message = message +" " +self.file_manager.get_field_info(account_id,"last_name")
        return message
    
    # extra from me, so that i can customize any input that i wanna convert to a number and could raise a value error
    def customer_entered_numbers(self,number,message,type="float"):
        try:
            if type.lower() == "int":
                number = int(number)
            else:
                number = float(number)
            return number
        except ValueError:
            raise ValueError(message)
        except TypeError:
            raise TypeError(message)
    
    