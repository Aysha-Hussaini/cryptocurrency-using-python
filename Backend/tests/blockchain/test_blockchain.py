from Backend.blockchain.blockchain import Blockchain
from Backend.blockchain.block import GENESIS_DATA
 
def test_blockchain():
    blockchain = Blockchain()
    assert blockchain.chain[0].hash == GENESIS_DATA['hash']

def test_add_block():
    blockchain = Blockchain()
    data = 'test-data'
    blockchain.add_block(data)

    #assertion after adding block to the blockchain
    assert blockchain.chain[-1].data == data