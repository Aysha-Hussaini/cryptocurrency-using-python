import pytest

from Backend.wallet.wallet import Wallet
from Backend.wallet.transaction import Transaction

def test_transaction():
    sender_wallet = Wallet()
    recipient = 'recipient'
    amount = 50

    transaction = Transaction(sender_wallet, recipient, amount)

    assert transaction.output[recipient] == amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - amount

    assert 'timestamp' in transaction.input
    assert transaction.input ['address'] == sender_wallet.address
    assert transaction.input['public_key'] == sender_wallet.public_key
    assert transaction.input['amount'] == sender_wallet.balance


    assert sender_wallet.verify_sign(
        transaction.input['public_key'],
        transaction.output, 
        transaction.input['signature'])

def test_transaction_exceeds_balance():
    
    with pytest.raises(Exception, match="Amount exceeds sender wallet's balance !"):
        Transaction(Wallet(), 'recipient', 1400)

def test_transaction_update_exceeds_balance():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 50) 
    with pytest.raises(Exception, match="Amount exceeds sender wallet's balance !"):
        transaction.update(sender_wallet, 'recipient-1', 8000) 

def test_tranaction_update_successful_update():
    sender_wallet = Wallet()
    first_recipient = 'first_recipient'
    first_amount = 50

    transaction = Transaction(sender_wallet, first_recipient, first_amount) 
    
    next_recipient = 'next_recipient'
    next_amount = 50
    
    transaction.update(sender_wallet, next_recipient, next_amount)

    assert transaction.output[next_recipient] == next_amount
    assert transaction.output[sender_wallet.address] == \
        sender_wallet.balance - first_amount - next_amount

    assert sender_wallet.verify_sign(
        transaction.input['public_key'],
        transaction.output, 
        transaction.input['signature'])

    to_first_recipient_amount = 50
    transaction.update(sender_wallet, first_recipient, to_first_recipient_amount)
    assert transaction.output[first_recipient] == to_first_recipient_amount
    assert transaction.output[sender_wallet.address] == \
        sender_wallet.balance - first_amount - next_amount - to_first_recipient_amount

    assert sender_wallet.verify_sign(
        transaction.input['public_key'],
        transaction.output, 
        transaction.input['signature'])

def test_valid_transaction():
    Transaction.validate_transaction(Transaction(Wallet(), 'recipient', 80))

def test_invalid_transaction_output_values():

    sender_wallet = Wallet()

    transaction = Transaction(sender_wallet, 'recipient', 50)

    transaction.output[sender_wallet.address] = 9000
    
    with pytest.raises(Exception, match = 'Invalid transaction output values'):
        Transaction.validate_transaction(transaction)


def test_invalid_transaction_signature():
    transaction = Transaction(Wallet(), 'recipient', 18)

    transaction.input['signature'] = Wallet().sign(transaction.output)

    with pytest.raises(Exception, match = 'Invalid transaction signature'):
        Transaction.validate_transaction(transaction)

        

   