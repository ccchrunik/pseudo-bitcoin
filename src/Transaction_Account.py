# third-party ecdsa modules
import base58
from ecdsa import SigningKey, VerifyingKey, NIST384p


class Transaction:
    def __init__(self, source, dest, amount):
        self._source = source
        self._dest = dest
        self._amount = amount
        self._signature = None

    def __str__(self):
        return self.signed_record

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
