from Backend.blockchain.block import Block
class Blockchain:
    """
    Blockchain is a open distributed and decentralized ledger of transactions, implemented as list of blocks-data sets of transactions
    """
    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        return f'Blockchain :{self.chain}'

def main():
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')
    blockchain.add_block('three')
    print(blockchain)
    print(f'blockchain.py __name__ : {__name__}')

if __name__ == "__main__": 
    main()