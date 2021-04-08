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

    balance : List[tuple]
        the transactions balance move record of transactions

    transactions : List[Transaction]
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
        """The number of transactions in the pool"""
        return len(self._transactions)

    @property
    def records(self):
        """The record list of transactions in the pool"""
        return [tx.signed_record for tx in self._transactions]

    @property
    def balance(self):
        """The balance list of transactions wallet"""
        return [tx.balance for tx in self._transactions]

    @property
    def transactions(self):
        """The transactions list in the pool"""
        return self._transactions

    def add_transaction(self, transaction):
        """Add a transaction into the pool

        Parameters:
        ----------
        transaction : Transaction
            the transaction to be added to the pool
        """
        self._transactions.append(transaction)

    def pop_transaction(self, index):
        """Pop a transaction out of the pool at the given index

        Parameters:
        ----------
        index : int
            the index of the transaction to be removed in the pool
        """
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

    deserialize(raw_data) : Transaction
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
        """The sender address"""
        return self._source

    @property
    def dest(self):
        """The receiver address"""
        return self._dest

    @property
    def amount(self):
        """The amounf of value to be transferred"""
        return self._amount

    @property
    def signature(self):
        """The signature of the transaction"""
        return self._signature

    @signature.setter
    def signature(self, signature):
        self._signature = signature

    @property
    def record(self):
        """The transaction record of the transaction"""
        return f'from: {self._source} -- to: {self._dest} -- amount: {self._amount}'

    @property
    def balance(self):
        """The transaction value pair of the transaction"""
        return (self._source, self._dest, self._amount)

    @property
    def signed_record(self):
        """The combination of the transaction record and signature"""
        if self.signature:
            return f'{self.record}|{self.signature}'
        else:
            return self.record

    @staticmethod
    def sign(tx, sk):
        """Sign a transaction and set the signature in a transaction

        Parameters:
        ----------
        tx : Transaction
            a transaction instance

        sk : SigningKey
            the signing key (private key) of a wallet

        Returns:
        ----------
        signed_record : str
            the signed transaction record
        """
        signature = base58.b58encode(sk.sign(tx.record.encode())).decode()
        tx.signature = signature

        return tx.signed_record

    @staticmethod
    def verify(tx, vk):
        """Verify the signature of a record

        Parameters:
        ----------
        tx : Transaction
            a transaction instance

        vk : VerifyingKey
            the verifying key (public key) of a wallet

        Returns:
        ----------
        result : bool
            the result of whether the transaction is valid
        """
        record, signature = sign_data.split('|')

        record = record.encode()
        signature = base58.b58decode(signature.encode())

        return vk.verify(signature, record)

    @staticmethod
    def serialize(tx):
        """Transform a transaction into a string

        Parameters:
        ----------
        tx : Transaction
            the transaction to be serialized

        Returns:
        ----------
        data : str
            the json formatted representation of the transaction
        """
        d = {'source': tx.source, 'dest': tx.dest,
             'amount': tx.amount, 'signature': tx.signature}
        data = json.dumps(d)
        return data

    @staticmethod
    def deserialize(raw_data):
        """Transform a string back into a transaction

        Parameters:
        ----------
        raw_data : str
            the json formatted string representation of a transaction

        Returns:
        ----------
        tx : Transaction
            a Transaction instance based on the given data
        """
        data = json.loads(raw_data)
        tx = Transaction(data['source'], data['dest'], data['amount'])
        tx._signature = data['signature']
        return tx
