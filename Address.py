
class Address:
    def __init__(self, name, balance=0):
        self._name = name
        self._balance = balance

    def add_balance(self, amount):
        self.balance += amount

    def sub_balance(self, amount):
        self.balance -= amount

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, balance):
        self._balance = balance
