
# standard modules
import sys
import os
import base58
import base64
import time
import hashlib
import json
import random
from configparser import ConfigParser

# my modules
from ecdsa import SigningKey, VerifyingKey, NIST384p
from Block import Block
from PoW import PoW
from Wallet import Wallet, WalletPool
from MerkleTree import MerkleTree
from Transaction_Account import Transaction, TransactionPool

# TODO: Complete CLI
# TODO: Refactor CLI using decorator factory
# TODO: Refactor read and save methods
# TODO: Complete UTXO Model
# TODO: Create virtual environment
# TODO: Add Client-Server Network Model
# TODO: Add P2P Network Model

# Change storage directory to the project directory
os.chdir('../')


class Blockchain:
    """
    The main class of the Blockchain.

    ... 

    Attributes:
    ----------
    _blocks : List[Block]
        the blocks in the blockchain

    bits : int 
        the PoW hardness in the current blockchain, can change between blocks

    subsify : int
        the mining reward of a block 

    address_pool : Dict(str -> Address)
        the dictionary to store the all account address

    transaction_pool : List[str]
        the pending transactions records to be added to the next block

    balance_pool : List[(str, str, int)]
        the actual transactions waiting to be written in the blockchain 

    height : int
        the height of the blockchain

    count : int 
        internal variable for controlling the data file name

    index : int
        internal variable for controlling the data file name

    threshold : int
        internal variable as the trigger threshold to change the file name

    data_path : str
        the path the blockchain to save the block data in the file system

    base_dir : str 
        the base directory name of this project

    data_file : file
        the file handler that the blockchain write the block data to

    address_file : file
        the file handler that the blockchain write the address data to


    Methods: 
    ----------
    initialize(name) : void
        initialize the blockchain with the provided name

    create_user(name) : void
        create an user with the given name in the address pool

    new_block_data(prev_height, transactions, prev_hash) : Block
        create a new block, internal method

    new_genesis_block(name) : Block
        create the genesis block, internal method

    add_block(transactions, name) : void
        create a new block and add it to the blockchain, internal method

    new_coinbase_tx_account(transactions, name) : void
        add reward to miner and add a block to the blockchain, internal method

    fire_transactions(self, name='Eric Chen') : void 
        aggregate all transactions in the blockchain to a single block and add it to the blockchain, internal method

    add_transaction(source, dest, amount) : void
        add a transaction to the transaction

    sign_transaction(source, tx_data) : void
        sign a transaction using source's signing key and add signature after the transaction, internal method

    verify_transaction(source, sign_data) : void
        assert whether that a transaction is valid, internal method

    have_balance(name, amount) : bool
        check if an account has enough balance, internal method

    increment_balance(name, amount) : void
        increment an account's balance, internal method

    decrement_balance(name, amount) : void
        decrement an account's balance, internal method

    move_balance(source, dest, amount) : void
        move balance from source account to destination acccount, internal method

    save_blockchain(path='/data') : void
        save blockchain data under the path directory under the project folder

    save_metadata(path='/data') : void
        save the blockchain metadata under the path directory under the project folder, internal method

    save_address_data(addr, path='/data') : void
        save the blockchain address data under the path directory under the project folder, internal method

    save_address_pool_data(path='/data') : void
        save the blockchain all addresses data under the path directory under the project folder, internal method

    save_genesis_data(path='/data') : void
        save the blockchain genesis block data under the path directory under the project folder, internal method

    save_transaction_data(path='/data') : void
        save the blockchain unprocessed transactions under the path directory under the project folder, internal method

    save_block_data(path='/data') : void
        save a block data under the path directory under the project folder, internal method

    save_blocks_data(path='/data') : void
        save all blockchain blocks under the path directory under the path directory, internal method

    read_blockchain(path='/data') : void
        read all blockchain blocks under the path directory under the path directory, internal method

    read_address_pool_data(path='/data') : void
        read all account data under the path directory under the path directory, internal method

    read_genesis_data(path='/data') : void
        read the genesis block data under the path directory under the project folder, internal method

    read_metadata_data(path='/data') : void
        read the blockchain metadata under the path directory under the project folder, internal method

    read_transaction_data(path='/data') : void
        read the unprocessed transaction data under the path directory under the project folder, internal method

    read_blocks_data(path='/data') : void
        read the blocks data under the path directory under the project folder, internal method

    print_blocks() : void
        print all blocks in the blockchain


    Static Methods:
    ----------
    verify_block(block1, block2) : bool
        verify the top hash of the merkle tree of each block
    """

    def __init__(self, bits=10, subsidy=50, threshold=100, path='/data'):
        self._blocks = []
        self._bits = bits
        self._subsidy = subsidy
        self._root_address = None
        self._wallet_pool = WalletPool()
        self._transaction_pool = TransactionPool()
        self._height = 0
        self._count = 0
        self._index = 0
        self._threshold = threshold
        self._base_dir = os.getcwd() + path
        self._info_path = self._base_dir + '/info'
        self._data_path = self._base_dir + '/data'
        self._data_file = None
        self._wallet_file = None

    @property
    def blocks(self):
        return self._blocks

    @property
    def bits(self):
        return self._bits

    @property
    def subsidy(self):
        return self._subsidy

    @property
    def threshold(self):
        return self._threshold

    @property
    def info_path(self):
        return self._info_path

    @property
    def data_path(self):
        return self._data_path

    @property
    def base_dir(self):
        return self._base_dir

    @property
    def tx_num(self):
        return self._transaction_pool.size

    @property
    def wallet_num(self):
        return self._wallet_pool.size

    @property
    def size(self):
        return len(self._blocks)

    def initialize(self, name):
        """Initialize the blockchain

        Parameters: 
        ----------
        name : str
            the first account name of the blockchain
        """
        if not os.path.exists(self._info_path):
            os.mkdir(self._info_path)

        if not os.path.exists(self._data_path):
            os.mkdir(self._data_path)

        # Open file handler to save initialization data
        self._wallet_file = open(f'{self._info_path}/wallet', 'w+')
        self._data_file = open(f'{self._data_path}/data-0', 'w+')

        # Create an user
        wallet = self.create_user(name)
        self._root_address = wallet.address

        self.increment_balance(wallet.address, self._subsidy)

        # Create the genesis block
        genesis_block = self._new_genesis_block(wallet.address)
        self._blocks.append(genesis_block)

        # Save the initialization data
        self._save_metadata()
        self._save_genesis_data()

        return wallet

    def create_user(self, name):
        """Create an user in the blockchain

        Parameters: 
        ----------
        name : str
            create an user based on the given name
        """
        # Add to the address pool
        wallet = Wallet(name, 0)
        self._wallet_pool.add_wallet(wallet)

        # Update the address data
        self._save_wallet_pool_data()

        return wallet

    def _new_block(self, prev_height, transactions, prev_hash):
        """Create a new block in the blockchain

        Parameters: 
        ----------
        prev_height : int
            the height of the previous block

        transactions : List[str]
            the transactions of the block

        prev_hash : bytes
            the hash of the previous block

        Returns: 
        ----------
        block : Block
            return the new block
        """

        # Create a Block instance
        block = Block(prev_height, time.time(), self._bits,
                      0, transactions, prev_hash)

        print(f'Try to get Block! {transactions} ...')

        # Compute the hash of the block
        block.set_hash()

        print(f'\nGet Block!!!', end='\n\n')
        return block

    def _new_genesis_block(self, address):
        """Create the genesis block

        Parameters: 
        ----------
        name : str
            the name of first account

        Returns: 
        ---------- 
        block : Block
            the genesis block
        """
        # Construct the reward message
        miner_data = f'This is the genesis block!!!'

        # Sign the transaction data
        sign_data = self._sign_transaction(address, miner_data)

        # Create the block
        prev_hash = base64.b64encode(hashlib.sha256().digest()).decode()
        block = self._new_block(-1, [sign_data], prev_hash)

        return block

    def _add_block(self, transactions):
        """Create a new block and add it to the blockchain

        Parameters:
        ---------- 
        transactions : List[str]
            the transactions of the created block

        name : str
            the name of the miner
        """
        prev_block = self._blocks[-1]

        # Create and append a new block to the blockchain
        new_block = self._new_block(
            prev_block.height, transactions, prev_block.hash)
        self._blocks.append(new_block)

    @staticmethod
    def verify_blocks(block1, block2):
        """Verify the top hash of the merkle tree of each block

        Parameters:
        ---------- 
        block1 : Block
            a block

        block2 : Block
            a block
        """
        return block1.merkle_tree.hash == block2.merkle_tree.hash

    def _new_coinbase_tx_account(self, transactions, address):
        """Add reward to the miner and add a block to the blockchain

        Parameters:
        ----------
        transactions : List[str]
            the transactions of the block

        name : str
            the name of the miner 
        """
        # Create and sign a reward transaction
        miner_data = f'Reward ${self.subsidy} to {address}'
        sign_data = self._sign_transaction(address, miner_data)

        # Add a block to the blockchain
        transactions.append(sign_data)
        self._add_block(transactions)

        # Add reward to miner's account
        self.increment_balance(address, self._subsidy)

        # Save the block data
        self._save_block_data(self._blocks[-1])

    def fire_transactions(self, address):
        """Aggregate all transactions in the blockchain to a single block and add it to the blockchain, internal method

        Parameters:
        ---------- 
        name : str
            the name of the miner
        """

        # Add transactions records in the blockchain
        self._new_coinbase_tx_account(self._transaction_pool.records, address)

        # Move money between account based on each transaction
        for source, dest, amount in self._transaction_pool.balance:
            if not self.have_balance(source, amount):
                raise ValueError(
                    f'{source} has no enough balance for transaction!!!')
            self.move_balance(source, dest, amount)

        # Save updated account data
        self._save_wallet_pool_data()

        # Clear the transaction records and balance
        self._transaction_pool.reset()

    def add_transaction(self, source, dest, amount):
        """Add a transaction to the transaction pool

        Parameters:
        ---------- 
        source : Address
            the address of the sender

        dest : Address
            the address of the receiver

        amount : int
            the amount that moving between accounts 
        """

        # Check if sender have enough balance
        if not self.have_balance(source, amount):
            raise ValueError(
                f'{source} has no enough balance for transaction!!!')

        # Create a transaction
        tx = Transaction(source, dest, amount)

        # Add transaction on the blockchain
        self._transaction_pool.add_transaction(tx)

        # If the number of transactions reaches the threshold, create a new block
        if self._transaction_pool.size >= self._threshold:
            self.fire_transactions(source)

        self._save_transaction_data()

    def _sign_transaction(self, source, tx_data):
        """Sing a transaction and add signature to the transaction

        Parameters:
        ----------
        source : Address
            the sender account

        tx_data : str
            the transaction data 

        Returns:
        ---------- 
        sign_data : str
            the signed transaction 
        """

        # Sign the transaction and add signature after the transaction
        sk = self._wallet_pool.get_wallet_signing_key(source)
        signature = base58.b58encode(sk.sign(tx_data.encode())).decode()
        sign_data = tx_data + '|' + signature

        return sign_data

    def _verify_transaction(self, source, sign_data):
        """Verify whether a signed transaction is valid

        Parameters: 
        -----------
        source : Address
            the sender account address

        sign_data : str
            the signed transaction
        """
        # Process the signed transaction
        vk = self._wallet_pool.get_wallet_verifying_key(source)
        tx_data, signature = sign_data.split('|')
        tx_data = tx_data.encode()
        signature = base58.b58decode(signature.encode())

        # Verify the signature
        assert vk.verify(signature, tx_data)

    def get_balance(self, address):
        if self._wallet_pool.has_address(address):
            return self._wallet_pool.wallet_balance(address)
        else:
            print('The account does not exist!!!')

    def have_balance(self, address, amount):
        """Check if an account has enough amount of balance

        name : str 
            the sender account name

        amount : int
            the amount of balance
        """
        if self._wallet_pool.has_balance(address, amount):
            return True
        else:
            return False

    def increment_balance(self, address, amount):
        """Increment an account's balance

        name :  str
            an account name

        amount : int
            the amount of balance to be incremented
        """
        self._wallet_pool.add_balance(address, amount)
        self._save_wallet_pool_data()

    def decrement_balance(self, address, amount):
        """decrement an account's balance

        name :  str
            an account name

        amount : int
            the amount of balance to be decremented
        """
        self._wallet_pool.sub_balance(address, amount)
        self._save_wallet_pool_data()

    def move_balance(self, source, dest, amount):
        """Move balance from source account to dest account

        source :  str
            the source account name

        dest : str
            the destination account name

        amount : int
            the amount of balance to be moved
        """
        self.decrement_balance(source, amount)
        self.increment_balance(dest, amount)

    def save_blockchain(self, path='/data'):
        """Save blockchain data under the path folder under the project directory

        Parameters:
        ----------
        path : str
            the path to store the blockchain data
        """

        info_path = path + '/info'
        data_path = path + '/data'

        # Save blockchain metadata
        self._save_metadata(info_path)

        # Save account data
        self._save_wallet_pool_data(info_path)

        # Save uncommited transactions
        self._save_transaction_data(info_path)

        # Save the genesis block data
        self._save_genesis_data(data_path)

        # Save blocks data
        self._save_blocks_data(data_path)

    def _save_metadata(self, path='/data/info'):
        """Save blockchain metadata

        Parameters: 
        ---------
        path : str
            the path to store the metadata 
        """

        # Get the base directory
        base_dir = os.getcwd() + path

        # Make sure the base directory exists
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)

        # Save the metadata
        with open(f'{base_dir}/metadata', 'w+') as f:
            # Create a dictionary contains blockchain metadata
            d = {'bits': self._bits, 'subsidy': self._subsidy, 'height': len(
                self._blocks), 'count': self._count, 'index': self._index, 'root_address': self._root_address}

            # Dump data to json formatted data and save it
            data = json.dumps(d)
            f.write(data + '\n')

    def _save_wallet_data(self, addr, path='/data/info'):
        """Save an account address

        Parameters: 
        ---------
        name : Address
            the account to be stored

        path : str
            the path to store the account address
        """
        # Get the base directory
        base_dir = os.getcwd() + path
        data = Wallet.serialize(addr)
        self._wallet_file.write(data + '\n')

    def _save_wallet_pool_data(self, path='/data/info'):
        """Save all account address

        Parameters: 
        ---------
        path : str
            the path to store the account addresses
        """
        # Get the base directory
        base_dir = os.getcwd() + path

        # Reset the address file
        self._wallet_file.close()

        # Save the address data
        with open(f'{base_dir}/wallet', 'w+') as f:
            for address, wallet in self._wallet_pool.wallets:
                data = Wallet.serialize(wallet)
                f.write(data + '\n')

    def _save_transaction_data(self, path='/data/info'):
        """Save the unprocessed transaction data

        Parameters:
        ----------
        path : str
            the path to store the transaction data
        """
        base_dir = os.getcwd() + path
        # Save transactions data record
        with open(f'{base_dir}/transactions', 'w+') as f:
            for tx_balance in self._transaction_pool.balance:
                data = Transaction.serialize(tx_balance)
                f.write(data + '\n')

    def _save_genesis_data(self, path='/data/data'):
        """Save genesis block data

        Parameters:
        ----------
        path : str
            the path to store the genesis block data
        """
        base_dir = os.getcwd() + path

        # Save the genesis block
        with open(f'{base_dir}/genesis', 'w+') as f:
            data = Block.serialize(self._blocks[0])
            f.write(data + '\n')

    def _save_block_data(self, block, path='/data/data'):
        """Save a block data

        Parameters: 
        ----------
        block : Block
            the block to be stored

        path : str
            the path to store the block data
        """
        # Serialize the block
        data = Block.serialize(block)

        # Track the data file to be written
        self._index = self._count // self._threshold

        # Create a new file for incoming data if we have too many block in this data file
        if self._count != 0 and self._count % self._threshold == 0:
            self._data_file.close()
            self._data_file = open(f'{self.base_dir}/data-{self.index}', 'w+')

        self._count += 1
        self._data_file.write(data + '\n')
        self._save_metadata()

    def _save_blocks_data(self, path='/data/data'):
        """Save blocks data in the blockchain

        Parameters:
        ----------
        path : str
            the path to store the blocks data
        """
        # Reset the data file
        self._data_file.close()

        base_dir = os.getcwd() + path

        # Track the file to write the next block
        count = 0
        index = 0
        threshold = 100

        f = open(f'{base_dir}/data-{index}', 'w+')
        # Serialize all blocks and save them to the current file
        for block in self._blocks[1:]:
            index = count // threshold
            # Create a new file if we have too many data in the current file
            if count != 0 and count % threshold == 0:
                f.close()
                f = open(f'{base_dir}/data-{index}', 'w+')

            count += 1

            # Serialized the block and save it to the current file
            data = Block.serialize(block)
            f.write(data + '\n')

        f.close()

    def read_blockchain(self, path='/data'):
        """Read the blockchain data 

        Parameters:
        ----------
        path : str
            the path to read the blockchain data
        """
        info_path = path + '/info'
        data_path = path + '/data'

        self._wallet_file = open(f'{self.base_dir}/info/wallet', 'a+')
        self._data_file = open(
            f'{self.base_dir}/data/data-{self._index}', 'a+')
        self._read_metadata(info_path)
        self._read_wallet_pool_data(info_path)
        self._read_transaction_data(info_path)
        self._read_genesis_data(data_path)
        self._read_blocks_data(data_path)

    def _read_metadata(self, path='/data/info'):
        """Read the blockchain metadata

        Parameters:
        ----------
        path : str
            the path to read the blockchain metadata
        """
        base_dir = os.getcwd() + path

        # Return if we cannot file the metadata file
        if not os.path.exists(base_dir):
            return

        # Read metadata from the file
        with open(f'{base_dir}/metadata', 'r') as f:
            # Process metadata
            raw_data = f.read().strip('\n')
            metadata = json.loads(raw_data)

            # Add data back to the blockchain
            self._bits = metadata['bits']
            self._subsidy = metadata['subsidy']
            self._height = metadata['height']
            self._count = metadata['count']
            self._index = metadata['index']
            self._root_address = metadata['root_address']

    def _read_wallet_pool_data(self, path='/data/info'):
        """Read the blockchain account data from the path

        Parameters:
        ----------
        path : str
            the path to read the blockchain account data
        """
        base_dir = os.getcwd() + path

        # Read address data
        with open(f'{base_dir}/wallet', 'r') as f:
            # Each line of data is an account
            for line in f:
                # Process account data
                raw_data = line.strip('\n')
                wallet = Wallet.deserialize(raw_data)
                self._wallet_pool.add_wallet(wallet)

    def _read_transaction_data(self, path='/data/info'):
        """Read the unprocessed transaction data

        Parameters:
        ----------
        path : str
            the path to read the transaction data
        """
        base_dir = os.getcwd() + path

        if not os.path.exists(f'{base_dir}/transactions'):
            return

        # Read transaction data
        with open(f'{base_dir}/transactions', 'r') as f:
            # Each line data is a transaction
            for line in f:
                # Process the transaction
                raw_data = line.strip('\n')
                tx = Transaction.deserialize(raw_data)

                # Add the transaction back to the transaction pool
                self._transaction_pool.add_transaction(tx)

        # Unknown: need to test whether it will affect the functionality
        with open(f'{base_dir}/transactions', 'w+') as f:
            pass

    def _read_genesis_data(self, path='/data/data'):
        """Read the genesis block data

        Parameters:
        ---------
        path : str
            the path to read the genesis block data
        """
        base_dir = os.getcwd() + path

        # Read the genesis block
        with open(f'{base_dir}/genesis', 'r') as f:
            data = f.read().strip('\n')
            block = Block.deserialize(data)
            self._blocks.append(block)

    def _read_blocks_data(self, path='/data/data'):
        """Read the blocks data

        Parameters:
        ----------
        path : str
            the path to read all blocks data
        """
        base_dir = os.getcwd() + path

        # Get all file in the directory
        dir_list = os.listdir(base_dir)

        # Remove genesis block data
        dir_list.remove(f'genesis')

        # Sort the file to get the right time sequence
        sort_dir = sorted(dir_list)

        # Read data from each file under the directory
        for file in sort_dir:
            with open(f'{base_dir}/{file}', 'r') as f:
                # Each line is a block
                for line in f:
                    # Process the block
                    data = line.strip('\n')

                    # Save the block back into the blockchain
                    block = Block.deserialize(data)
                    self._blocks.append(block)

    def print_blocks(self, height=-1, direction='back'):
        """Print blockchain data"""
        if height < 0:
            for block in self._blocks:
                print(block)
        else:
            if height == 0:
                print('Print nothing!')
            elif height > len(blockchain._blocks):
                print(
                    'Invalid Command: The height must be less than or equal to the height of the blockchain !!!')
            else:
                if direction and direction == 'back':
                    size = len(blockchain._blocks)
                    for i in range(size - 1, size - height - 1, -1):
                        print(blockchain._blocks[i])
                else:
                    for i in range(height):
                        print(blockchain._blocks[i])


