from Backend.wallet.wallet import Wallet
from Backend.blockchain.blockchain import Blockchain
from Backend.config import STARTING_BALANCE
from Backend.wallet.transaction import Transaction

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

def test_calculate_balance():
    blockchain = Blockchain()
    wallet = Wallet()

    assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE

    amount = 80
    transaction1 = Transaction(wallet, 'recipient', amount)
    blockchain.add_block([transaction1.to_json()])

    assert Wallet.calculate_balance(blockchain, wallet.address) == \
        STARTING_BALANCE - amount

    received_amount1 = 80
    received_transaction1 = Transaction(Wallet(), wallet.address, received_amount1)

    received_amount2 = 60
    received_transaction2 = Transaction(Wallet(), wallet.address, received_amount2)

    blockchain.add_block([received_transaction1.to_json(), received_transaction2.to_json()])

    assert Wallet.calculate_balance(blockchain, wallet.address) == \
        STARTING_BALANCE - amount + received_amount1 + received_amount2
    


    




