import requests
import time
from Backend.wallet.wallet import Wallet

BASE_URL = 'http://localhost:5000'

def get_blockchain():
    return requests.get(f'{BASE_URL}/blockchain').json()

def get_blockchain_mine():
    return requests.get(f'{BASE_URL}/blockchain/mine').json()

def post_wallet_transact(recipient, amount):
    return requests.post(
        f'{BASE_URL}/wallet/transact',
        json = {
            'recipient' : recipient,
            'amount' : amount
        }
    ).json()

def get_wallet_info():
    return requests.get(f'{BASE_URL}/wallet/info').json()

start_blockchain = get_blockchain()
print(f'\n start_blockchain : {start_blockchain}')

recipient_wallet_address = Wallet().address
recipient = recipient_wallet_address 

post_wallet_transact1 = post_wallet_transact(recipient, 13)
print(f'\npost_wallet_transact1: {post_wallet_transact1}')

time.sleep(1)
post_wallet_transact2 = post_wallet_transact(recipient, 15)
print(f'\n post_wallet_transact2: {post_wallet_transact2}')

time.sleep(1)
mined_block = get_blockchain_mine()
print(f'\nmined_block : {mined_block}')

wallet_info = get_wallet_info()
print(f'\nwallet_info : {wallet_info}')