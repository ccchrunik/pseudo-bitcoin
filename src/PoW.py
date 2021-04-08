# standard modules
import hashlib
import json
import base64
import time
from configparser import ConfigParser


class PoW:
    """
    A class for simulating the Proof of Work (PoW) process of the blockchain.

    ... 

    Attributes:
    ----------
    block : Block
        the Block instance ready for hash computation

    threshold : int
        the threshold of the computation, if less than thershold, meaning we find an valid nonce

    salt : str
        used for improve the security of the hash computation

    tx_data : str   
        the joined transaction data used for hash computation     

    prev_hash : str
        the base64 encoded hash value 

    data_prefix : str
        the combined data from all the blocks data to be hashed except for the nonce

    data : str
        data_prefix + data, generated to compute the valid hash for the block

    Methods:
    ---------- 
    run() : int, str
        compute and then return the nonce and the valid hash to the caller

    prepare(nonce) : None
        prepared for candidate hash using the given nonce

    validate() : bool
        check if the computed hash is less than the threshold
    """

    def __init__(self, block):
        """
        Parameters: 
        ----------
        block : Block
            the block to compute the hash value
        """

        # Initialization
        self._block = block

        # Set the target threshold
        self._threshold = 1 << (256 - block.bits)

        # Read configuration
        # cfg = ConfigParser()
        # cfg.read('./config.txt')
        # self.salt = cfg['secret']['salt'].encode()

        # Prepare header information
        self._txdata = ':'.join(block.transactions)

        # Combined all data into one string
        self._data_prefix = str(block.height).encode() + str(block.time).encode() + str(block.bits).encode(
        ) + self._txdata.encode() + block.prev_hash.encode() + block.merkle_tree.hash.encode()

        # Other Attributes
        self._hash = None
        self._data = None

    @property
    def block(self):
        """The block"""
        return self._block

    @property
    def threshold(self):
        """The threshold for the hash to be evaluated as valid or not"""
        return self._threshold

    @property
    def hash(self):
        """The hash of the block"""
        return self._hash

    @hash.setter
    def hash(self, hash):
        self._hash = hash

    @property
    def data(self):
        """The block data to be hashed"""
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    def run(self):
        """Return the nonce and valid hash to the caller function

        Returns:
        ----------
        nonce : int
            nonce to produce valid hash

        hash : str
            the base64 encoded valid hash
        """
        nonce = 0
        # Increment nonce by once after each loop until we find a valid one
        while True:
            # Generate hash and save it to self.hash
            self._prepare_data(nonce)

            # If the hash is valid, return the nonce and the base64 encoded hash
            if self._validate():
                # Using base64 encoding for storage
                hash_data = base64.b64encode(
                    self._hash.to_bytes(32, 'big')).decode()
                return nonce, hash_data

            nonce += 1

    def _prepare_data(self, nonce):
        """
        Parameters: 
        ---------- 
        nonce : int 
            the nonce for computing the hash value of this round
        """
        self._data = self._data_prefix + str(nonce).encode()

        # Generate the hash of the block
        m = hashlib.sha256()
        m.update(self._data)
        self._hash = int.from_bytes(m.digest(), 'big')

        # Print the hash to the console
        print_hash = base64.b64encode(
            int.to_bytes(self.hash, 32, 'big')).decode()
        print(
            f'nonce = {nonce}, hash = {print_hash}', end='\r')

    def _validate(self):
        """Check if the computed hash is less than the threshold

        Returns:
        result : bool
            whether the hash is less than the threshold
        """
        if self._hash < self._threshold:
            return True
        else:
            return False
