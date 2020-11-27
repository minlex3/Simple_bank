import random
import sqlite3

connect = sqlite3.connect('card.s3db')
cursor = connect.cursor()

# cursor.execute("DROP TABLE card")
cursor.execute("CREATE TABLE if not exists card (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")
connect.commit()

class Card():
    def __init__(self):
        self.number = None
        self.pin = None
        self.balance = None
    
    def create(self):
        number ='400000' + ''.join(str(random.randrange(9)) for _ in range(9))
        self.number = number + str(luna(number,0))
        self.pin = ''.join(str(random.randrange(10)) for _ in range(4))
        self.balance = 0
        print('\nYour card has been created\nYour card number:\n{}\nYou card PIN:\n{}\n'.format(self.number, self.pin))

        cursor.execute("INSERT INTO card (number, pin, balance) VALUES (?, ?, ?);",
                       (self.number, self.pin, self.balance))
        connect.commit()

    def login(self, number, pin):
        self.number = number
        self.pin = database(number)
        if self.pin != 0:
            if self.pin == int(pin):
                cursor.execute("SELECT balance FROM card WHERE number = (?)", [(self.number)])
                balance = cursor.fetchone()
                self.balance = balance[0]
                print('\nYou have successfully logged in!\n')
                return 1
            else:
                print('\nWrong card number or PIN!\n')
                return 0
        else:
            print('\nWrong card number or PIN!\n')
            return 0
        
    def check(self):
        print('\nBalance: {}\n'.format(self.balance))

    def income(self, cost):
        self.balance += int(cost)
        cursor.execute("UPDATE card SET balance = ? WHERE number = ?", [self.balance, self.number])
        connect.commit()
        print('Income was added!\n')

    def do_transfer(self):
        number_recipient = input('Enter card number:\n')
        if luna(number_recipient, 1):
            if database(number_recipient):
                money = int(input('Enter how much money you want to transfer:\n'))
                if money <= self.balance:
                    self.balance -= money
                    cursor.execute("UPDATE card SET balance = ? WHERE number = ?", [self.balance, self.number])
                    connect.commit()
                    cursor.execute("SELECT balance FROM card WHERE number = ?", [(number_recipient)])
                    db_bal = cursor.fetchone()
                    new_balance = int(db_bal[0]) + money
                    cursor.execute("UPDATE card SET balance = ? WHERE number = ?", [new_balance, number_recipient])
                    connect.commit()
                    print('Success!\n')
                else:
                    print('Not enough money!\n')
            else:
                print('Such a card does not exist.\n')
        else:
            print('Probably you made a mistake in the card number. Please try again!\n')

    def delete(self):
        cursor.execute("DELETE FROM card WHERE number = ?", [(self.number)])
        connect.commit()
        print('\nThe account has been closed!\n')

def luna(number, mode):  # mode=0 -> search check sum. mode=1 -> check
    s, odd = 0, 1
    if mode == 1:
        check = int(number) % 10
        num_var = int(number) // 10
        number = str(num_var)
    for char in number:
        n = int(char)
        if odd % 2 == 1:
            n *= 2
        if n > 9:
            n -= 9
        odd += 1
        s += n
    if s % 10 != 0:
        check_sum = 10 - (s % 10)
    else:
        check_sum = 0
    if mode == 0:
        return check_sum
    else:
        if check == check_sum:
            return True
        else:
            print('\nProbably you made a mistake in the card number. Please try again!\n')
            return False

def database(number):
    cursor.execute("SELECT pin FROM card WHERE number = (?)", [(number)])
    db_pin = cursor.fetchone()
    if db_pin is None:
        print('\nSuch a card does not exist.\n')
        return 0
    else:
        return int(db_pin[0])

print('1. Create an account\n2. Log into account\n0. Exit')
login = 0
command = int(input())

while command != 0:
    # Create card
    if command == 1 and login == 0:
        card = Card()
        card.create()
    # Balance
    if command == 1 and login == 1:
        card.check()
    # Login
    if command == 2 and login == 0:
        command = -1
        number = input('\nEnter your card number:\n')
        pin = input('Enter your PIN:\n')
        login = card.login(number, pin)
    # Add income
    if command == 2 and login == 1:
        cost = input('\nEnter income:\n')
        card.income(cost)
    # Do transfer
    if command == 3 and login == 1:
        print('\nTransfer')
        card.do_transfer()
    # Delete
    if command == 4 and login == 1:
        card.delete()
        login = 0
    # Log out
    if command == 5 and login == 1:
        command = -1
        login = 0
        print('\nYou have successfully logged out!\n')
    # Menu
    if login == 0:
        print('1. Create an account\n2. Log into account\n0. Exit')
    else:
        print('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit')
    command = int(input())

print('\nBye!')
