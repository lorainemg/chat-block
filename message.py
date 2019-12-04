from hashlib import sha256
import json, sys

MESSAGE_HASH = "hash"
MESSAGE_DATA = "data"

class Message:
    def __init__(self, data):
        self.data = data

    def __getitem__(self, key):
        return self.data[key]
        
    def hash(self):
        return sha256(self.data[MESSAGE_DATA].encode())

    def hexdigest(self):
        return self.hash().hexdigest()

    def __hash__(self):
        return int.from_bytes(self.hash().digest(), byteorder=sys.byteorder)

    def __str__(self):
        return json.dumps({ **self.data, MESSAGE_HASH: self.hexdigest() })

    def __eq__(self, other):
        if type(other) == str:
            return hash(self) == hash(Message.parse(other))
        else:
            return hash(self) == hash(other)

    def valid(self):
        return self.hexdigest() == self.data[MESSAGE_HASH]

    @staticmethod
    def parse(string):
        return Message(json.loads(string))

    @staticmethod
    def create(string):
        return Message({MESSAGE_DATA: string})