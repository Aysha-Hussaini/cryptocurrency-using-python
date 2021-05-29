from Backend.wallet.wallet import Wallet

def test_verify_valid_signature():
    data = {'foo' : 'bar'}
    wallet = Wallet()
    signature = wallet.sign(data)

    assert wallet.verify_sign(wallet.public_key, data, signature)

def test_verify_invalid_signature():
    data = {'foo' : 'bar'}
    wallet = Wallet()
    signature = wallet.sign(data)

    assert not wallet.verify_sign(Wallet().public_key, data, signature)


