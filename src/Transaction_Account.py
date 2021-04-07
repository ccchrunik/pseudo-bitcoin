# standard modules
import base58
import json
# third-party ecdsa modules
from ecdsa import SigningKey, VerifyingKey, NIST384p


class TransactionPool:
    def __init__(self):
        self._transactions = list()

    @property
    def size(self):
        return len(self._transactions)

    def add_transaction(self, transaction):
        self._transactions.append(transaction)

    def reset(self):
        self._transactions = []

    def pop_transaction(self, index):
        if index >= 0 and index < len(self._transactions):
            self._transactions.pop(index)
        else:
            print("Wrong index!")

    @property
    def records(self):
        return [tx.signed_record for tx in self._transactions]

    @property
    def balance(self):
        return [tx.balance for tx in self._transactions]

    @property
    def transactions(self):
        return self._transactions


class Transaction:
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
        signature = base58.b58encode(sk.sign(tx.record.encode())).decode()
        tx.signature = signature

        return tx.signed_record

    @staticmethod
    def verify(tx, vk):
        record, signature = sign_data.split('|')

        record = record.encode()
        signature = base58.b58decode(signature.encode())

        return vk.verify(signature, record)

    @staticmethod
    def serialize(tx):
        d = {'source': tx.source, 'dest': tx.dest,
             'amount': tx.amount, 'signature': tx.signature}
        data = json.dumps(d)
        return data

    @staticmethod
    def deserialize(raw_data):
        data = json.loads(raw_data)
        tx = Transaction(data['source'], data['dest'], data['amount'])
        tx._signature = data['signature']
        return tx
