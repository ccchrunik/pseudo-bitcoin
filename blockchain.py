import sys
import os
import hashlib
import json
import base64
import time
from configparser import ConfigParser


class Block:
    def __init__(self, prev_hash, time, bits, nonce, transactions):
        self.height = 1
        self.prev_hash = prev_hash
        self.time = time
        self.bits = bits
        self.nonce = nonce
        # transactions is a list
        self.transactions = transactions

        cfg = ConfigParser()
        cfg.read('./utils/config.txt')
        salt = cfg['secret']['salt'].encode()
        txdata = ':'.join(transactions).encode()
        prev_block_hash = base64.b64encode(self.prev_hash)

        data = str(self.height).encode() + str(time).encode() + str(bits).encode() + \
            str(nonce).encode() + txdata + prev_block_hash

        m = hashlib.sha256()
        m.update(salt + data)
        self.hash = m.digest()

    def __str__(self):
        print(f"Block Information: ")
        print(f"---")
        print(f"height: {self.height}")
        print(f"time: {self.time}")
        print(f"hardness: {self.bits}")
        print(f"nonce: {self.nonce}")
        print(f"transactions: {self.transactions}")
        print(f"previous hash: {self.prev_hash}")
        print(f"hash: {self.hash}")
        print(f"---")
        return ''

    def compress(self):
        prev_hash = base64.b64encode(self.prev_hash).decode()
        block_hash = base64.b64encode(self.hash).decode()
        print(prev_hash)
        print(block_hash)
        d = {'height': self.height, 'bits': self.bits, 'time': self.time, 'nonce': self.nonce,
             'transactions': self.transactions, 'prev_block_hash': prev_hash, 'hash': block_hash}
        data = json.dumps(d)
        print(data)
        return data


class Blockchain:
    def __init__(self):
        self._blocks = []

    def print_blocks(self):
        for block in self._blocks:
            print(block)

    def save_blocks(self, path='/data'):
        base_dir = os.getcwd() + path
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)

        for index, block in enumerate(self._blocks):
            with open(f'{base_dir}/data-{index}.json', 'w+') as f:
                data = block.compress()
                f.write(data + '\n')

    def read_blocks(self, path='/data'):
        pass

    def new_block(self, prev_hash, time, bits, nonce, transactions):
        block = Block(prev_hash, time, bits, nonce, transactions)
        self.add_block(block)
        return block

    def new_genesis_block(self):
        block = Block(hashlib.sha256().digest(), 1616408474,
                      10, 234325325, ['the genesis block', 'test block', 'I am handsome'])
        self.add_block(block)
        return block

    def add_block(self, block):
        self._blocks.append(block)


if __name__ == '__main__':
    blockchain = Blockchain()
    genesis_block = blockchain.new_genesis_block()
    blockchain.new_block(genesis_block.hash, time.time(),
                         10, 23412341431421, ['test block 2'])
    blockchain.print_blocks()
    blockchain.save_blocks()
