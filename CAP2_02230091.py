import os
import json
import random

class Account:   #The Account class represents a bank account with methods for depositing and withdrawing money, and checking the balance.
    def __init__(self, account_number, password, account_type, balance=0):
        self.account_number = account_number
        self.password = password
        self.account_type = account_type
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance < amount:
            print("Insufficient funds!")
            return
        self.balance -= amount

    def check_balance(self):
        return self.balance

class Bank:  #The Bank class represents the bank. It maintains a dictionary of accounts, which is loaded from a file when the bank is created and saved back to the file whenever an account is created or modified. The bank has methods for creating accounts and logging in.
    def __init__(self, filename="accounts.txt"):
        self.filename = filename
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.accounts = json.load(f)
        else:
            self.accounts = {}

    def create_account(self, account_type):
        account_number = str(random.randint(10000, 99999))
        password = str(random.randint(1000, 9999))
        self.accounts[account_number] = {
            'password': password,
            'account_type': account_type,
            'balance': 0
        }
        self.save_accounts()
        print(f"Account created! Your account number is {account_number} and your password is {password}.")

    def login(self, account_number, password):
        if account_number in self.accounts and self.accounts[account_number]['password'] == password:
            return Account(account_number, password, self.accounts[account_number]['account_type'], self.accounts[account_number]['balance'])
        else:
            print("Invalid account number or password!")
            return None

    def save_accounts(self):
        with open(self.filename, 'w') as f:
            json.dump(self.accounts, f)

bank = Bank()
while True:
    print("1. Create account")
    print("2. Login")
    print("3. Exit")
    choice = input("Choose an option: ")
    if choice == '1':
        account_type = input("Enter account type (savings/current): ")
        bank.create_account(account_type)
    elif choice == '2':
        account_number = input("Enter account number: ")
        password = input("Enter password: ")
        account = bank.login(account_number, password)
        if account:
            while True:
                print("1. Check balance")
                print("2. Deposit money")
                print("3. Withdraw money")
                print("4. Logout")
                choice = input("Choose an option: ")
                if choice == '1':
                    print(f"Your balance is {account.check_balance()}.")
                elif choice == '2':
                    amount = float(input("Enter amount to deposit: "))
                    account.deposit(amount)
                    bank.accounts[account.account_number]['balance'] = account.balance
                    bank.save_accounts()
                    print(f"Deposited {amount}. Your new balance is {account.check_balance()}.")
                elif choice == '3':
                    amount = float(input("Enter amount to withdraw: "))
                    account.withdraw(amount)
                    bank.accounts[account.account_number]['balance'] = account.balance
                    bank.save_accounts()
                    print(f"Withdrew {amount}. Your new balance is {account.check_balance()}.")
                elif choice == '4':
                    break
    elif choice == '3':
        break
