import requests, time, random, sys
import hashlib, math

from resources import lock, firsts
from config import SPACE, GENESIS_BLOCK, BLOCK_CONTAINER, MINING_TIME, MINING_ROUND, MINING_LIMIT
from block import Block, BLOCK_CONTENT, BLOCK_DIFFICULTY, BLOCK_HASH, BLOCK_INDEX, BLOCK_MERKLE_ROOT, BLOCK_TIMESTAMP, BLOCK_PREV_HASH, BLOCK_NONCE

STATE_CHAIN = "C"
STATE_BEST  = "B"

class Blockchain:
    def __init__(self, genesis=GENESIS_BLOCK, container=BLOCK_CONTAINER):
        self.state = {
            STATE_CHAIN: [Block.parse(GENESIS_BLOCK, BLOCK_CONTAINER)], # Blocks of the blockchain
            STATE_BEST : 0
        }
        self.container    = container
        self.mining_alive = True
        self.pending      = []

    def __getitem__(self, key):
        return self.state[key]

    def add_content(self, content):
        lock.acquire()
        self.pending.append(content)
        lock.release()

    def bestblock(self):
        return self.state[STATE_BEST]
    
    # This method performs the mining procedure.
    def mine(self, broadcast=None):
        # There is defined a class variable "mining_alive" that defines if the mining loop should be alive.
        while self.mining_alive:
            time.sleep(5)
            if self.pending:
                data = {BLOCK_CONTENT: self.pending, BLOCK_MERKLE_ROOT: ''}
                prev = self.state[STATE_CHAIN][self.state[STATE_BEST]]
                data[BLOCK_HASH], data[BLOCK_NONCE], data[BLOCK_DIFFICULTY] = self.get_header(prev)
                data[BLOCK_INDEX] = prev[BLOCK_INDEX] + 1
                data[BLOCK_PREV_HASH] = prev[BLOCK_HASH]
                data[BLOCK_TIMESTAMP] = time.time()
                b = Block(data, self.container)
                b.recalculate_tree()
                self.setState(b)
                print(b)


    def get_header(self, prev_block):
        initial_difficulty = prev_block[BLOCK_DIFFICULTY]
        hash_ = prev_block[BLOCK_HASH]
        
        # checks the current time
        start_time = time.time()

        # makes a new block wich includes the hash from the previous block
        new_block = 'transaction_' + hash_

        # find a valid nonce for the new block
        hash_, nonce = self.proof_of_work(new_block)

        end_time = time.time()
        # TODO: Si el tiempo transcurrido excede un tiempo determinado, bajar la dificultad
        return hash_, nonce, initial_difficulty


    def proof_of_work(self, header):
        # calculate the difficulty target
        diff = SPACE
        init = start = time.time()
        # target = 2**difficulty
        for nonce in range(2**32):
            text = f'{header}_{nonce}'
            h = hashlib.sha256(text.encode()).digest()
            # check if this is a valid result, below the target
            n = int.from_bytes(h, byteorder=sys.byteorder)            
            if n < diff:
                return h, nonce
        return None, nonce

    # Check if the blockchain can grow given a state and a block
    @staticmethod
    def check(state, block):
        last_block = state[STATE_CHAIN][state[STATE_BEST]]
        if block[BLOCK_PREV_HASH] != last_block[BLOCK_HASH] or not block.valid():
            return False
        return True


    def setState(self, item):
        lock.acquire()
        
        if Blockchain.check(self.state, item):
            index = item[BLOCK_INDEX]
            while not len(self.state[STATE_CHAIN]) > index:
                self.state[STATE_CHAIN].append(None)
            self.state[STATE_CHAIN][index] = item
            self.state[STATE_BEST] = index
            

        for c in item[BLOCK_CONTENT]:
            self.pending.remove(c)
        
        if len(item[BLOCK_CONTENT]):
            print(item[BLOCK_CONTENT])

        lock.release()

B = Blockchain()

if __name__ == "__main__":
    from resources import broadcast
    from threading import Thread

    def miner(broadcast_function):
        B.mine(broadcast_function)

    thr = Thread(target=miner, args=[broadcast])
    thr.start()

    # while True:
    #     message = input(">>> ")
    #     if message == "exit":
    #         B.mining_alive = False
    #         break
    #     B.add_content(str(BLOCK_CONTAINER.create(message)))
    B.add_content(str(BLOCK_CONTAINER.create('Hola')))
    B.add_content(str(BLOCK_CONTAINER.create('soy')))
    B.add_content(str(BLOCK_CONTAINER.create('Hola')))
