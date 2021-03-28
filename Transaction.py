import hashlib
import base64


class TxInput:
    def __init__(self, Txid, Vout, ScriptSig):
        self.Txid = Txid
        self.Vout = Vout
        # self.ScriptSig = ScriptSig
        self.ScriptSig = 'temp input string'

    def value(self):
        return base64.b64encode(self.Txid).decode + str(self.Vout) + self.ScriptSig


class TxOutput:
    def __init__(self, value, ScriptPubKey):
        self.value = value
        # self.ScriptPubKey = ScriptPubKey
        self.ScriptPubKey = 'temp output string'

    def value(self):
        return str(self.value) + self.ScriptPubKey


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
