from flask import Flask, jsonify
from Backend.blockchain.blockchain import Blockchain

app = Flask(__name__)
blockchain= Blockchain()

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
    return jsonify(blockchain.chain[-1].to_json())


app.run()


