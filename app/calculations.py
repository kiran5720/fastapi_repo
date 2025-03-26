def add(num:int,num2:2):
    return num+num2


class Bankaccount:
    def __init__(self,initial_balance = 0):
        self.balance = initial_balance
        pass
    def balance(self):
        return self.balance
    def deposite(self,depositee):
        self.balance = depositee+self.balance
    def withdraw(self,amount):
        if amount>self.balance:
            raise Exception("insufficient fund")
        self.balance = self.balance-amount
        return amount
    