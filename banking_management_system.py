 
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

    
def main():
    bank= Bank()
    admin= Admin(bank)

    while True:
        print("\nWelcome to the banking system")
        print("1.Create Account")
        print("2.Delete Account")
        print("3.Deposit")
        print("4.Withdraw")
        print("5.Transfer")
        print("6.Take loan")
        print("7.View all users")
        print("8.Check total bank balance")
        print("9.Check total loan amount")
        print("10.Toggle loan status")
        print("11.View Transaction history")
        print("12.Exit")
        
        choice = input("Please select an option (1-12): ")

        if choice == '1':
            name = input("Enter name: ")
            email = input("Enter email: ")
            address = input("Enter address: ")
            account_type = input("Enter account type (Savings/Current): ")
            admin.create_user_account(name, email, address, account_type)

        elif choice == '2':
            account_number = int(input("Enter account number to delete: "))
            admin.delete_user_account(account_number)

        elif choice == '3':
            account_number = int(input("Enter account number to deposit into: "))
            amount = float(input("Enter amount to deposit: "))
            if account_number in bank._get_users():
                bank._get_users()[account_number].deposit(amount)
            else:
                print(f"Account {account_number} does not exist.")

        elif choice == '4':
            account_number = int(input("Enter account number to withdraw from: "))
            amount = float(input("Enter amount to withdraw: "))
            if account_number in bank._get_users():
                bank._get_users()[account_number].withdraw(amount)
            else:
                print(f"Account {account_number} does not exist.")
        elif choice == '5':
            from_account = int(input("Enter your account number: "))
            to_account = int(input("Enter account number to transfer to: "))
            amount = float(input("Enter amount to transfer: "))
            if from_account in bank._get_users():
                bank._get_users()[from_account].transfer(bank, to_account, amount)
            else:
                print(f"Account {from_account} does not exist.")

        elif choice == '6':
            account_number = int(input("Enter account number to take loan: "))
            amount = float(input("Enter loan amount: "))
            if account_number in bank._get_users():
                bank._get_users()[account_number].take_loan(bank, amount)
            else:
                print(f"Account {account_number} does not exist.")

        elif choice == '7':
            admin.show_users()

        elif choice == '8':
            admin.check_total_balance()

        elif choice == '9':
            admin.check_total_loan()

        elif choice == '10':
            status = input("Enter loan status (On/Off): ").strip().lower() == 'on'
            admin.set_loan_status(status)

        elif choice == '11':
            account_number = int(input("Enter account number to view history: "))
            if account_number in bank._get_users():
                bank._get_users()[account_number].view_transaction_history()
            else:
                print(f"Account {account_number} does not exist.")

        elif choice == '12':
            print("Exiting the system.")
            break

        else:
            print("Invalid choice, please select a valid option.")

main()

    





