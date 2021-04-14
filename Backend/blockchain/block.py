import time
from Backend.util.crypto_hash import crypto_hash

##globalvariable
GENESIS_DATA = {
    'data' : [],
    'timestamp' : 1,
    'last_hash' : 'genesis_last_hash',
    'hash' : 'genesis_hash',
    'difficulty' : 5,
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
        difficulty = last_block.difficulty
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hash[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
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

def main():
    #print(f'block.py __name__ : {__name__}'
    genesis_block = Block.genesis()
    block = Block.mine_block(genesis_block, 'safi')

    print(block)

if __name__ == "__main__":
    main()