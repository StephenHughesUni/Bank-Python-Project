"""
Stephen Hughes - D21126653
Bank Account
Login, Create, Logout, Checks age, Checks Name, Opens Checking Account if Age, Opens Saving Account one withdraw a month
Deposits to either account even if two accounts open under one Name
Withdraw from any account created under one Name
Transfer to any bank account, across any name
Print Transaction from account under one Name
Delete account under one Name
Log Out

Will save details on logout.
"""


class Customer:  # my customer class
    def __init__(self, name, age):  # contains name and age
        self.name = name
        self.age = age
        self.accounts = []  # initialize the accounts list

    def addAccount(self, account):  # add account method - using account
        self.accounts.append(account)  # append the account info to accounts in customer class

    def __str__(self):  # Promoting for Name and Age when creating an account.
        return "Name: " + self.name + " Age: " + str(self.age)

    def info(self):  # Converting info into strings and adding them to account, also adding account number to it.
        string = self.name + "," + str(self.age) + "," + str(len(self.accounts))
        for account in self.accounts:
            string += "," + str(account.accNo)
        return string


class Account:  # Account class
    def __init__(self, accNo, type):  # Declaring account number and type of account
        self.balance = 0  # Starting balance will be 0
        self.accNo = accNo
        self.type = type

    def __int__(self):
        self.balance = 0  # Setting balance to 0
        self.accNo = 0  # Setting account number to 0
        self.type = ""  # Setting account type to empty string until selected.

    def deposit(self, amt):  # Deposit Method within account class
        if amt > 0:  # Once amt ( entered from user ) is above 0 then begin rest of code
            self.balance += amt  # Add (entered amt from user ) to self.balance in account
            print(str(amt) + " has been deposited")  # Prompt user
            return "Deposit of " + str(amt) + " Successful: New Balance: $" + str(self.balance)  # Show new balance
        else:  # Otherwise when its below 0, explain its invalid and allow for re-entry.
            print("Invalid amount")
            return ""

    def transfer(self, amt, account):  # Transfer Method
        if amt > 0:  # If amt ( entered from user ) is above 0 then begin rest of code
            if self.balance >= amt:  # Once balance is above ( entered from user )
                self.balance -= amt  # Take the amount from user from balance
                account.deposit(amt)  # Call deposit for amount entered
                print("Transfer Complete")  # Transfer completed
                return "Transfer of " + str(amt) + " Successful: New Balance: $" + str(self.balance)  # Update prompt
            else:
                print("Insufficient funds")  # If balance is not above or equal to amount entered then insufficient
        else:
            print("Invalid amount")  # If less than entry from user is less than 0 then insufficient

        return ""

    def withdraw(self, amt):  # Withdraw Method
        if amt > 0:  # If user amount is over 0 then continue
            if self.balance >= amt:  # if balance is greater or = to amount entered then continue
                self.balance -= amt  # take amount entered from balance
                print("Withdrawal Successful")  # withdraw prompt
                return "Withdrawl of " + str(amt) + " Successful: New Balance: $" + str(self.balance)  # Update prompt
            else:  # Otherwise
                print("Insufficient funds")  # if balance is not greater or = to amount entered then insufficient
                return ""

    def __str__(self):
        return "Type: " + self.type + " Balance: " + str(self.balance)

    def info(self):
        return self.type + "," + str(self.accNo) + "," + str(self.balance)


class CheckingAccount(Account):  # Checking account, inheriting Account
    def __init__(self, accNo, limit):  # Contains accNo and Limit
        super().__init__(accNo, "Checking")  # accNo will be set to type Checking using super
        self.limit = limit  # Declaring self limit

    def setup(self, string):  # Splitting the information from Accounts on "," and using index for elements
        info = string.split(",")
        self.accNo = int(info[1])
        self.balance = float(info[2])
        self.limit = float(info[3])

    def info(self):
        return super().info() + "," + str(self.limit)  # Displaying info including the ","

    def transfer(self, amt, account):  # Similar to previous transfer but now within checking account with limit
        if amt > 0:
            if self.balance >= (amt + self.limit):
                self.balance -= amt
                account.deposit(amt)
                print("Transfer Complete")
                return "Transfer of " + str(amt) + " Successful: New Balance: $" + str(self.balance)
            else:
                print("Insufficient funds")
        else:
            print("Invalid amount")

        return ""

    def withdraw(self, amt):  # Similar to previous withdraw but with limit
        if amt > 0:
            if self.balance >= (amt + self.limit):
                self.balance -= amt
                print("Withdrawal Successful")
                return "Withdrawal of " + str(amt) + " Successful: New Balance: $" + str(self.balance)
            else:
                print("Insufficient funds")
                return ""


