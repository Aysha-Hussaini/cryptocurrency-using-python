import pytest
import time
from Backend.blockchain.block import Block, GENESIS_DATA
from Backend.config import MINERATE, SECONDS
from Backend.util.hex_to_binary import hex_to_binary

def test_mine_block():
    last_block = Block.genesis()
    data = 'test-data'
    block = Block.mine_block(last_block, data)

    assert isinstance (block, Block)
    #isinstance checks if the instance is object of a class 

    assert block.data == data

    assert block.last_hash == last_block.hash

    assert hex_to_binary(block.hash)[0:block.difficulty] == '0' * block.difficulty

def test_genesis():
    genesis = Block.genesis()

    assert isinstance(genesis, Block)
    # assert genesis.data == GENESIS_DATA['data']
    # assert genesis.timestamp == GENESIS_DATA['timestamp']
    # assert genesis.last_hash == GENESIS_DATA['last_hash']
    # assert genesis.hash == GENESIS_DATA['hash']

    for key, value in GENESIS_DATA.items():
        getattr(genesis, key) == value
        #this unpacks same as above

def test_quickly_mined_block():
    last_block = Block.mine_block(Block.genesis(), 'foo')
    mined_block = Block.mine_block(last_block, 'bar')   

    assert mined_block.difficulty == last_block.difficulty + 1   

def test_slowly_mined_block():
    last_block = Block.mine_block(Block.genesis(), 'foo')

    time.sleep(MINERATE / SECONDS) 
    #The sleep function takes argumentsin seconds, but minerate is in nanoseconds,dividing it by SECONDS will convert 
    # it to  seconds     

    mined_block = Block.mine_block(last_block, 'bar')  

    assert mined_block.difficulty == last_block.difficulty - 1 

def test_mined_block_difficulty_limits_at_1():
    last_block = Block(
        'test-data',
        time.time_ns(),
        'test_last_hash',
        'test_hash',
        1,
        0
    )

    time.sleep(MINERATE / SECONDS)

    mined_block = Block.mine_block(last_block, 'bar')  

    assert mined_block.difficulty == 1

#fixtures
@pytest.fixture
def last_block():
    return Block.genesis()

@pytest.fixture
def block(last_block):
    return Block.mine_block(last_block, 'foo') 

def test_is_valid_block(last_block, block):
    Block.is_valid(last_block, block)
    

def test_is_valid_block_bad_last_hash(last_block, block):
    block.last_hash = 'evil last hash'

    with pytest.raises(Exception, match = 'last_hash must be correct'):
        Block.is_valid(last_block, block)

def test_is_valid_block_proof_of_work(last_block, block):
    block.hash = 'ffff'

    with pytest.raises(Exception, match = 'The proof of work requirement not met'):
        Block.is_valid(last_block, block)

def test_is_valid_block_difficulty(last_block, block):
    jumped_difficulty = 10
    block.difficulty = jumped_difficulty

    block.hash = f'{"0" * jumped_difficulty}1f456'

    with pytest.raises(Exception, match = 'Block difficulty must only adjust by 1'):
        Block.is_valid(last_block, block)

def test_is_valid_block_bad_hash(last_block, block):
    block.hash = '00000000000aefb32'

    with pytest.raises(Exception, match = 'Block hash must be correct'):
        Block.is_valid(last_block, block)


