import pprint

# TESTING MESSAGE
from message import Message, MESSAGE_DATA, MESSAGE_HASH

chat_message_1 = {MESSAGE_DATA: "Hello World From Blockchain"}
chat_message_2 = "{\"%s\": \"Hello World From Blockchain\", \"%s\": \"1b4c878aea01ffd70803426843f28d0c8f83342175528685bd7cf4a671a8466e\"}" % (MESSAGE_DATA, MESSAGE_HASH)
chat_message_3 = "Blockchain Is Great"

message_1 = Message(chat_message_1)
message_2 = Message.create(chat_message_3)
print(message_1)
print(message_2)
print(Message.parse(chat_message_2).valid())

# TESTING BLOCK
from block import Block, BLOCK_INDEX, BLOCK_NONCE, BLOCK_TIMESTAMP, BLOCK_PREV_HASH, BLOCK_DIFFICULTY, BLOCK_CONTENT, BLOCK_HASH, BLOCK_MERKLE_ROOT

block_data_1 = {
    BLOCK_INDEX         : 0,
    BLOCK_NONCE         : 0,
    BLOCK_TIMESTAMP     : 0,
    BLOCK_PREV_HASH     : "NONE",
    BLOCK_DIFFICULTY    : 1000,
}
block_data_2 = "{\"%s\": 0, \"%s\": 0, \"%s\": 0, \"%s\": \"NONE\", \"%s\": 1000, \"%s\": [\"{\\\"%s\\\": \\\"Hello World From Blockchain\\\", \\\"%s\\\": \\\"1b4c878aea01ffd70803426843f28d0c8f83342175528685bd7cf4a671a8466e\\\"}\"], \"%s\": \"5af7a60f7b6bc1a291096f1b85513a3a3faef6f4bd54175ab107978243f0388a\", \"%s\": \"cbc750e95e066eb3aa56f3392c3dbd34b8988e53ee8b899b1e3b6f48393cb638\"}" % (
    BLOCK_INDEX, 
    BLOCK_NONCE, 
    BLOCK_TIMESTAMP, 
    BLOCK_PREV_HASH, 
    BLOCK_DIFFICULTY,
    BLOCK_CONTENT, 

    MESSAGE_DATA,
    MESSAGE_HASH,

    BLOCK_MERKLE_ROOT,
    BLOCK_HASH
)

block_1 = Block(block_data_1, container=Message)
block_1.append(chat_message_2)
print(block_1)
print(Block.parse(block_data_2).valid())