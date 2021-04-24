from Backend.blockchain.block import Block, GENESIS_DATA

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
            raise Exception('Cannot replace, incoming chain is invalid : {e}')

        self.chain = chain

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



def main():
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')
    blockchain.add_block('three')
    blockchain.add_block('5')
    blockchain.add_block(1)
    print(blockchain)
  
   

if __name__ == "__main__": 
    main()