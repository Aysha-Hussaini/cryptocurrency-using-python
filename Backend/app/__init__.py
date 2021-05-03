import os
import requests
import random
from flask import Flask, jsonify
from Backend.blockchain.blockchain import Blockchain
from Backend.pubsub import PubSub

app = Flask(__name__)
blockchain= Blockchain()
pubsub = PubSub(blockchain)

@app.route('/')
def route_default():
    return 'Welcome to the blockchain'


@app.route('/blockchain')
def route_blockchain():
    # return blockchain.chain #list cannot be sent 
    return jsonify(blockchain.to_json())


@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = 'stub_transaction_data'
    blockchain.add_block(transaction_data)

    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    return jsonify(block.to_json())

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


