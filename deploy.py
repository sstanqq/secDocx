# Deploy before use(Ganache)

from web3 import Web3
from solcx import compile_standard
import json 

# Conncet to ganache
ganache_url = "http://127.0.0.1:7545" 
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Compile solidity 
with open("app/web3/documentStorage.sol", "r") as file:
    contract_source_code = file.read()

compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"documentStorage.sol": {"content": contract_source_code}},
    "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}}
})

bytecode = compiled_sol["contracts"]["documentStorage.sol"]["DocumentStorage"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["documentStorage.sol"]["DocumentStorage"]["abi"]

print(f'ABI: {abi}')

account = web3.eth.accounts[0]
contract = web3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = contract.constructor().transact({"from": account})
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress

with open("app/web3/abi.json", "w") as abi_file:
    json.dump(abi, abi_file)

print("Contract deployed successfully.")
print("Contract address:", contract_address)