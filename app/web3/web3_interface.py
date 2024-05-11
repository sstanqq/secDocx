from web3 import Web3
from web3.middleware import geth_poa_middleware
import json 

GANACHE_NODE = 'http://localhost:7545'
web3 = Web3(Web3.HTTPProvider(GANACHE_NODE))

def get_latest_block():
    print(f'latest local ganache block: {web3.eth.get_block("latest")}') 

def check_connection() -> bool:
    if web3.is_connected():
        return True 
    
    return False 

def create_ethereum_address():
    account = web3.eth.account.create()
    private_key = account._private_key.hex()
    address = account.address

    return private_key, address 

def get_accs():
    return web3.eth.accounts

def generate_ethereum_address():
    account = web3.eth.account.create()

    return account.address

def get_balance(addr):
    return web3.eth.get_balance(addr) 

def connect_metamask():
    # Добавление промежуточного программного обеспечения, если это сеть Ethereum с proof-of-authority (например, Ganache)
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # Проверка подключения к провайдеру
    if web3.isConnected():
        print("Successfully connected to MetaMask!")
    else:
        print("Failed to connect to MetaMask.")

    # Возвращаем экземпляр web3
    return web3
def send_transaction(to, data):
    tx_hash = web3.eth.send_transaction({
        'to' : to,
        'value' : 10,
        'data' : data
    }) 

    return tx_hash