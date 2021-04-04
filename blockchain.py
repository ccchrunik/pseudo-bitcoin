
# standard modules
import sys
import os
import base58
import base64
import time
import hashlib
import json
import random

# my modules
from configparser import ConfigParser
from ecdsa import SigningKey, VerifyingKey, NIST384p
from Block import Block
from PoW import PoW
from Address import Address
from MerkleTree import MerkleTree


class Blockchain:
    """
    """

    def __init__(self):
        self._blocks = []
        self.bits = 15
        self.subsidy = 50
        self.address_pool = dict()
        self.transaction_pool = list()
        self.balance_pool = list()
        self.height = 0
        self.count = 0
        self.index = 0
        self.threshold = 100
        self.data_path = '/data'
        self.base_dir = os.getcwd() + self.data_path
        self.data_file = None
        self.address_file = None

    """
        Basic Operation Methods
        - initialize
        - create_user
        - new_block
        - new_genesis_block
        - add_block
    """

    def initialize(self, name):

        self.address_file = open(f'{self.base_dir}/address', 'w+')
        self.data_file = open(f'{self.base_dir}/data-0', 'w+')
        self.create_user(name)
        self.increment_balance(name, 50)
        genesis_block = self.new_genesis_block(name)
        self._blocks.append(genesis_block)
        # self.create_merkle_tree(genesis_block)
        self.save_block_data(genesis_block)

        # initialize the blockchain metadata and block file handler
        self.save_metadata()
        self.save_genesis_data()

    def create_user(self, name):
        if name not in self.address_pool:
            self.address_pool[name] = Address(name, 0)
            # update the address
            self.save_address_data((name, 0))
        else:
            print('User name exist! Please choose another name as your address!')

    def new_block(self, prev_height, transactions, prev_hash):
        block = Block(prev_height, time.time(), self.bits,
                      0, transactions, prev_hash)

        print(f'Try to get Block! {transactions} ...')
        block.set_hash()
        print(f'\nGet Block!!!', end='\n\n')
        return block

    def new_genesis_block(self, name):
        # tx = self.new_coinbase_tx(self.address, 'test reward')
        miner_data = f'Reward ${self.subsidy} to {name}'
        sign_data = self.sign_transaction(name, miner_data)
        block = self.new_block(-1, [sign_data], hashlib.sha256().digest())
        return block

    def add_block(self, transactions, name):
        prev_block = self._blocks[-1]
        new_block = self.new_block(
            prev_block.height, transactions, prev_block.hash)
        self._blocks.append(new_block)

        # account model
        # self.increment_balance(name, self.subsidy)
        # UTXO model

    @staticmethod
    def verify_blocks(block1, block2):
        return block1.merkle_tree.hash() == block2.merkle_tree.hash()

    def create_merkle_tree(self, block):
        block_data = block.transactions
        block.merkle_tree = MerkleTree.new_merkle_tree(block_data)

    # a coinbase transaction: add reward to the miner account

    def new_coinbase_tx_account(self, transactions, name):
        miner_data = f'Reward ${self.subsidy} to {name}'
        sign_data = self.sign_transaction(name, miner_data)
        transactions.append(sign_data)
        self.add_block(transactions, name)
        self.increment_balance(name, self.subsidy)
        # self.create_merkle_tree(self._blocks[-1])
        self.save_block_data(self._blocks[-1])

    # fire transactions: aggregate all transactions from the transaction pool

    def fire_transactions(self, name='Eric Chen'):
        self.new_coinbase_tx_account(self.transaction_pool, name)

        for source, dest, amount in self.balance_pool:
            if not self.have_balance(source, amount):
                raise ValueError(
                    f'{source} has no enough balance for transaction!!!')
            self.move_balance(source, dest, amount)

        self.transaction_pool = []
        self.balance_pool = []
        self.save_address_pool_data()

    # add a transaction to the transaction pool
    def add_transaction(self, source, dest, amount):
        if not self.have_balance(source, amount):
            raise ValueError(
                f'{source} has no enough balance for transaction!!!')
        tx_data = f'from: {source} -- to: {dest} -- amount: {amount}'
        sign_data = self.sign_transaction(source, tx_data)
        self.transaction_pool.append(sign_data)
        self.balance_pool.append((source, dest, amount))

    def sign_transaction(self, source, tx_data):
        sk = self.address_pool[source].sk
        signature = base58.b58encode(sk.sign(tx_data.encode())).decode()
        sign_data = tx_data + '|' + signature

        return sign_data

    def verify_transaction(self, source, sign_data):
        vk = self.address_pool[source].verifying_key
        tx_data, signature = sign_data.split('|')
        tx_data = tx_data.encode()
        signature = base58.b58decode(signature.encode())
        assert vk.verify(signature, tx_data)

    """
        Account Model Methods
        - have_balance
        - increment_balance
        - decrement_balance
        - move_balance
    """

    def have_balance(self, name, amount):
        if self.address_pool[name].balance >= amount:
            return True
        else:
            return False

    def increment_balance(self, name, amount):
        self.address_pool[name].add_balance(amount)

    def decrement_balance(self, name, amount):
        self.address_pool[name].sub_balance(amount)

    def move_balance(self, source, dest, amount):
        self.decrement_balance(source, amount)
        self.increment_balance(dest, amount)

    """
        UTXO Model Methods
        - new_coinbase_tx
    """

    # def new_coinbase_tx(self, to, data):
    #     if data == '':
    #         data = f'Reward to {to}'

    #     txout = TxOutput(self.subsidy, to)
    #     txin = TxInput('', txout, data)
    #     tx = Transaction(None, [txin], [txout])

    #     return tx

    """
        Save Blokchain Data Methods
        - save_blocks
        - save_metadata
        - save_address_data
        - save_address_pool_data
        - save_genesis_data
        - save_block_data
        - save_blocks_data
    """

    # save blocks to files
    def save_blocks(self, path='/data'):
        self.save_metadata(path)
        self.save_address_pool_data(path)
        self.save_genesis_data(path)
        self.save_blocks_data(path)
        self.save_transaction_data(path)

    def save_metadata(self, path='/data'):
        base_dir = os.getcwd() + path
        # if the directory not exists
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)

        # save the metadata of the blockchain
        with open(f'{base_dir}/metadata', 'w+') as f:
            d = {'bits': self.bits, 'subsidy': self.subsidy, 'height': len(
                self._blocks), 'count': self.count, 'index': self.index}
            data = json.dumps(d)
            f.write(data + '\n')

    def save_address_data(self, addr):
        # save the metadata of the blockchain
        key, value = addr
        d = {key: value}
        data = json.dumps(d)
        self.address_file.write(data + '\n')

    def save_address_pool_data(self, path='/data'):
        base_dir = os.getcwd() + path
        # save the metadata of the blockchain
        self.address_file.close()
        with open(f'{self.base_dir}/address', 'w+') as f:
            for name, addr in self.address_pool.items():
                d = {'name': name, 'balance': addr.balance, 'sk': base64.b64encode(addr.sk.to_string(
                )).decode(), 'vk': base64.b64encode(addr.vk.to_string()).decode()}
                data = json.dumps(d)
                f.write(data + '\n')

    def save_transaction_data(self, path='/data'):
        base_dir = os.getcwd() + path
        # save the metadata of the blockchain
        with open(f'{self.base_dir}/transactions', 'w+') as f:
            for source, dest, amount in self.balance_pool:
                d = {'source': source, 'dest': dest, 'amount': amount}
                data = json.dumps(d)
                f.write(data + '\n')

    def save_genesis_data(self, path='/data'):
        base_dir = os.getcwd() + path

        # save the genesis block
        with open(f'{base_dir}/genesis', 'w+') as f:
            data = Block.serialize(self._blocks[0])
            f.write(data + '\n')

    # dynamically save a block when we add a block to the blockchain
    def save_block_data(self, block):
        # serialize the block and save it to the file
        data = Block.serialize(block)
        self.index = self.count // self.threshold
        # create a new file for incoming data
        if self.count != 0 and self.count % self.threshold == 0:
            self.data_file.close()
            self.data_file = open(f'{self.base_dir}/data-{self.index}', 'w+')

        self.count += 1
        self.data_file.write(data + '\n')
        self.save_metadata()

    # used for forcibly save all blocks
    def save_blocks_data(self, path='/data'):
        self.data_file.close()
        base_dir = os.getcwd() + path
        count = 0
        index = 0
        threshold = 100
        f = open(f'{base_dir}/data-{index}', 'w+')
        # serialize all blocks and save them to files
        for block in self._blocks[1:]:
            index = count // threshold
            # each file contains "thres" record
            if count != 0 and count % threshold == 0:
                f.close()
                f = open(f'{base_dir}/data-{index}', 'w+')
            data = Block.serialize(block)
            count += 1
            f.write(data + '\n')

        f.close()

    """
        Read Blochchain Data Methods
        - read_blocks
        - read_metadata
        - read_address_pool_data
        - read_genesis_data
        - read_blocks_data
    """

    def read_blockchain(self, path='/data'):
        self.read_metadata(path)
        self.read_address_pool_data(path)
        self.read_transaction_data(path)
        self.read_genesis_data(path)
        self.address_file = open(f'{self.base_dir}/address', 'a+')
        self.data_file = open(f'{self.base_dir}/data-{self.index}', 'a+')
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
            self.height = metadata['height']
            self.count = metadata['count']
            self.index = metadata['index']

    def read_address_pool_data(self, path='/data'):
        base_dir = os.getcwd() + path

        # read address data
        with open(f'{base_dir}/address', 'r') as f:
            for line in f:
                raw_data = line.strip('\n')
                # print(raw_data)
                address = json.loads(raw_data)
                name = address['name']
                balance = address['balance']
                addr = Address(name, balance)
                addr.sk = SigningKey.from_string(
                    base64.b64decode(address['sk'].encode()), curve=NIST384p)
                addr.vk = VerifyingKey.from_string(
                    base64.b64decode(address['vk'].encode()), curve=NIST384p)
                self.address_pool[name] = addr

    def read_transaction_data(self, path='/data'):
        base_dir = os.getcwd() + path

        # read transaction data
        with open(f'{base_dir}/transactions', 'r') as f:
            for line in f:
                raw_data = line.strip('\n')
                transaction = json.loads(raw_data)

                source = transaction['source']
                dest = transaction['dest']
                amount = transaction['amount']
                tx_data = f'from: {source} -- to: {dest} -- amount: {amount}'
                self.transaction_pool.append(tx_data)
                self.balance_pool.append((source, dest, amount))

        with open(f'{base_dir}/transactions', 'w+') as f:
            pass

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
        sort_dir.remove('address')
        sort_dir.remove('transactions')

        # read data from each file under the directory
        for file in sort_dir:
            with open(f'{base_dir}/{file}', 'r') as f:
                for line in f:
                    data = line.strip('\n')
                    block = Block.deserialize(data)
                    self._blocks.append(block)
                    # self.create_merkle_tree(block)
                    block.merkle_tree = block.create_merkle_tree()

    # shutdown the blockchain

    def freeze(self):
        self.data_file.close()

    """
        Display Methods
        - print_blocks
    """

    def print_blocks(self):
        for block in self._blocks:
            print(block)


