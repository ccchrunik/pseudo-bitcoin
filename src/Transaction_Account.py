# standard modules
import base58
import json
# third-party ecdsa modules
from ecdsa import SigningKey, VerifyingKey, NIST384p


class TransactionPool:
    """
    A class for collect all transactions into a pool.

    ...

    Attributes: 
    ----------
    size : int
        the number of transactions in the pool

    records : List[str]
        the transaction records of transactions

    balance : List[str]
        the transactions balance move record of transactions

    transactions : List[str]
        the transactions list in the pool

    Methods:
    ----------
    add_transaction(transaction) : None
        add a transaction into the transaction pool

    pop_transaction(index) : None
        pop transaction at the given index

    reset() : None
        clear all transactions in the pool
    """

    def __init__(self):
        self._transactions = list()

    @property
    def size(self):
        return len(self._transactions)

    @property
    def records(self):
        return [tx.signed_record for tx in self._transactions]

    @property
    def balance(self):
        return [tx.balance for tx in self._transactions]

    @property
    def transactions(self):
        return self._transactions

    def add_transaction(self, transaction):
        """Add a transaction into the pool"""
        self._transactions.append(transaction)

    def pop_transaction(self, index):
        """Pop a transaction out of the pool at the given index"""
        if index >= 0 and index < len(self._transactions):
            self._transactions.pop(index)
        else:
            print("Wrong index!")

    def reset(self):
        """Clear transactions in the pool"""
        self._transactions = []


class Transaction:
    """
    A class for storing transaction data.

    ... 

    Attributes: 
    ----------
    source : Wallet.address (str)
        the wallet address of the sender

    dest : Wallet.address (str)
        the wallet address of the receiver

    amount : int
        the amount of value to be transferred from one account to another

    signature : str
        the signature of the transaction record

    record : str
        the transaction record 

    balance : tuple
        the transaction record value (source, dest, amount)

    signed_record : str
        the transaction record combined with the signature

    Static Methods:
    ----------
    sign(tx, sk) : str
        sign the transaction record

    verify(tx, vk) : bool
        verify the transaction record and signature

    serialize(tx) : str
        transform a transaction into a string

    deserialize(raw_data) : 
        transform data back to a transaction
    """

    def __init__(self, source, dest, amount):
        self._source = source
        self._dest = dest
        self._amount = amount
        self._signature = None

    def __str__(self):
        return self.signed_record

    @property
    def source(self):
        return self._source

    @property
    def dest(self):
        return self._dest

    @property
    def amount(self):
        return self._amount

    @property
    def signature(self):
        return self._signature

    @signature.setter
    def signature(self, signature):
        self._signature = signature

    @property
    def record(self):
        return f'from: {self._source} -- to: {self._dest} -- amount: {self._amount}'

    @property
    def balance(self):
        return (self._source, self._dest, self._amount)

    @property
    def signed_record(self):
        if self.signature:
            return f'{self.record}|{self.signature}'
        else:
            return self.record

    @staticmethod
    def sign(tx, sk):
        """Sign a transaction and set the signature in a transaction"""
        signature = base58.b58encode(sk.sign(tx.record.encode())).decode()
        tx.signature = signature

        return tx.signed_record

    @staticmethod
    def verify(tx, vk):
        """Verify the signature of a record"""
        record, signature = sign_data.split('|')

        record = record.encode()
        signature = base58.b58decode(signature.encode())

        return vk.verify(signature, record)

    @staticmethod
    def serialize(tx):
        """Transform a transaction into a string"""
        d = {'source': tx.source, 'dest': tx.dest,
             'amount': tx.amount, 'signature': tx.signature}
        data = json.dumps(d)
        return data

    @staticmethod
    def deserialize(raw_data):
        """Transform a string back into a transaction"""
        data = json.loads(raw_data)
        tx = Transaction(data['source'], data['dest'], data['amount'])
        tx._signature = data['signature']
        return tx
