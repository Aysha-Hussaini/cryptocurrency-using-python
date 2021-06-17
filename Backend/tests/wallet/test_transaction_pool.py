from Backend.wallet.transaction_pool import TransactionPool
from Backend.wallet.transaction import Transaction
from Backend.wallet.wallet import Wallet
from Backend.blockchain.blockchain import Blockchain

def test_set_transaction():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 100)

    transaction_pool = TransactionPool()

    transaction_pool.set_transaction(transaction) 

    assert transaction_pool.transaction_map[transaction.id] ==  transaction

def test_clear_blockchain_transaction():
    transactionpool = TransactionPool()
    blockchain = Blockchain()
    
    transaction_1 = Transaction(Wallet(), 'recipient', 20)
    transaction_2 = Transaction(Wallet(), 'recipient', 30)

    transactionpool.set_transaction(transaction_1)
    transactionpool.set_transaction(transaction_2)

    blockchain.add_block([transaction_1.to_json(), transaction_2.to_json()])

    assert transaction_1.id in transactionpool.transaction_map
    assert transaction_2.id in transactionpool.transaction_map

    transactionpool.clear_blockchain_transactions(blockchain)

    assert not transaction_1.id in transactionpool.transaction_map
    assert not transaction_2.id in transactionpool.transaction_map


           

