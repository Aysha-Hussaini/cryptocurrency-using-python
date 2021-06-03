from Backend.wallet.transaction_pool import TransactionPool
from Backend.wallet.transaction import Transaction
from Backend.wallet.wallet import Wallet

def test_set_transaction():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 100)

    transaction_pool = TransactionPool()

    transaction_pool.set_transaction(transaction) 

    assert transaction_pool.transaction_map[transaction.id] ==  transaction
           

