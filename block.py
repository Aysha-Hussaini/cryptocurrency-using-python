import time
from crypto_hash import crypto_hash
class Block:
    """
    Block : a unit of storage
    Store transactions in a blockchain that supports cryptocurrency
    """

    def __init__(self, data, timestamp, last_hash, hash):
        self.data = data
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash

    def __repr__(self):
        return (
            'Block('
            f'data :{self.data}, '
             f'timestamp :{self.timestamp}, '
            f'last_hash :{self.last_hash}, '
            f'hash :{self.hash} )'
        )

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the giveb last_block and data.
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        hash = crypto_hash(timestamp, last_hash, data)

        return Block(data, timestamp, last_hash, hash)

    @staticmethod
    def genesis():
        """
        Generate a genesis block.
        """
        return Block([], 1, 'genesis_last_hash', 'genesis_hash')

def main():
    #print(f'block.py __name__ : {__name__}'
    genesis_block = Block.genesis()
    block = Block.mine_block(genesis_block, 'foo')

    print(block)

if __name__ == "__main__":
    main()