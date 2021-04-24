import pytest

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

@pytest.fixture
def blockchain_blocks():
    blockchain = Blockchain()
    for i in range(3):
        blockchain.add_block(i)
    
    return blockchain

def test_is_valid_chain(blockchain_blocks):    
    Blockchain.is_valid_chain(blockchain_blocks.chain)

def test_is_valid_chain_bad_genesis(blockchain_blocks):
    
    blockchain_blocks.chain[0].hash = 'fff567_evil' 

    with pytest.raises(Exception, match = 'Genesis block must be valid'):
        Blockchain.is_valid_chain(blockchain_blocks.chain)

def test_replace_chain(blockchain_blocks):
    blockchain = Blockchain()
    blockchain.replace_chain(blockchain_blocks.chain)

    assert blockchain.chain == blockchain_blocks.chain

def test_replace_chain_not_longer(blockchain_blocks):
    blockchain = Blockchain()
   
    with pytest.raises(Exception, match = 'Cannot replace, incoming chain must be longer'):
        blockchain_blocks.replace_chain(blockchain.chain)

def test_replace_chain_invalid(blockchain_blocks):
    blockchain = Blockchain()
    blockchain_blocks.chain[2].hash = 'ffff_evil'

    with pytest.raises(Exception, match = 'Cannot replace, incoming chain is invalid'):
        blockchain.replace_chain(blockchain_blocks.chain)

