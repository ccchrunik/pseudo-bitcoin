import hashlib
import json
import base64
import time
from configparser import ConfigParser


class PoW:
    def __init__(self, block):
        self._block = block
        self._target = 1 << (256 - block.bits)

        # read configuration and prepare header information
        cfg = ConfigParser()
        cfg.read('./config.txt')
        self.salt = cfg['secret']['salt'].encode()
        self.txdata = ':'.join(block.transactions).encode()
        # self.txdata = str(block.transactions).encode()
        self.prev_block_hash = base64.b64encode(block.prev_hash)
        self.data_prefix = str(block.height).encode() + str(block.time).encode() + str(block.bits).encode() + \
            self.txdata + self.prev_block_hash + block.merkle_tree.hash().encode()

    def prepare_data(self, nonce):
        self.data = self.data_prefix + str(nonce).encode()
        m = hashlib.sha256()
        m.update(self.salt + self.data)
        self.hash = int.from_bytes(m.digest(), 'big')
        print_hash = base64.b64encode(
            int.to_bytes(self.hash, 32, 'big')).decode()
        print(
            f'nonce = {nonce}, hash = {print_hash}', end='\r')

        return self.validate()

    def run(self):
        nonce = 0
        while True:
            # print(f'nonce = {nonce}')
            if self.prepare_data(nonce):
                hash_data = self.hash.to_bytes(32, 'big')
                return nonce, hash_data

            nonce += 1

    def validate(self):
        if self.hash < self._target:
            return True
        else:
            return False
