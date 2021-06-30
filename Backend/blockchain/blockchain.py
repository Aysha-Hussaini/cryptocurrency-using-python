from Backend.blockchain.block import Block, GENESIS_DATA
from Backend.wallet.transaction import Transaction
from Backend.wallet.wallet import Wallet
from Backend.config import MINING_REWARD_INPUT
class Blockchain:
    """
    Blockchain is a open distributed and decentralized ledger of transactions, implemented 
    as list of blocks-data sets of transactions
    """
    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        return f'Blockchain :{self.chain}'

    def replace_chain(self, chain):
        """
        Replaces local chain with incoming chain if following applies:
        -incoming chain must be longer than local one.
        -incoming chain is formatted properly- call is_valid_chain to check
        """
        #chain-> incoming chain
        if len(chain) <= len(self.chain):
            raise Exception('Cannot replace, incoming chain must be longer')
        
        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace, incoming chain is invalid : {e}')

        self.chain = chain

    def to_json(self):
        """
        The goal of this function is to serialize the blockchain into lists of blocks.
        """

        return list (map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def from_json(chain_json):
        """
        Deserialize a list of serialized blocks into blockchain instance.
        The result will contain a chain list of block instances.
        """
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda block_json: Block.from_json(block_json), chain_json))
        return blockchain
    

    @staticmethod
    def is_valid_chain(chain):
        """
        Validates entire incoming  chain

        It should enforce following rules:
        -chain must start with genesis block
         -block must be formatted correctly
        """

        if chain[0] != Block.genesis():
            raise Exception ('Genesis block must be valid' )
            

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]

            Block.is_valid(last_block, block)

        Blockchain.is_valid_transaction_chain(chain)

    @staticmethod
    def is_valid_transaction_chain(chain):
        """
        Enfoce the rules of a chain composed of blocks contanining transactions.
            -Each transaction must appear only once in the chain.
            -There can only be one mining reward per block.
            -Each transaction must be valid.
        """
        transaction_ids = set()
        #set is used because it is unchangeable and duplicates are not allowed.

        for i in range(len(chain)): 
            block = chain[i]
            has_mining_reward = False

            for transaction_json in block.data:
                transaction = Transaction.from_json(transaction_json)
                
                if transaction.id in transaction_ids:
                    raise Exception(f'Transaction id - {transaction.id} is not unique')

                transaction_ids.add(transaction.id)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward == True:
                        raise Exception('There can be only one mining reward per block'\
                             f'Check block with hash: {block.hash}'
                        )
                    has_mining_reward = True
                else:
                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:i]
                    historic_balance = Wallet.calculate_balance(
                        historic_blockchain,
                        transaction.input['address']
                    )

                    if historic_balance != transaction.input['amount']:
                        raise Exception(f'Transaction- {transaction.id} has an invalid amount')

                Transaction.validate_transaction(transaction)

def main():
    blockchain = Blockchain()
    
    print(blockchain)
  
   

if __name__ == "__main__": 
    main()