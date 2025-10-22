import pytest
from app.calculations import add,Bankaccount

@pytest.fixture
def zero_balance():
    return Bankaccount()

@pytest.fixture
def bank_balance():
    return Bankaccount(50)

@pytest.mark.parametrize("num1,num2,expected",[
    (4,5,9),
    (5,6,11),
    (7,3,10)
])
def test_add(num1,num2,expected):
    print("checking assertion")
    assert add(num1,num2) == expected
    

def test_bank_balance():
    bank_balance = Bankaccount()
    assert bank_balance.balance == 0

def test_withdraw():
    bank = Bankaccount(50)
    withdraw = bank.withdraw(20)
    assert  bank.balance == 30 


@pytest.mark.parametrize("deposite,withdraw,expected",[
    (100,50,50),
    (200,100,100)
])
def test_bank_fixturees(zero_balance,deposite,withdraw,expected):
    zero_balance.deposite(deposite)
    zero_balance.withdraw(withdraw)
    assert zero_balance.balance == expected 