class SavingsAccount(Account):  # Saving account, inheriting Account
    def __init__(self, accNo):  # Contains accNo
        try:
            if "," in accNo:  # If there is still elements with , it will check and split them.
                super().__init__(0, "Savings")
                info = accNo.split(",")
                self.accNo = int(info[1])  # splitting and assigning element to index
                self.balance = float(info[2])  # same
            else:
                super().__init__(accNo, "Savings")  # Setting the account number and type
                self.withdrawn = False
        except:
            super().__init__(accNo, "Savings")
            self.withdrawn = False

    def withdraw(self, amt):  # Withdraw method
        if not self.withdrawn:  # Once its not done then withdraw can preform
            res = super().withdraw(amt)
            if res != "":
                self.withdrawn = True  # set withdraw to true so if they try again will be once a month
            return res
        else:
            print("You can only withdraw or transfer funds once a month with a Savings account")

    def transfer(self, amt, account):  # Same as above for transfer
        if not self.withdrawn:
            res = super().transfer(amt, account)
            if res != "":
                self.withdrawn = True
            return res
        else:
            print("You can only withdraw or transfer funds once a month with a Savings account")


customers = []  # Initializing customer list
accounts = []  # Initializing accounts list
transactions = []  # Initializing transactions list
maxAccNo = 0  # Initializing max account number


def readAccounts():
    global maxAccNo
    file = open("accounts.txt", "r")
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        if "Checking" in line:
            ac = CheckingAccount(0, 0)
            ac.setup(line)
            accounts.append(ac)
            if ac.accNo > maxAccNo:
                maxAccNo = ac.accNo + 1
        else:
            ac = SavingsAccount(line)
            accounts.append(ac)
            if ac.accNo > maxAccNo:
                maxAccNo = ac.accNo + 1


def readTransactions():
    file = open("transactions.txt", "r")
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        transactions.append(line)


def readCustomers():
    file = open("customers.txt", "r")
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        info = line.split(",")
        c = Customer(info[0], int(info[1]))
        count = int(info[2])
        curr = 3
        for i in range(count):
            accNo = int(info[curr])
            for ac in accounts:
                if ac.accNo == accNo:
                    c.addAccount(ac)
                    break

            curr += 1
        customers.append(c)


def writeAccounts():
    file = open("accounts.txt", "w")

    for account in accounts:
        file.write(account.info() + "\n")

    file.close()


def writeTransactions():
    file = open("transactions.txt", "w")

    for transaction in transactions:
        file.write(transaction + "\n")

    file.close()


def writeCustomers():
    file = open("customers.txt", "w")

    for customer in customers:
        file.write(customer.info() + "\n")

    file.close()


def selectAccount(accounts, prompt):
    if len(accounts) == 0:
        print("No accounts available")
        return None
    index = 1
    for ac in accounts:
        print(str(index) + ". " + str(ac))
        index += 1
    choice = int(input(prompt)) - 1
    if choice < 0 or choice >= len(customer.accounts):
        print("Invalid choice")
        return None
    else:
        return customer.accounts[choice]


