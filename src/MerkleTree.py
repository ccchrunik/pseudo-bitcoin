import hashlib
import base64


class MerkleTree:
    """
    A class used for promise the data integrity of all transactions in the block

    ...

    Attributes
    ----------
    root : MerkleNode
        the root node of the merkle tree instance

    Methods
    ----------
    hash() : str (base64)
        return the top hash of the merkle tree

    Static Methods
    ----------
    new_merkle_tree(arr) : MerkleTree
        construct a new MerkleTree instance with the given arr input
    """

    def __init__(self, root):
        """
        Parameters: 
        ----------
        root : MerkleNode
            the root node of the merkle tree instance
        """
        self.root = root

    def __str__(self):
        """Return the top hash of the merkle tree"""
        return self.hash()

    def __repr__(self):
        """Return the top hash of the merkle tree"""
        return self.hash()

    def hash(self):
        """Return the top hash of the merkle tree

        Returns
        ----------
        self.root.data : str (base64)
            return the base64 encoded top hash value
        """
        return self.root.data

    @staticmethod
    def new_merkle_tree(arr):
        """Construct a new MerkleTree instance with the given arr input

        Parameters
        ----------
        arr : List[str]
            a list of transactions strings

        Returns
        ----------
        merkle_tree : MerkleNode
            the root node of the merkle tree instance
        """
        # The list for holding all nodes
        nodes = []

        # Duplicate the last transaction if the number of transactions is odd
        if len(arr) % 2 != 0:
            arr.append(arr[-1])

        # Create a node for each transaction and add it into nodes
        for i in range(len(arr)):
            node = MerkleNode(None, None, arr[i])
            nodes.append(node)

        # Iteratively build the merkle tree
        for i in range(len(arr)):
            # the list of the new higher level of nodes
            new_level = []

            # Break the loop if we left only one node
            if len(nodes) == 1:
                break
            # Duplicate the last node if the number of nodes is odd
            elif len(nodes) % 2 != 0:
                nodes.append(nodes[-1])

            # Create a higher level node for for each two nodes
            for j in range(0, len(nodes), 2):
                # Compute the hash of the two nodes' data
                m = hashlib.sha256()
                m.update(nodes[j].data.encode())
                m.update(nodes[j+1].data.encode())
                hash = base64.b64encode(m.digest()).decode()

                # Create a new node and append to the nodes list
                node = MerkleNode(nodes[j], nodes[j+1], hash)
                new_level.append(node)

            # Move to the next higher level of nodes
            nodes = new_level

        # Create a MerkleTree instance with its root node as the first node in nodes
        merkle_tree = MerkleTree(nodes[0])

        return merkle_tree


class MerkleNode:
    """
    An internal class for the class MerkleTree

    ...  

    Attributes:
    ----------
    left : MerkleNode
        the left child node of this node
    right : MerkleNode
        the right child node of this node
    data : str
        the value of the node, which is a transaction in a block
    """

    def __init__(self, left=None, right=None, data=None):
        """
        Parameters:
        ----------
        left : MerkleNode
            the left child node of this node
        right : MerkleNode
            the right child node of this node
        data : str
            the value of the node, which is a transaction in a block
        """

        self._left = left
        self._right = right
        self._data = data

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, left):
        self._left = left

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, right):
        self._right = right

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
