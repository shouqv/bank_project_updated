from .custome_exceptions import InactiveAccountError , AccountIsNoneError,OverdraftRejectedError ,OverdraftLimitExceededError
class CheckingAccount():
    overdrafts_count = {}
    
    def withdraw(self ,file, account_id, amount , flag=True):
        status = file.get_field_info(account_id, "status").lower()
        
        current_balance_checking = self.get_current_checking_balance(file,account_id)
        if status == "active":
            if self.check_if_account_exist(file,account_id):


                amount = int(amount)
                new_balance_checking = current_balance_checking - amount

                if account_id not in CheckingAccount.overdrafts_count:
                    CheckingAccount.overdrafts_count[account_id] = 0

                message = ""

                if CheckingAccount.overdrafts_count[account_id] >= 2:
                    file.update_row(account_id, "status" , "inactive")
                    raise OverdraftLimitExceededError("You have exceeded the overdraft attempt limit, account deactivated")


                if amount > current_balance_checking:
                    if new_balance_checking - 35 < -100:
                        raise OverdraftRejectedError("you have exceeded the balance limit of -100$ including the fee! operation canceled")
                        
                    else:
                        if account_id in CheckingAccount.overdrafts_count:
                            if CheckingAccount.overdrafts_count[account_id] <3:
                                new_balance_checking -= 35
                                # print("Overdraft! 35 fee applied.")
                                message = "Overdraft! 35 fee applied\n"
                                CheckingAccount.overdrafts_count[account_id] +=1


                if flag:
                    # print(f"The new checking balance: {new_balance_checking}")
                    message = message + f"The new checking balance: {new_balance_checking}"
                file.update_row(account_id, "balance_checking" , new_balance_checking)
                return message
            else:

                raise AccountIsNoneError(f"Error: the checking account with id= {account_id}, have not been initated yet", "balance_checking")
        else:
            raise InactiveAccountError(f"The account id {account_id} is inactive, please pay {current_balance_checking * -1}")

    
    
    def deposit(self ,file, account_id, amount , flag = True):
        current_balance_checking = self.get_current_checking_balance(file,account_id)
        if self.check_if_account_exist(file,account_id):
            
            amount = int(amount)
            new_balance_checking = current_balance_checking + amount
            
            message = ""
            status = file.get_field_info(account_id, "status").lower()
            if status == "inactive" and new_balance_checking>=0:
                file.update_row(account_id, "status" , "active")
                CheckingAccount.overdrafts_count[account_id] = 0
                message = "Account reactivated\n"
            
            if flag:
                message = message + f"The new checking balance: {new_balance_checking}"
            file.update_row(account_id, "balance_checking" , new_balance_checking)
            return message
        else:
            raise AccountIsNoneError(f"Error: the checking account with id={account_id}, have not been initated yet", "balance_checking")
    
    def transfer(self,file ,  account_id,saving_account , amount):
        message = saving_account.withdraw(file,account_id, amount) +"\n"
        message += self.deposit(file,account_id , amount)
        return  message
    

        
        
    def get_current_checking_balance(self,file,account_id):
        current_checking_balance= file.get_field_info(account_id, "balance_checking")
        return current_checking_balance
        
    def check_if_account_exist(self,file ,account_id):
        current_balance = self.get_current_checking_balance(file,account_id)
        if str(current_balance).lower() == "none":
            return False
        else:
            return True



        
        