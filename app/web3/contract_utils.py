from web3 import Web3
import json 

contract_address = '0x123456789ABCDEF'

with open('contract_abi.json', 'r') as abi_file:
    contract_abi = json.load(abi_file)

def init_contract(w3: Web3, contract_address, contract_abi):
    return w3.eth.contract(address=contract_address, abi=contract_abi)

def add_document(w3: Web3, contract, file_hash, owner_address):
    tx_hash = contract.functions.addDocument(file_hash, owner_address).transact({'from': owner_address})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt

def get_documents(contract, owner_address):
    documents = contract.functions.getDocumentsByOwner(owner_address).call()
    return documents
