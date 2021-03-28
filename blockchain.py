import sys
import os
import base64
import time
import hashlib
import json
from configparser import ConfigParser
# my block file
from Block import Block
from PoW import PoW
from Transaction import TxInput, TxOutput, Transaction


class Blockchain:
    def __init__(self):
        self._blocks = []
        self.bits = 10
        self.subsidy = 50
        self.address_pool = dict()
        self.height = 0
        self.count = 0
        self.index = 0

    def initialize(self, name):
        self.create_user(name)
        self._blocks.append(self.new_genesis_block())

    def create_user(self, name):
        if name not in self.address_pool:
            self.address_pool[name] = 0
        else:
            print('User name exist! Please choose another name as your address!')

    def new_block(self, prev_height, transactions, prev_hash):

        block = Block(prev_height, time.time(), self.bits,
                      0, transactions, prev_hash)
        block.set_hash()
        return block

    def new_genesis_block(self):
        # tx = self.new_coinbase_tx(self.address, 'test reward')
        block = self.new_block(-1, ['testblock 0'], hashlib.sha256().digest())
        return block

    def add_block(self, transactions):
        prev_block = self._blocks[-1]
        new_block = self.new_block(
            prev_block.height, transactions, prev_block.hash)
        self._blocks.append(new_block)

    def print_blocks(self):
        for block in self._blocks:
            print(block)

    def new_coinbase_tx(self, to, data):
        if data == '':
            data = f'Reward to {to}'

        txin = TxInput('', -1, data)
        txout = TxOutput(self.subsidy, to)
        tx = Transaction(None, [txin], [txout])

        return tx

    # save blocks to files
    def save_blocks(self, path='/data'):
        self.save_metadata(path)
        self.save_genesis_data(path)
        self.save_blocks_data(path)

    def save_metadata(self, path='/data'):
        base_dir = os.getcwd() + path
        # if the directory not exists
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)

        # save the genesis block
        with open(f'{base_dir}/genesis', 'w+') as f:
            data = Block.serialize(self._blocks[0])
            f.write(data + '\n')

        # save the metadata of the blockchain
        with open(f'{base_dir}/metadata', 'w+') as f:
            d = {'bits': self.bits, 'subsidy': self.subsidy, 'address_pool': self.address_pool,
                 'height': len(self._blocks), 'count': self.count, 'index': self.index}
            data = json.dumps(d)
            f.write(data + '\n')

    def save_genesis_data(self, path='/data'):
        base_dir = os.getcwd() + path

        # save the genesis block
        with open(f'{base_dir}/genesis', 'w+') as f:
            data = Block.serialize(self._blocks[0])
            f.write(data + '\n')

    def save_blocks_data(self, path='/data'):
        base_dir = os.getcwd() + path

        count = 0
        index = 0
        thres = 100
        f = open(f'{base_dir}/data-{index}', 'w+')
        # serialize all blocks and save them to files
        for block in self._blocks[1:]:
            index = count // thres
            # each file contains "thres" record
            if count != 0 and count % thres == 0:
                f.close()
                f = open(f'{base_dir}/data-{index}', 'w+')
            data = Block.serialize(block)
            count += 1
            f.write(data + '\n')

        f.close()

    def read_blocks(self, path='/data'):
        self.read_metadata(path)
        self.read_genesis_data(path)
        self.read_blocks_data(path)

    # read metadata like address from the file
    def read_metadata(self, path='/data'):
        base_dir = os.getcwd() + path
        # if the directory not exists
        if not os.path.exists(base_dir):
            return

        # read metadata
        with open(f'{base_dir}/metadata', 'r') as f:
            raw_data = f.read().strip('\n')
            metadata = json.loads(raw_data)
            self.bits = metadata['bits']
            self.subsidy = metadata['subsidy']
            self.address_pool = metadata['address_pool']
            self.height = metadata['height']
            self.count = metadata['count']
            self.index = metadata['index']

    def read_genesis_data(self, path='/data'):
        base_dir = os.getcwd() + path
        # read the genesis block
        with open(f'{base_dir}/genesis', 'r') as f:
            data = f.read().strip('\n')
            block = Block.deserialize(data)
            self._blocks.append(block)

    def read_blocks_data(self, path='/data'):
        base_dir = os.getcwd() + path

        # sort the file to get the right time sequence
        sort_dir = sorted(os.listdir(base_dir))
        sort_dir.remove('genesis')
        sort_dir.remove('metadata')

        # read data from each file under the directory
        for file in sort_dir:
            with open(f'{base_dir}/{file}', 'r') as f:
                for line in f:
                    data = line.strip('\n')
                    block = Block.deserialize(data)
                    self._blocks.append(block)


def test_save_blocks():
    blockchain = Blockchain()

    blockchain.initialize('my address')
    for i in range(1, 11):
        blockchain.add_block([f'test block {i}'])

    blockchain.print_blocks()
    blockchain.save_blocks()


def test_read_blocks():
    blockchain = Blockchain()
    blockchain.read_blocks()
    blockchain.print_blocks()


if __name__ == '__main__':
    test_save_blocks()
    # test_read_blocks()