done = False
print("\n")
print("*" * 25)
print("* Bank Account Creator  *\n*************************")
readAccounts()
readTransactions()
readCustomers()
while not done:

    # Menu and Choices
    choice = input("*\t1. Log in\t\t\t*\n*\t2. Create account\t*\n*\t3. Exit\t\t\t\t*\n*************************"
                   "\t\nEnter choice: ")
    # Choice 1 of Logging in
    if choice == "1":
        name = input("Enter name of the account: ")
        for customer in customers:
            if customer.name == name:
                print("*" * 25, "\n* \tLogged In\t\t\t*\n*************************")
                while not done:
                    choice = input("1. Open Checking Account\n2. Open Savings Account\n3. Deposit\n4. Withdraw\n"
                                   "5. Transfer funds\n6. Print Transactions\n7. Delete account\n8. Log out\nEnter "
                                   "choice: ")
                    # Opening checking account + verify age - then appends information.
                    if choice == "1":
                        if customer.age < 18:
                            print("You are too young to open a Checking Account")
                        else:
                            ac = CheckingAccount(maxAccNo, 100)
                            customer.addAccount(ac)
                            accounts.append(ac)
                            maxAccNo += 13
                            print("Checking Account Added")
                    # Savings account + verify age - then appends information.
                    elif choice == "2":
                        if customer.age < 14:
                            print("You are too young to open a Savings Account")
                        else:
                            ac = SavingsAccount(maxAccNo)
                            customer.addAccount(ac)
                            accounts.append(ac)
                            maxAccNo += 13
                            print("Savings Account Added")
                    # Deposit choice - select an account, once ac is not empty, use deposit on res with the amount
                    # entered from user then append res to transactions
                    elif choice == "3":
                        try:
                            amt = int(input("Enter the amount to deposit: "))
                            ac = selectAccount(customer.accounts, "Select Account: ")
                            if ac is not None:
                                res = ac.deposit(amt)
                                if res != "":
                                    res = "TRX:" + str(len(transactions) + 1) + "-" + str(ac.accNo) + "-: " + res
                                    transactions.append(res)
                        except:
                            print("Invalid input")
                    # Similar to deposit but withdrawn instead
                    elif choice == "4":
                        try:
                            amt = int(input("Enter the amount to withdraw: "))
                            ac = selectAccount(customer.accounts, "Select Account: ")
                            if ac is not None:
                                res = ac.withdraw(amt)
                                if res != "":
                                    res = "TRX" + str(len(transactions) + 1) + "-" + str(ac.accNo) + "-: " + res
                                    transactions.append(res)
                        except:
                            print("Invalid input")
                    # Transfer from one account to second account, can transfer to other users bank accounts
                    elif choice == "5":
                        try:
                            amt = int(input("Enter the amount to transfer: "))
                            ac = selectAccount(customer.accounts, "Select first Account: ")
                            if ac is not None:
                                ac2 = selectAccount(accounts, "Select second account: ")
                                if ac2 is not None:
                                    res = ac.transfer(amt, ac2)
                                    if res != "":
                                        res = "TRX" + str(len(transactions) + 1) + "-" + str(ac.accNo) + "-: " + res
                                        transactions.append(res)
                        except:
                            print("Invalid input")
                    # Will print transactions based on customer logged in and their transaction.txt file
                    elif choice == "6":
                        try:
                            ac = selectAccount(customer.accounts, "Select account: ")
                            if ac is not None:
                                for transaction in transactions:
                                    if "-" + str(ac.accNo) in transaction:
                                        print(transaction)
                        except:
                            print("Invalid input")
                    # Deletes everything from the customer logged in at the time
                    elif choice == "7":
                        customers.remove(customer)
                        done = True
                    # Logout
                    elif choice == "8":
                        done = True
                    else:
                        print("Invalid choice")
                done = False
                break
    # Create an account choice
    elif choice == "2":
        name = input("Enter name: ")
        try:
            age = int(input("Enter the age: "))
            c = Customer(name, age)
            exists = False
            # Checks if user already exisits based on name
            for customer in customers:
                if c.name == customer.name:
                    print("Account already exists")
                    exists = True
                    break
            # If not then will append information
            if not exists:
                customers.append(c)
                print("\n* \tAccount Created\t\t*\n*************************")
        except:

            print("Invalid input")
    # Writes all of the information to txt files once logged out, end of session.
    elif choice == "3":
        writeAccounts()
        writeCustomers()
        writeTransactions()
        print("Goodbye")
        done = True
    else:
        print("Invalid choice")
