from bank.customer import Customer
import bank.custome_exceptions as exceptions

try:
    customer = Customer("data/bank.csv")
    print("welcome to the bank")

    while True:
        print("1) Add customer  2) Login 3) Bless a customer 4) Exit")
        choice = input("Choice: ")
        try:
            match choice:
                case "1":

                    account_id = customer.customer_generated_id()
                    print(f"The account id is: {account_id}")
                    first_name = input("Enter first name: ")
                    last_name = input("Enter last name: ")
                    while True:
                        try:
                            password = input("Enter your password: ")
                            customer.password_checcker(password)
                            break
                        except ValueError as e:
                            print(e)

                    print("Type None if you don’t want to create any of the below accounts")
                    balance_checking = customer.customer_entered_numbers(input("Checking account balance: "),"Please ensure to enter a valid checking balance")
                    balance_savings = customer.customer_entered_numbers(input("Saving account balance: "),"Please ensure to enter a valid saving balance")
                    overdraft_limit = input("Enter the overdraft limit (to use the default value -100 , just press Enter): ")
                    customer.add_new_customer( account_id,first_name, last_name, password, balance_checking, balance_savings,overdraft_limit)
                    print("Customer added successfully.")
                    print(f"Welcome {customer.customer_greetings(account_id)}")



                case "2":
                    account_id = customer.customer_entered_numbers(input("Account ID: "),"Invalid ID, please enter a number","int")
                    password = input("password: ")

                    if customer.login(account_id,password):
                        print(f"Welcome {customer.customer_greetings(account_id)}")
                        while True:
                            try:
                                print("1) Withdraw  2) Deposit 3) Transfer 4) Change overdraft limit 5) Generate report 6) Logout")
                                selection = input("Choice: ")
                                match selection:
                                    case "1":
                                        account = input("Withdraw from (checking/saving): ").strip().lower()
                                        print(f"The current {account} balance: {customer.get_current_balance(account_id , account)}")
                                        amount = customer.customer_entered_numbers(input("Amount: "),"Invalid ammount, please enter a number")
                                        print(customer.withdraw(account_id, account , amount)) 


                                    case "2":
                                        account = input("Deposite to (checking/saving): ").strip().lower()
                                        print(f"The current {account} balance: {customer.get_current_balance(account_id , account)}")
                                        amount = customer.customer_entered_numbers(input("Amount: "),"Invalid ammount, please enter a number")              
                                        print(customer.deposit(account_id, account , amount))


                                    case "3":
                                            print("a) Transfer from checking to saving")
                                            print("b) Transfer from saving to checking")
                                            print("c) Transfer to another customer account")
                                            print()
                                            print(f"The current checking balance: {customer.get_current_balance(account_id , "checking")}")
                                            print(f"The current saving balance: {customer.get_current_balance(account_id , "saving")}")
                                            print()                           
                                            choice = input("Choice: ").lower()
                                            if choice == "c":
                                                from_account = input("Transfer from (checking/saving): ").strip().lower() #just personal preference, he chooses the account then the ammount                                   
                                            amount = customer.customer_entered_numbers(input("Amount: "),"Invalid ammount, please enter a number")


                                            if choice == "c":
                                                other_customer = customer.customer_entered_numbers(input("Enter the account ID to transfer to: "),"Invalid ID, please enter a number","int")
                                                print(customer.transfer(account_id, choice, amount, from_account=from_account, other_customer=other_customer))
                                                print(f"Transferred {amount} from {from_account} to customer {other_customer}")
                                            else:
                                                print(customer.transfer(account_id, choice, amount))
                                                print("Transfer completed successfully.")
                                    case "4":
                                        overdraft_limit = customer.customer_entered_numbers(input("Enter the new overdraft limit: "),"Please ensure to enter a valid number")
                                        customer.file_manager.update_row(account_id,"overdraft_limit",overdraft_limit)
                                    case "5":
                                        customer.customer_report(account_id)
                                        print(f"The report customer{account_id}_statement.txt created successfuly")
                                    case "6":
                                        break
                                    case _:
                                        print("Invalid choice")
                            except ValueError as e:
                                    print(e)
                            except exceptions.InactiveAccountError as e:
                                print(e)
                            except exceptions.AccountIsNoneError as e:
                                print(e)
                                if e.account_name:
                                    answer = input(f"You dont have a {e.account_name}, do you wish to create one? (yes/no) ").lower()
                                    if answer == "yes":
                                        inital_balance = customer.customer_entered_numbers(input("Enter the new account balance: "),"Invalid ammount, please enter a number")
                                        customer.create_account(account_id , e.account_name,inital_balance)
                            except exceptions.OverdraftRejectedError as e:
                                print(e)
                            except exceptions.OverdraftLimitExceededError as e:
                                print(e)
                            except exceptions.CustomerNotFoundError as e:
                                print(e)
                            except exceptions.InvalidChoiceError as e:
                                print(e)

                    else:
                        print("Password incorrect!")
                case "3":
                    print(customer.least_3_customer_reward())
                case "4":
                    break
                case _:
                    print("invalid option")
        except ValueError as e:
            print(e)
        except exceptions.CustomerNotFoundError as e:
            print(e)   
except ValueError as e:
    print(e)