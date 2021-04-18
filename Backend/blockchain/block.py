import time
from Backend.util.crypto_hash import crypto_hash
from Backend.config import MINERATE
from Backend.util.hex_to_binary import hex_to_binary
##globalvariable
GENESIS_DATA = {
    'data' : [],
    'timestamp' : 1,
    'last_hash' : 'genesis_last_hash',
    'hash' : 'genesis_hash',
    'difficulty' : 3,
    'nonce' : 'genesis_nonce'
}

class Block:
    """
    Block : a unit of storage
    Store transactions in a blockchain that supports cryptocurrency
    """

    def __init__(self, data, timestamp, last_hash, hash, difficulty, nonce):
        self.data = data
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        return (
            'Block('
            f'data :{self.data}, '
            f'timestamp :{self.timestamp}, '
            f'last_hash :{self.last_hash}, '
            f'hash :{self.hash}, '
            f'difficulty : {self.difficulty}, '
            f'nonce : {self.nonce} )'
        )

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the given last_block and data, until a block hash is found that meets
        difficulty requirement of proof of work
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block, timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)



        return Block(data, timestamp, last_hash, hash, difficulty, nonce)

    @staticmethod
    def genesis():
        """
        Generate a genesis block.
        """
        # return Block (
        #     'data' = GENESIS_DATA['data'],
        #     'timestamp' = GENESIS_DATA['timestamp'],
        #     'last_hash' = GENESIS_DATA['last_hash'],
        #     'hash' = GENESIS_DATA['hash'], 
        #     )

        return Block(**GENESIS_DATA) #This syntax unpacks as above 

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        Calculate dificulty according to MINE RATE
        Increase difficulty for quickly mined blocks.
        Decrease difficulty for slowly mined blocks.
        """
        if (new_timestamp - last_block.timestamp) < MINERATE:
            return last_block.difficulty + 1

        
        if (last_block.difficulty -1) > 0:
            return last_block.difficulty - 1
        
        return 1


def main():
    #print(f'block.py __name__ : {__name__}'
    genesis_block = Block.genesis()
    block = Block.mine_block(genesis_block, 'foooooooooooooo')

    print(block)

if __name__ == "__main__":
    main()