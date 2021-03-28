import sys
import os
import base64
import time
import hashlib
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
        self.address = ''
        self.height = 0

    def initialize(self, address):
        self.address = address
        self._blocks.append(self.new_genesis_block())

    def new_block(self, prev_height, transactions, prev_hash):
        # tx =
        block = Block(prev_height, time.time(), self.bits,
                      0, transactions, prev_hash)
        block.set_hash()
        return block

    def new_genesis_block(self):
        tx = self.new_coinbase_tx(self.address, 'test reward')
        block = self.new_block(0, [tx], hashlib.sha256().digest())
        return block

    def add_block(self, transactions):
        prev_block = self._blocks[-1]
        new_block = self.new_block(
            prev_block.height, transactions, prev_block.hash)
        self._blocks.append(new_block)

    def print_blocks(self):
        for block in self._blocks:
            print(block)

    # save blocks to files
    def save_blocks(self, path='/data'):
        base_dir = os.getcwd() + path
        # if the directory not exists
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)

        # serialize the genesis block
        with open(f'{base_dir}/genesis.json', 'w+') as f:
            data = Block.serialize(self._blocks[0])
            f.write(data + '\n')

        # serialize all blocks and save them to files
        for index, block in enumerate(self._blocks[1:]):
            with open(f'{base_dir}/data-{index}.json', 'w+') as f:
                data = Block.serialize(block)
                f.write(data + '\n')

    def read_blocks(self, path='/data'):
        base_dir = os.getcwd() + path
        # if the directory not exists
        if not os.path.exists(base_dir):
            return
        # deserialize the genesis block
        with open(f'{base_dir}/genesis.json', 'r') as f:
            data = f.read().strip('\n')
            block = Block.deserialize(data)
            self._blocks.append(block)

        # sort the file to get the right time sequence
        sort_dir = sorted(os.listdir(base_dir))
        sort_dir.remove('genesis.json')

        # read data from each file under the directory
        for file in sort_dir:
            with open(f'{base_dir}/{file}', 'r') as f:
                data = f.read().strip('\n')
                block = Block.deserialize(data)
                self._blocks.append(block)

    def new_coinbase_tx(self, to, data):
        if data == '':
            data = f'Reward to {to}'

        txin = TxInput('', -1, data)
        txout = TxOutput(self.subsidy, to)
        tx = Transaction(None, [txin], [txout])

        return tx

    def save_metadata(self, path='/metadata.json'):
        base_dir = os.getcwd() + path
        # if the directory not exists
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)

        with open(f'{base_dir}/metadata.json', 'w+') as f:
            d = {'bits': self.bits, 'subsidy': self.subsidy,
                 'address': self.address, 'height': len(self._blocks)}
            data = json.dumps(d)
            f.write(data + '\n')

    # read metadata like address from the file
    def read_metadata(self, path='/metedata.json'):
        base_dir = os.getcwd() + path
        # if the directory not exists
        if not os.path.exists(base_dir):
            return

        with open(path, 'r') as f:
            raw_data = f.read().split('\n')
            metadata = json.load(raw_data)
            self.bits = metadata['bits']
            self.subsidy = metadata['subsidy']
            self.address = metadata['address']
            self.length = metadata['length']


if __name__ == '__main__':
    blockchain = Blockchain()

    blockchain.initialize('my address')
    blockchain.add_block(['test block 1'])
    blockchain.add_block(['test block 2'])
    blockchain.add_block(['test block 3'])
    blockchain.add_block(['test block 4'])
    # blockchain.add_block(['test block 5'])
    # blockchain.add_block(['test block 6'])
    # blockchain.add_block(['test block 7'])
    # blockchain.add_block(['test block 8'])
    # blockchain.add_block(['test block 9'])
    # blockchain.add_block(['test block 10'])

    blockchain.print_blocks()
    blockchain.save_blocks()
    # blockchain.read_blocks()
    # blockchain.print_blocks()
