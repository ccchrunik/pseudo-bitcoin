import hashlib
import base64


class TxInput:
    def __init__(self, Txid, Vout, ScriptSig='temp input string'):
        self.Txid = Txid
        self.Vout = Vout
        # self.ScriptSig = ScriptSig
        self.ScriptSig = ScriptSig

    def value(self):
        return base64.b64encode(self.Txid).decode + str(self.Vout) + self.ScriptSig

    @staticmethod
    def serialize(txin):
        return ''

    @staticmethod
    def deserialize(data):
        return ''


class TxOutput:
    def __init__(self, value, ScriptPubKey='temp output string'):
        self.value = value
        # self.ScriptPubKey = ScriptPubKey
        self.ScriptPubKey = ScriptPubKey

    def value(self):
        return str(self.value) + self.ScriptPubKey

    @staticmethod
    def serialize(txout):
        return ''

    @staticmethod
    def deserialize(data):
        return ''


class Transaction:
    def __init__(self, ID, Vin, Vout):
        self.ID = ID
        self.Vin = Vin
        self.Vout = Vout

    def set_ID(self):
        m = hashlib.sha256()
        value = (self.Vin.value() + self.Vout.value()).encode()
        m.update(value)
        self.ID = m.digest()
        return self.ID

    @staticmethod
    def serialize(txin, txout):
        return ''

    @staticmethod
    def deserialize(in_data, out_data):
        return ''


class Transaction_Pool:
    def __init__(self, txs):
        self.transactions = []
        print(type(txs))
        print(len(txs))
        self.add_transactions(txs)

    def add_transactions(self, txs):
        for tx in txs:
            if not isinstance(tx, Transaction):
                raise ValueError('You must input a list of transactions!!!')
            else:
                self.transactions.append(tx)

    def __str__(self):
        if len(self.transactions) == 0:
            return ''
        else:
            return ''
