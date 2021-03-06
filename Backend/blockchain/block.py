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

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_json(self):
        """
        Serialize blocks into a its dictionary representation 
        """
        return self.__dict__


    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the given last_block and data, until a block hash is found that meets
        difficulty requirement of proof of work.
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
        #This syntax unpacks as above
        return Block(**GENESIS_DATA)  

    @staticmethod
    def from_json(block_json):
        """
        Deserialize block_json format into block instance
        """
        return Block(**block_json)

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        Calculate difficulty according to MINE RATE
        Increase difficulty for quickly mined blocks.
        Decrease difficulty for slowly mined blocks.
        """
        if (new_timestamp - last_block.timestamp) < MINERATE:
            return last_block.difficulty + 1

        
        if (last_block.difficulty -1) > 0:
            return last_block.difficulty - 1
        
        return 1
    
    @staticmethod
    def is_valid(last_block, block):
        """
        Validate block by enforcing the following rules:
            -The block must have the proper last_hash ref
            -The block must meet the proof of work requirement
            -The difficulty must only adjust by 1
            -The block hash is valid combination of block fields
        """
        if block.last_hash != last_block.hash:
            raise Exception('The block last_hash must be correct')
        if hex_to_binary(block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception('The proof of work requirement not met')
        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception('Block difficulty must only adjust by 1')
        
        regenerated_hash = crypto_hash(
            block.data, 
            block.timestamp, 
            block.last_hash, 
            block.difficulty, 
            block.nonce)

        if block.hash != regenerated_hash:
            raise Exception('Block hash must be correct')


def main():
    genesis_block = Block.genesis()
    bad_block = Block.mine_block(genesis_block, 'foo')
    
    try:
        Block.is_valid(genesis_block, bad_block)
        print(' NOT A BAD BLOCK')
        print(f'bad_block : {bad_block}' )
    except Exception as e:
        print (f'is_valid_block: {e}')


if __name__ == "__main__":
    main()