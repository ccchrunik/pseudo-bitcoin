# standard modules
import sys
import os
import hashlib
import json
import base64
import time
from configparser import ConfigParser
# my modules
from PoW import PoW
from MerkleTree import MerkleTree


class Block:
    """
    A class which is the basic block object of a blockchain.

    ...

    Attributes:
    ----------
    height : int
        the position of the block in the blockchain

    time : float (unix timestamp)
        the creation time of the block

    bits : int 
        the hardness of the PoW, the bigger is the harder 

    nonce : int
        the nonce of the block computed in the PoW process

    transactions : List[str]
        the transactions of the block

    prev_hash : byte
        the hash value of the previous block

    hash : byte
        the hash value of this block

    merkle_tree : MerkleTree
        the constructed merkle tree based on the transactions

    Methods: 
    ----------
    set_hash() : None
        compute the hash of the block and append this and nonce to the block attributes

    _create_merkle_tree() : None
        create a merkle tree based on the transactions

    print_block() : None
        print the block


    Static Methods:
    ----------
    serialize(block: Block) : str 
        return the serialization of the block

    deserialize(raw_data: str) : Block
        deserialize the raw_data can create the Block instance based on the given data
    """

    def __init__(self, prev_height, time, bits, nonce, transactions, prev_hash):
        """
        Parameters:
        ----------
        height : int
            the position of the block in the blockchain

        time : float (unix timestamp)
            the creation time of the block

        bits : int 
            the hardness of the PoW, the bigger is the harder 

        nonce : int
            the nonce of the block computed in the PoW process

        transactions : List[str]
            the transactions of the block

        prev_hash : byte
            the hash value of the previous block

        hash : byte
            the hash value of this block
        """
        self._height = prev_height + 1
        self._time = time
        self._bits = bits
        self._nonce = nonce
        self._transactions = transactions
        self._prev_hash = prev_hash
        self._hash = ''
        self._merkle_tree = self._create_merkle_tree()

    def __str__(self):
        """the string representation of the block"""

        info_pieces = ["Block Information: ",
                       "---",
                       f"height: {self.height}",
                       f"time: {self.time}",
                       f"hardness: {self.bits}",
                       f"nonce: {self.nonce}",
                       f"transactions: {str(self.transactions)}",
                       f"previous hash: {self.prev_hash}",
                       f"hash: {self.hash}",
                       f'Merkle hash: {self.merkle_tree.hash}',
                       f"---\n"]

        info = '\n'.join(info_pieces)

        return info

    @property
    def height(self):
        """The position of the block in the blockchain"""
        return self._height

    @property
    def time(self):
        """The time the block being created"""
        return self._time

    @property
    def bits(self):
        """The hardness of the PoW when the block was created"""
        return self._bits

    @property
    def nonce(self):
        """The nonce of the block"""
        return self._nonce

    @property
    def transactions(self):
        """The transactions list of the block"""
        return self._transactions

    @property
    def prev_hash(self):
        """The hash of the previous block"""
        return self._prev_hash

    @property
    def hash(self):
        """The hash of the block"""
        return self._hash

    @hash.setter
    def hash(self, hash):
        self._hash = hash

    @property
    def merkle_tree(self):
        """The merkle tree of the block"""
        return self._merkle_tree

    @merkle_tree.setter
    def merkle_tree(self, merkle_tree):
        self._merkle_tree = merkle_tree

    def print_block(self):
        """Print the block"""
        print(self)

    def set_hash(self):
        """Compute the hash of the block"""

        # Create a PoW instance and pass self block as the argument
        Pow = PoW(self)

        # Run the PoW process to get the nonce and the hash value
        self._nonce, self._hash = Pow.run()

    def _create_merkle_tree(self):
        """Construct a merkle tree based on the transactions

        Returns:
        ----------
        merkle_tree : MerkleTree
            the merkle tree of the block based on the transactions
        """
        return MerkleTree.new_merkle_tree(self.transactions)

    @staticmethod
    def serialize(block):
        """Serialize a block

        Parameters: 
        ----------
        block : Block
            the block instance to be serialized

        Returns:
        ---------
        data : str
            the json formatted string data to be stored in a file
        """

        # Create a dictionary to be dumped by the json module
        d = {'height': block.height, 'bits': block.bits, 'time': block.time, 'nonce': block.nonce,
             'transactions': block.transactions, 'prev_hash': block.prev_hash, 'hash': block.hash, 'merkle_hash': block.merkle_tree.hash}

        # Use json module to dump data
        data = json.dumps(d)

        return data

    # deserialize a block
    @staticmethod
    def deserialize(raw_data):
        """Deserialize a data string back into a Block instance

        Parameters:
        ----------
        raw_data : str 
            the json formatted string data to be deserialized

        Returns: 
        ----------
        block : Block
            the deserialized Block instance

        """

        # Load data to the json module
        data = json.loads(raw_data)

        # Retrieve each attributes from the data
        height = data['height']
        time = data['time']
        bits = data['bits']
        nonce = data['nonce']
        transactions = data['transactions']
        prev_hash = data['prev_hash']

        # Create a Block instance and also set the hash value to the block
        block = Block(height - 1, time, bits, nonce, transactions, prev_hash)
        block.hash = data['hash']
        block._create_merkle_tree()

        return block
