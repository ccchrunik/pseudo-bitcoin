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
    set_hash() : void
        compute the hash of the block and append this and nonce to the block attributes

    create_merkle_tree() : void 
        create a merkle tree based on the transactions

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
        self.height = prev_height + 1
        self.time = time
        self.bits = bits
        self.nonce = nonce
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.hash = ''
        self.merkle_tree = self.create_merkle_tree()

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
                       f'Merkle hash: {self.merkle_tree.hash()}',
                       f"---"]

        info = '\n'.join(info_pieces)

        return info

    def set_hash(self):
        """Compute the hash of the block"""

        # Create a PoW instance and pass self block as the argument
        Pow = PoW(self)

        # Run the PoW process to get the nonce and the hash value
        self.nonce, self.hash = Pow.run()

    def create_merkle_tree(self):
        """Construct a merkle tree based on the transactions"""
        return MerkleTree.new_merkle_tree(self.transactions)

    # serialize a block

    @staticmethod
    def serialize(block):
        """Serialize a block instance

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
             'transactions': block.transactions, 'prev_hash': block.prev_hash, 'hash': block.hash, 'merkle_hash': block.merkle_tree.hash()}

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

        return block
