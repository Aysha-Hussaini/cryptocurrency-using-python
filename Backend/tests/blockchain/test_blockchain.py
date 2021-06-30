import pytest

from Backend.blockchain.blockchain import Blockchain
from Backend.blockchain.block import GENESIS_DATA
from Backend.wallet.transaction import Transaction
from Backend.wallet.wallet import Wallet
 
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
        blockchain.add_block([Transaction(Wallet(), 'recipient', i).to_json()])
    
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

def test_valid_transaction_chain(blockchain_blocks):
    Blockchain.is_valid_transaction_chain(blockchain_blocks.chain)

def test_duplicate_invalid_transaction(blockchain_blocks):
    transaction = Transaction(Wallet(), 'recipient', 40).to_json()

    blockchain_blocks.add_block([transaction, transaction])
    with pytest.raises(Exception, match = 'is not unique'):
        Blockchain.is_valid_transaction_chain(blockchain_blocks.chain)

def test_multiple_rewards_in_single_block(blockchain_blocks):
    reward_1 = Transaction.reward_transaction(Wallet()).to_json()
    reward_2 = Transaction.reward_transaction(Wallet()).to_json()

    blockchain_blocks.add_block([reward_1, reward_2])

    with pytest.raises(Exception, match = 'one mining reward per block'):
        Blockchain.is_valid_transaction_chain(blockchain_blocks.chain)

def test_is_valid_transaction_chain_bad_transaction(blockchain_blocks):
    bad_transaction = Transaction(Wallet(), 'recipient', 7)
    bad_transaction.input['signature'] = Wallet().sign(bad_transaction.output)
    blockchain_blocks.add_block([bad_transaction.to_json()])

    with pytest.raises(Exception):
        Blockchain.is_valid_transaction_chain(blockchain_blocks.chain)

def test_is_valid_transaction_chain_bad_balance(blockchain_blocks):
    wallet = Wallet()
    bad_transaction = Transaction(wallet, 'recipient', 1)
    bad_transaction.output[wallet.address] = 9000
    bad_transaction.input['amount'] = 9001
    bad_transaction.input['signature'] = wallet.sign(bad_transaction.output)

    blockchain_blocks.add_block([bad_transaction.to_json()])

    with pytest.raises(Exception, match= 'has an invalid amount'):
        Blockchain.is_valid_transaction_chain(blockchain_blocks.chain)
