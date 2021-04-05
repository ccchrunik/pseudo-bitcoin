# standard modules
import json
import base64
# third-party ecdsa modules
from ecdsa import SigningKey, VerifyingKey, NIST384p


class Address:
    """
    A class represent the account data in the blockchain.

    ... 

    Attributes:
    ----------
    _name : str 
        the name of the account

    _balance : int 
        the account balance

    sk : SigningKey
        the signing key (private key) of the account

    vk : VerifyingKey
        the verifying key (public key) of the account

    Methods: 
    ----------
    add_balance(amount) : void 
        add the amount to the account balance

    sub_balance(amount) : void
        subtract the amount from the account balance

    verifying_key() : VerifyingKey
        return the verifying key of the account

    Accessor Methods: 
    ----------
    name : string
        get or set the name of the account

    balance : int
        get or set the account balance
    """

    def __init__(self, name, balance=0):
        """
        Parameters: 
        ----------
        name : str
            the name of the account

        balance : int 
            the account balance
        """
        self._name = name
        self._balance = balance
        self.sk = SigningKey.generate(curve=NIST384p)
        self.vk = self.sk.verifying_key

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

    def add_balance(self, amount):
        """Add the amount to the account balance

        Parameters: 
        ----------
        amount : int
            the amount to be added to the balance
        """
        self.balance += amount

    def sub_balance(self, amount):
        """Substract the amount from the account balance

        Parameters: 
        ----------
        amount : int
            the amount to be substracted form the account balance
        """
        self.balance -= amount

    @staticmethod
    def serialize(addr):
        d = {'name': addr.name, 'balance': addr.balance, 'sk': base64.b64encode(addr.sk.to_string(
        )).decode(), 'vk': base64.b64encode(addr.vk.to_string()).decode()}

        data = json.dumps(d)

        return data

    @staticmethod
    def deserialize(raw_data):
        data = json.loads(raw_data)
        addr = Address(data['name'], data['balance'])
        addr.sk = SigningKey.from_string(
            base64.b64decode(data['sk'].encode()), curve=NIST384p)
        addr.vk = VerifyingKey.from_string(
            base64.b64decode(data['vk'].encode()), curve=NIST384p)

        return addr
