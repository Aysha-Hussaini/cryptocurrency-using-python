
class Blockchain:
    """
    Blockchain is a open distributed and decentralized ledger of transactions, implemented as list of blocks-data sets of transactions
    """
    def __init__(self):
        self.chain = []

    def add_block(self, data):
        self.chain.append(Block(data))

    def __repr__(self):
        return f'Blockchain :{self.chain}'

blockchain = Blockchain()

blockchain.add_block('one')
blockchain.add_block('two')
blockchain.add_block('three')

print(blockchain)