"""
    Test Methods
    - test_save_blocks
    - test_read_blocks
"""


def test_save_blocks():
    blockchain = Blockchain()

    try:
        blockchain.initialize('Eric Chen')
        # blockchain.increment_balance('Eric Chen', 10000)
        blockchain.increment_balance('Eric Chen', 1000000)

        for i in range(1, 11):
            blockchain.create_user(f'my address {i}')

        for i in range(1, 201):
            if len(blockchain.balance_pool) >= 100:
                blockchain.fire_transactions('Eric Chen')

            winner = random.randint(1, 10)
            blockchain.add_transaction(
                'Eric Chen', f'my address {winner}', 80)
        if len(blockchain.balance_pool) >= 100:
            blockchain.fire_transactions('Eric Chen')
    except ValueError as e:
        blockchain.save_blocks()
    except KeyboardInterrupt:
        blockchain.save_blocks()


def test_read_blocks():
    blockchain = Blockchain()
    blockchain.read_blockchain()

    try:
        blockchain.increment_balance('Eric Chen', 200000)

        for i in range(301, 1001):
            if len(blockchain.balance_pool) >= 100:
                blockchain.fire_transactions('Eric Chen')

            winner = random.randint(1, 10)
            blockchain.add_transaction(
                'Eric Chen', f'my address {winner}', 80)

        if len(blockchain.balance_pool) >= 100:
            blockchain.fire_transactions('Eric Chen')

        blockchain.save_address_pool_data()
        blockchain.print_blocks()
    except ValueError as e:
        blockchain.save_blocks()
    except KeyboardInterrupt:
        blockchain.save_blocks()


def test_signature():
    blockchain = Blockchain()
    blockchain.read_metadata()
    blockchain.read_address_pool_data()
    blockchain.read_genesis_data()
    block = blockchain._blocks[0]
    blockchain.verify_transaction('Eric Chen', block.transactions[0])


if __name__ == '__main__':
    # test_save_blocks()
    test_read_blocks()
    # test_signature()
