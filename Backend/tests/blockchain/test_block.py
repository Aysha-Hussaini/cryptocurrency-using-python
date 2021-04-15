import time
from Backend.blockchain.block import Block, GENESIS_DATA
from Backend.config import MINERATE, SECONDS

def test_mine_block():
    last_block = Block.genesis()
    data = 'test-data'
    block = Block.mine_block(last_block, data)

    assert isinstance (block, Block)
    #isinstance checks if the instance is object of a class 

    assert block.data == data

    assert block.last_hash == last_block.hash

    assert block.hash[0:block.difficulty] == '0' * block.difficulty

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