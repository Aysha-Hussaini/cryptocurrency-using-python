from Backend.util.crypto_hash import crypto_hash

def test_crypto_hash():
    #assert keyword is used when debugging the code, 
    #it checksif the condition is true
    
    assert crypto_hash('one', [5], 3) == crypto_hash([5], 'one', 3)
    #It should create same hash with inputsinany order

    assert crypto_hash('foo') == 'b2213295d564916f89a6a42455567c87c3f480fcd7a1c15e220f17d7169a790b'