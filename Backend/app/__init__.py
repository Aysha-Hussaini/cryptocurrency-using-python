import os
import requests
import random
from flask import Flask, jsonify, request
from flask_cors import CORS
from Backend.blockchain.blockchain import Blockchain
from Backend.wallet.wallet import Wallet
from Backend.wallet.transaction import Transaction
from Backend.wallet.transaction_pool import TransactionPool
from Backend.pubsub import PubSub

app = Flask(__name__)
CORS(app, resources={r'/*' : {'origins': 'http://localhost:3000'}})
blockchain = Blockchain()
wallet = Wallet(blockchain)
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain, transaction_pool)

@app.route('/')
def route_default():
    return 'Welcome to the blockchain'


@app.route('/blockchain')
def route_blockchain():
    # return blockchain.chain #list cannot be sent 
    return jsonify(blockchain.to_json())


@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = transaction_pool.transaction_data()
    transaction_data.append(Transaction.reward_transaction(wallet).to_json())
    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    transaction_pool.clear_blockchain_transactions(blockchain)
    #jsonify accepts only serialized data - 
    # serialization and jsonify is necessary for https requests 
    return jsonify(block.to_json())

@app.route('/wallet/transact', methods= ['POST'])
def route_wallet_transact():
    #{'recipient' : 'foo', 'amount' = 15}
    transaction_data = request.get_json()
    transaction = transaction_pool.existing_transaction(wallet.address)
    if transaction:
        transaction.update(wallet, transaction_data['recipient'], transaction_data['amount'])    
    else:
        transaction = Transaction(wallet, transaction_data['recipient'], transaction_data['amount'])

    pubsub.broadcast_transaction(transaction)
    
    return jsonify(transaction.to_json()) 

@app.route('/wallet/info')
def route_wallet_info():
    return jsonify({'address' : wallet.address, 'balance' : wallet.balance })

ROOT_PORT = 5000
PORT = ROOT_PORT

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000)

    try:
        result = requests.get(f'http://localhost:{ROOT_PORT}/blockchain')
    except Exception as e:
        print(f'unable to get the request : {e}')
    
    result_blockchain = Blockchain.from_json(result.json())

    try:
        Blockchain.replace_chain(result_blockchain.chain)
        print('-- Successfully synchronized the local chain')
    except Exception as e:
        print(f'Error synchronizing the local chain: {e}')


app.run(port = PORT)


