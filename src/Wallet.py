# standard modules
import hashlib
import json
import base64
import base58
# third-party ecdsa modules
from ecdsa import SigningKey, VerifyingKey, NIST384p
from Crypto.Hash import RIPEMD160


class WalletPool:
    def __init__(self):
        self._wallets = dict()

    @property
    def wallets(self):
        return self._wallets.items()

    @property
    def size(self):
        return len(self._wallets.keys())

    def get_wallet(self, address):
        return self._wallets[address]

    def has_address(self, address):
        return address in self._wallets

    def add_wallet(self, wallet):
        self._wallets[wallet.address] = wallet

    def remove_address(self, address):
        return self._wallets.pop(address, None)

    def has_balance(self, address, amount):
        return self._wallets[address].balance >= amount

    def add_balance(self, address, amount):
        wallet = self._wallets[address]
        wallet.add_balance(amount)

    def sub_balance(self, address, amount):
        wallet = self._wallets[address]
        wallet.sub_balance(amount)

    def wallet_balance(self, address):
        return self._wallets[address].balance

    def get_wallet_signing_key(self, address):
        wallet = self._wallets[address]
        return wallet.signing_key

    def get_wallet_verifying_key(self, address):
        wallet = self._wallets[address]
        return wallet.verifying_key


class Wallet:
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
        self._address = self._create_address()

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
    def address(self):
        return self._address

    @property
    def signing_key(self):
        return self.sk

    @property
    def verifying_key(self):
        return self.vk

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address

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

    def _create_address(self):
        m = hashlib.sha256()
        h = RIPEMD160.new()
        vk = base64.b64encode(self.verifying_key.to_string())

        m.update(vk)
        h.update(m.digest())
        key_hash = h.digest()

        m = hashlib.sha256()
        m.update(key_hash)
        temp = m.digest()

        m = hashlib.sha256()
        m.update(temp)
        checksum = m.digest()

        addr = key_hash + checksum

        return base58.b58encode(addr).decode()

    @staticmethod
    def verify_address(wallet):
        m = hashlib.sha256()
        h = RIPEMD160.new()
        vk = base64.b64encode(wallet.verifying_key.to_string())

        m.update(vk)
        key_hash = h.update(m.digest())

        m = hashlib.sha256()
        m.update(key_hash)
        temp = m.digest()

        m = hashlib.sha256()
        m.update(temp)
        checksum = m.digest()

        addr = key_hash + checksum

        return addr == wallet.address

    @staticmethod
    def serialize(wallet):
        d = {'name': wallet.name, 'balance': wallet.balance, 'sk': base64.b64encode(wallet.signing_key.to_string(
        )).decode(), 'vk': base64.b64encode(wallet.verifying_key.to_string()).decode(), 'address': wallet.address}

        data = json.dumps(d)

        return data

    @staticmethod
    def deserialize(raw_data):
        data = json.loads(raw_data)
        wallet = Wallet(data['name'], data['balance'])
        wallet.sk = SigningKey.from_string(
            base64.b64decode(data['sk'].encode()), curve=NIST384p)
        wallet.vk = VerifyingKey.from_string(
            base64.b64decode(data['vk'].encode()), curve=NIST384p)
        wallet.address = data['address']

        return wallet
