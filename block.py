from hashlib import sha256
import json, sys

from config import BLOCK_CONTAINER

BLOCK_HASH          = "hash"
BLOCK_INDEX         = "index"
BLOCK_NONCE         = "nonce"
BLOCK_TIMESTAMP     = "timestamp"
BLOCK_PREV_HASH     = "previous"
BLOCK_DIFFICULTY    = "difficulty"
BLOCK_MERKLE_ROOT   = "merkle"
BLOCK_CONTENT       = "content"

class Block:
    def __init__(self, data, container=BLOCK_CONTAINER):
        self.container = container
        self.data = data
        if not BLOCK_CONTENT in self.data or not len(self.data[BLOCK_CONTENT]):
            self.data[BLOCK_CONTENT]        = []
            self.data[BLOCK_MERKLE_ROOT]    = ""

    def __getitem__(self, key):
        return self.data[key]
        
    def hash(self):
        header = "\t".join(str(i) for i in [
            self.data[BLOCK_INDEX],
            self.data[BLOCK_NONCE],
            self.data[BLOCK_TIMESTAMP],
            self.data[BLOCK_PREV_HASH],
            self.data[BLOCK_DIFFICULTY],
            self.data[BLOCK_MERKLE_ROOT]
        ])
        return sha256(header.encode())

    def hexdigest(self):
        return self.hash().hexdigest()

    def num_hash(self):
         return int.from_bytes(self.hash().digest(), byteorder=sys.byteorder)

    def append(self, content, no_build_tree=False):
        if not type(content) is str:
            content = str(content)

        if not content in self.data[BLOCK_CONTENT]:
            self.data[BLOCK_CONTENT].append(content)
            self.recalculate_tree()

    def recalculate_tree(self):
        if len(self.data[BLOCK_CONTENT]):
            self.data[BLOCK_MERKLE_ROOT] = self.get_merkle_tree(
                [ self.container.parse(e).hexdigest() for e in self.data[BLOCK_CONTENT] ], 
                root=True
            )

    def get_merkle_tree(self, collection, root=False):
        if len(collection) == 1 and not root:
            return collection[0]

        merges = []
        i = 0
        while i < len(collection):
            value = collection[i]
            if i < len(collection) - 1:
                value += collection[i + 1]
            else:
                value += value
            merges.append(sha256(value.encode()).hexdigest())
            i += 2

        return self.get_merkle_tree(merges)

    def __str__(self):
        return json.dumps({**self.data, BLOCK_HASH: self.hexdigest()})

    @staticmethod
    def parse(string, container=BLOCK_CONTAINER):
        return Block(json.loads(string), container)

    # Checks if a builded block is valid
    def valid(self, container=BLOCK_CONTAINER):
        return self.num_hash() < self.data[BLOCK_DIFFICULTY]