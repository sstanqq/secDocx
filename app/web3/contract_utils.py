from web3 import Web3
from web3.middleware import geth_poa_middleware
from datetime import datetime, timezone

class DocumentStorageClient:
    def __init__(self, contract_address, abi, provider_uri='http://127.0.0.1:7545'):
        self.w3 = Web3(Web3.HTTPProvider(provider_uri))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.contract = self.w3.eth.contract(address=contract_address, abi=abi)
    
    def upload_document(self, hash, sender, name, size):
        tx_hash = self.contract.functions.uploadDocument(hash, name, size).transact({'from': sender})
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt
    
    def send_document(self, hash, sender, recipient_address):
        tx_hash = self.contract.functions.sendDocument(hash, recipient_address).transact({'from': sender})
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt
    
    def delete_document(self, hash, sender):
        tx_hash = self.contract.functions.deleteDocument(hash).transact({'from': sender})
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt
    
    def get_user_documents(self, sender):
        documents = self.contract.functions.getUserDocuments().call({'from': sender})

        print(documents)

        documents_list = []
        for doc in documents:
            document = {
                'hash' : doc[0],
                'sender' : doc[1],
                'tr_type' : doc[2],
                'name' : doc[3],
                'timestamp': datetime.fromtimestamp(doc[5], tz=timezone.utc).strftime('%d.%m.%Y %H:%M:%S')
            }
            documents_list.append(document)

        return documents_list