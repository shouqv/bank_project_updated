# Bank System Project (Updated)


## Description

This project is an updated and extended version of my original [Python-based bank system](https://github.com/shouqv/Bank-project).
It was built with a focus on Test-Driven Development (TDD), modular design, and simulating real-world banking workflows.


In addition to the core features (customer management, deposits, withdrawals, transfers), this version introduces several new enhancements, including:

- Transaction history with detailed logging and indexing

- Password strength validation for secure customer accounts

- Custom overdraft limits with account deactivation rules

- Automated account statement reports (.txt format)

- Random bonus system for lowest balances

## Features
- **Add New Customer**  
  - Can create a checking account, savings account, both, or neither  
  - Account ID is automatically generated 
  - Now includes password strength validation.


- **Withdraw Money** (requires login)  
  - From checking or savings accounts  
  - Checking accounts adhere to overdraft rules  
  - Savings accounts do not allow overdrafts  

- **Deposit Money** (requires login)  
  - Into checking or savings accounts  

- **Transfer Money** (requires login)  
  - Between own accounts  
  - To other customers’ accounts  

- **Overdraft Protection**  
  - $35 fee for overdraft  
  - Prevents account balance from going below a set limit (default -100 or custom per customer).
  - Account deactivation after 2 successful overdrafts  
  - Reactivation after clearing overdraft and fees  

- **Transaction History**
  - All customer operations are stored in transaction.csv.
  - Can list all transactions for a customer.
  - View detailed information about a single transaction.
  - Displays timestamp, type of operation, and resulting balance.

- **Account Statement Report**
  - Generates a text report (```customer{account_id}_statement.txt```).
  - Includes balances and customer's transactions.

- **Top 3 Customer Reward**
  - Identifies the three customers with the lowest combined balances.
  - Randomly selects one to receive a $100 bonus in their checking account.
  - Outputs all three customers and the winner’s information (name + ID) to the terminal.


## File Structure
```
Banking-With-Python/
│
├── bank/                   # Core banking logic
│ ├── customer.py
│ ├── checking_account.py
│ ├── saving_account.py
│ ├── file_management.py
│ ├── transactions.py
│ └── custome_exceptions.py
|
├── data/
│ ├── bank.csv              # Stores customer data
│ └── transaction.csv       # Stores customer transactions
|
├── test/                   # Unit tests (TDD approach)
│ ├── test_checking_account.py
│ ├── test_customer.py
│ ├── test_file_management.py
│ └── test_saving_account.py
|
├── main.py                 # Main user interface
└── README.md

```

# What I Learned

- How to design and implement a project using Test-Driven Development (TDD) from the ground up.

- The importance of modularity, by separating concerns into classes (Customer, CheckingAccount, SavingAccount, FileManagement, Transaction).

- How to implement custom exceptions to handle domain-specific errors gracefully.

- Practical experience with file I/O, CSV data persistence, and input validation.

- Building a CLI banking system that feels close to real-world workflows.

- Extending core functionality with security features (password validation), data tracking (transaction history), reporting (account statements), and reward logic (top 3 customer system).