def test_save_blocks():
    """Test the save aspect of the blockchain functions"""
    blockchain = Blockchain()

    try:
        blockchain.initialize('Eric Chen')
        wallets = [None for _ in range(11)]
        root_wallet = blockchain._root_wallet
        wallets[0] = root_wallet
        blockchain.increment_balance(wallets[0].address, 10000)
        # blockchain.increment_balance('Eric Chen', 1000000)

        for i in range(1, 11):
            wallet = blockchain.create_user(f'my address {i}')
            wallets[i] = wallet

        for i in range(1, 201):
            if blockchain.tx_num >= 100:
                blockchain.fire_transactions(wallets[0].address)

            winner = random.randint(1, 10)
            blockchain.add_transaction(
                wallets[0].address, wallets[winner].address, 80)
        if blockchain.tx_num >= 100:
            blockchain.fire_transactions(wallets[0].address)
    except ValueError as e:
        blockchain.save_blockchain()
    except KeyboardInterrupt:
        blockchain.save_blockchain()


def test_read_blocks():
    """Test the read aspect of the blockchain functions"""
    blockchain = Blockchain()
    blockchain.read_blockchain()
    wallets = [None for _ in range(11)]

    # Retrieve all wallet using brute-force
    for address, wallet in blockchain._wallet_pool.wallets:
        # Root address
        if wallet.name[-1] == 'n':
            wallets[0] = wallet
            continue

        num = int(wallet.name[-1])
        if num == 0:
            num = 10

        wallets[num] = wallet

    try:
        blockchain.increment_balance(wallets[0].address, 200000)

        for i in range(301, 1001):
            if blockchain.tx_num >= 100:
                blockchain.fire_transactions(wallets[0].address)

            winner = random.randint(1, 10)
            blockchain.add_transaction(
                wallets[0].address, wallets[winner].address, 80)

        if blockchain.tx_num >= 100:
            blockchain.fire_transactions(wallets[0].address)

        blockchain.save_blockchain()
        blockchain.print_blocks()
    except ValueError as e:
        blockchain.save_blockchain()
    except KeyboardInterrupt:
        blockchain.save_blockchain()


def test_signature():
    """Test the sign aspect of the blockchain functions"""
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
