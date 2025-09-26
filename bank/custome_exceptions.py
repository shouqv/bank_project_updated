class InactiveAccountError(Exception):
    # raised when trying to withdraw on inactive checking account
    pass

# crediting https://www.geeksforgeeks.org/python/define-custom-exceptions-in-python/
class AccountIsNoneError(Exception):
    # raised when tryinf to withdraw or deposit on an account that chosen to be none
    def __init__(self, message , account_name =None):
        super().__init__(message)
        self.account_name = account_name
        
        
class OverdraftRejectedError(Exception):
    # raised when the customer reach the limit of -100 in an account, or try to have an overdraft of a saving account
    pass

class OverdraftLimitExceededError(Exception):
    # when he tried to overdraft for the third time
    pass

class CustomerNotFoundError(Exception):
    pass

class InvalidChoiceError(Exception):
    pass