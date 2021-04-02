from hashlib import sha256
import base64


class MerkleTree:
    def __init__(self, node):
        self.root = node

    @staticmethod
    def new_merkle_tree(arr):
        nodes = []

        if len(arr) % 2 != 0:
            arr.append(arr[-1])

        for i in range(len(arr)):
            node = MerkleNode(None, None, arr[i])
            nodes.append(node)

        for i in range(len(arr)):
            new_level = []
            if len(nodes) == 1:
                break
            elif len(nodes) % 2 != 0:
                nodes.append(nodes[-1])

            for j in range(0, len(nodes), 2):
                m = sha256()
                m.update(nodes[j].data.encode())
                m.update(nodes[j+1].data.encode())
                hash = base64.b64encode(m.digest()).decode()
                node = MerkleNode(nodes[j], nodes[j+1], hash)
                new_level.append(node)

            nodes = new_level

        merkle_tree = MerkleTree(nodes[0])

        return merkle_tree

    def hash(self):
        return self.root.data


class MerkleNode:
    def __init__(self, left=None, right=None, data=None):
        self.left = left
        self.right = right
        self.data = data
