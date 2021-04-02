from ecdsa import SigningKey, NIST384p


class Address:
    def __init__(self, name, balance=0):
        self._name = name
        self._balance = balance
        self.sk = SigningKey.generate(curve=NIST384p)
        self.vk = self.sk.verifying_key

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

    @property
    def verifying_key(self):
        return self.vk
