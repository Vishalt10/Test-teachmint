#!/usr/bin/env python
# coding: utf-8

# In[1]:


class User:
    def __init__(self, user_id, name, email, mobile_number):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.mobile_number = mobile_number


class Spend:
    def __init__(self, expense_id, payer, amount, expense_type, splits):
        self.expense_id = expense_id
        self.payer = payer
        self.amount = amount
        self.expense_type = expense_type
        self.splits = splits

class Splitwise:
    def __init__(self):
        self.users = {} 
        self.expenses = []  

    def add_user(self, user_id, name, email, mobile_number):
        user = User(user_id, name, email, mobile_number)
        self.users[user_id] = user

    def add_expense(self, expense_id, payer_id, amount, expense_type, splits):
        expense = Spend(expense_id, self.users[payer_id], amount, expense_type, splits)
        self.expenses.append(expense)

    def calculate_balances(self):
        balances = {}
        for user_id in self.users:
            balances[user_id] = 0
        
        for expense in self.expenses:
            if expense.expense_type == "EQUAL":
                share = expense.amount / len(self.users)
                for user_id in self.users:
                    if user_id != expense.payer.user_id:
                        balances[user_id] += share
                        balances[expense.payer.user_id] -= share
            elif expense.expense_type == "EXACT":
                for user_id, share in expense.splits.items():
                    balances[user_id] += share
                    balances[expense.payer.user_id] -= share
            elif expense.expense_type == "PERCENT":
                total_percent = sum(expense.splits.values())
                if total_percent != 100:
                    raise ValueError("Total percentage shares must be 100.")
                
                for user_id, percent_share in expense.splits.items():
                    share = (percent_share / 100) * expense.amount
                    balances[user_id] += share
                    balances[expense.payer.user_id] -= share

        balances = {user_id: round(balance, 2) for user_id, balance in balances.items() if balance != 0}

        return balances


# In[2]:


## Initialization of users and function testing
split=Splitwise()
print("Hello welcome to splitwise!!!")
print('\n')
print("Request few details to details to get started!!!")
print('\n')
print("Enter the 4 user details")

for i in range(4):
    uid=input("Enter the user id: ")
    name=input("Enter the name of user: ")
    email=input("Enter the email id of the user: ")
    contact=input("Enter the contact number of user: ")
    split.add_user(uid, name, email, contact)
    print("user added successfully")
    print("\n")

expense_type=['EQUAL', 'EXACT', 'PERCENT']

expense_kind=input("Enter the expense type: ")
if expense_kind not in expense_type:
    print("Invalid operation, kindly re-enter: ")

eid= input("Enter expense id: ")
uid= input("Enter user id: ")
amount=int(input("Enter the amount"))
    
if expense_kind=='EQUAL':
    splits=[]
    split.add_expense(eid, uid, amount, expense_kind, splits)
    balances = split.calculate_balances()
    for user_id, balance in balances.items():
        print(f"{split.users[user_id].name} owes {split.users['u1'].name}: Rs {balance}")
elif expense_kind=='EXACT':
    splits={}
    no=int(input("Enter number of users under this category: "))
    for i in range(no):
        split_id=input("Enter user id : ")
        split_amount=float(input("Enter the amount: "))
        splits[split_id]=split_amount
    split.add_expense(eid, uid, amount, expense_kind, splits)
    balances = split.calculate_balances()
    for user_id, balance in balances.items():
        print(f"{split.users[user_id].name} owes {split.users['u1'].name}: Rs {balance}")
elif expense_kind=='PERCENT':
    splits={}
    no=int(input("Enter number of users under this category: "))
    for i in range(no):
        split_id=input("Enter user id : ")
        split_amount=float(input("Enter the percentage share: "))
        splits[split_id]=split_amount
    if sum(splits.values())!=100:
        print("Percentage should be equal to 100")
    split.add_expense(eid, uid, amount, expense_kind, splits)
    balances = split.calculate_balances()
    for user_id, balance in balances.items():
        print(f"{split.users[user_id].name} owes {split.users['u1'].name}: Rs {balance}")

