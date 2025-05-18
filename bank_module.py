# bank_module.py (refactored backend logic)
import os

class acc_hold:

    def __init__(self, id):
        self.usrnm = id
        self.fln = f"{id}.txt"
        with open(self.fln, 'r') as f:
            data = f.read().split("\n")
        self.fn, self.sn, self.age, self.balance, self.pin = data

    def wr_fl(self):
        data = f"{self.fn}\n{self.sn}\n{self.age}\n{self.balance}\n{self.pin}"
        with open(self.fln, 'w') as f:
            f.write(data)

    def deposit(self, amnt):
        self.balance = str(int(self.balance) + int(amnt))
        self.wr_fl()
        self.write_history(f"Rs {amnt} deposited.\n", self.usrnm)

    def withdraw(self, amnt):
        if int(amnt) > int(self.balance):
            return False, "Insufficient balance"
        self.balance = str(int(self.balance) - int(amnt))
        self.wr_fl()
        self.write_history(f"Rs {amnt} withdrawn.\n", self.usrnm)
        return True, f"Withdrawn Rs {amnt}"

    def transfer(self, receiver_id, amnt):
        if receiver_id == self.usrnm:
            return False, "Cannot transfer to yourself"
        if not os.path.exists(f"{receiver_id}.txt"):
            return False, "Receiver does not exist"
        if int(amnt) > int(self.balance):
            return False, "Insufficient balance"

        re_acc = acc_hold(receiver_id)
        self.balance = str(int(self.balance) - int(amnt))
        re_acc.balance = str(int(re_acc.balance) + int(amnt))
        self.wr_fl()
        re_acc.wr_fl()

        self.write_history(f"Rs {amnt} transferred to {receiver_id}.\n", self.usrnm)
        self.write_history(f"Rs {amnt} received from {self.usrnm}.\n", receiver_id)
        return True, f"Transferred Rs {amnt} to {receiver_id}"

    def write_history(self, data, usr):
        hname = f"{usr}-history.txt"
        with open(hname, "a") as file:
            file.write(data)

    def get_history(self):
        hname = f"{self.usrnm}-history.txt"
        if not os.path.exists(hname):
            return "No transaction history."
        with open(hname, "r") as f:
            return f.read()

    def get_inquiry(self):
        return f"Total balance: Rs {self.balance}"

    def get_details(self):
        return f"Name: {self.fn} {self.sn}\nAge: {self.age}\nBalance: Rs {self.balance}"

def create_account(fname, sname, age, deposit, username, password, pin):
    fln = f"{username}.txt"
    if os.path.exists(fln):
        return False, "Username already exists"

    with open(fln, 'w') as f:
        f.write(f"{fname}\n{sname}\n{age}\n{deposit}\n{pin}")

    with open("saved_accounts.txt", "a") as f:
        f.write(f"{username},{password}\n")

    with open(f"{username}-history.txt", "a") as f:
        f.write(f"Rs {deposit} deposited while creating account.\n")

    return True, "Account created successfully"

def check_credentials(username, password):
    if not os.path.exists("saved_accounts.txt"):
        return False
    with open("saved_accounts.txt", "r") as f:
        for line in f:
            u, p = line.strip().split(',')
            if u == username and p == password:
                return True
    return False
