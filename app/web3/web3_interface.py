from web3 import Web3
from web3.middleware import geth_poa_middleware
import json 

GANACHE_NODE = 'http://localhost:7545'
web3 = Web3(Web3.HTTPProvider(GANACHE_NODE))

def get_latest_block():
    return web3.eth.get_block("latest")

def check_connection() -> bool:
    if web3.is_connected():
        return True 
    
    return False 

def get_accs():
    return web3.eth.accounts

def upload_to_blockchain():
    pass 

def get_balance(addr):
    return web3.eth.get_balance(addr) 

def send_transaction(to, data):
    tx_hash = web3.eth.send_transaction({
        'to' : to,
        'value' : 0,
        'data' : data
    }) 

    return tx_hash