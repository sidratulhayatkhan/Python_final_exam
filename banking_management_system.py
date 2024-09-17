 
class User:
    def __init__(self,name,email,address,account_type,account_number):
        self.__name=name
        self.__email=email
        self.__address=address
        self.__account_type=account_type
        self.__account_number=account_number
        self.__balance=0
        self.__transaction_history=[]
        self.__loan_count=0

    def get_name(self):
        return self.__name
    
    def get_balance(self):
        return self.__balance
    
    def deposit(self,amount):
        self.__balance+=amount
        self.__transaction_history.append(f"deposit{amount}")
        print(f"deposited {amount}. New Balance {self.__balance}")

    def withdraw(self,amount):
        if amount> self.__balance:
            print(f"Withdrawal Balance Exceeded.")
        else:
            self.__balance-=amount
            self.__transaction_history.append(f"withdraw: {amount}")
            print(f"Withdraw amount {amount}. New Balance:{self.__balance}")

    def transfer(self,bank,to_account,amount):
        users=bank._get_users()
        if to_account not in users:
            print(f"Account {to_account} does not exist.")
        elif amount>self.__balance:
            print(f"Insuficient Balance")
        else:
            self.__balance-=amount
            users[to_account].deposit(amount)
            self.__transaction_history.append(f"{amount} transfer to{to_account}")
            print(f"Transfered {amount} to {to_account}. New Balance is {self.__balance}")

    def take_loan(self,bank,amount):
        if bank._Bank__is_loan_allowed() and self.__loan_count <2:
            self.__balance+=amount
            self.__loan_count+=1
            self.__transaction_history.append(f"loan:{amount}")
            print(f"loan {amount} taken. New Balance is {self.__balance}")
        else:
            print(f"Loan not allowed at this moment")

    def view_transaction_history(self):
        print(f"Transaction history for {self.__name}")
        for transaction in self.__transaction_history:
            print(transaction)


class Bank:
    def __init__(self):
        self.__users={}
        self.__total_balance=0
        self.__total_loan=0
        self.__loan_status=True

    def create_account(self,name,email,address,account_type):
        account_number=len(self.__users)+1
        new_user=User(name,email,address,account_type,account_number)
        self.__users[account_number]=new_user
        print(f"Account created for {name},Account Number:{account_number}")

    def delete_account(self,account_number):
        if account_number in self.__users:
            del self.__users[account_number]
            print(f"Account {account_number} deleted")
        else:
            print(f"Account {account_number} does not exist")

    def show_all_users(self):
        if not self.__users:
            print(f"No Users Available")
        else:
            for account_number,user in self.__users.items():
                print(f"Account Number:{account_number}, Name:{user.get_name()}, Balance:{user.get_balance()}.")
    
    def total_bank_balance(self):
        total_balance=sum(user.get_balance() for user in self.__users.values())
        print(f"Total Bank Balance:{total_balance}")

    def total_loan_amount(self):
        total_loan = sum(user._User__transaction_history.count(f"loan: {amount}") * amount for user in self.__users.values() for amount in range(1000))
        print(f"Total Loan Amount: {total_loan}")


    def toggle_loan(self,status):
        self.__loan_status=status
        print(f"Loan Status{'On' if self.__loan_status else 'Off'}")

    def __is_loan_allowed(self):
        return self.__loan_status
    
    def _get_users(self):
        return self.__users
    

class Admin:
    def __init__(self,bank):
        self.__bank=bank

    def create_user_account(self,name,email,address,account_type):
        self.__bank.create_account(name,email,address,account_type)

    def delete_user_account(self,account_number):
        self.__bank.delete_account(account_number)

    def show_users(self):
        self.__bank.show_all_users()

    def check_total_balance(self):
        self.__bank.total_bank_balance()

    def check_total_loan(self):
        self.__bank.total_loan_amount()

    def set_loan_status(self,status):
        self.__bank.toggle_loan(status)

    
bank= Bank()
admin= Admin(bank)

admin.create_user_account("Rahim", "rahim@gmail.com", "Rahimganj", "Savings")
admin.create_user_account("Karim", "karim@gmail.com", "karimganj", "Current")

user1 = bank._get_users()[1]
user2 = bank._get_users()[2]

user1.deposit(1000)
user1.withdraw(300)
user1.transfer(bank, 2, 200)

user2.deposit(500)
user2.take_loan(bank, 1000)

admin.show_users()
admin.check_total_balance()
admin.check_total_loan()
admin.set_loan_status(False)

user1.view_transaction_history()
user2.view_transaction_history()

    





