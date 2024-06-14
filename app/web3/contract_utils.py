from web3 import Web3
from web3.middleware import geth_poa_middleware
from datetime import datetime, timezone

class DocumentStorageClient:
    def __init__(self, contract_address, abi, provider_uri='http://127.0.0.1:7545'):
        self.w3 = Web3(Web3.HTTPProvider(provider_uri))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.contract = self.w3.eth.contract(address=contract_address, abi=abi)

    def upload_document(self, sender, document_hash, document_name, file_size):
        tx_hash = self.contract.functions.uploadDocument(document_hash, document_name, file_size).transact({'from': sender})
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def send_document(self, sender, document_hash, recipient_address):
        tx_hash = self.contract.functions.sendDocument(document_hash, recipient_address).transact({'from': sender})
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def delete_document(self, sender, document_hash):
        tx_hash = self.contract.functions.deleteDocument(document_hash).transact({'from': sender})
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def get_document_owner(self, document_hash):
        return self.contract.functions.getDocumentOwner(document_hash).call()

    def get_document_recipient(self, document_hash):
        return self.contract.functions.getDocumentRecipient(document_hash).call()

    def get_transaction_type(self, document_hash):
        return self.contract.functions.getTransactionType(document_hash).call()

    def is_document_sent(self, document_hash):
        return self.contract.functions.isDocumentSent(document_hash).call()

    def get_income_documents(self, recipient):
        pass 

    def get_user_documents(self, sender):
        docs = self.contract.functions.getUserDocuments().call({'from': sender})
        documents = []
        for doc in docs:
            document = {
                'name' : doc[0],
                'hash' : doc[1],
                'sender' : doc[2],
                'recipient' : doc[3],
                'tr_type' : doc[4],
                'isSend' : doc[5],
                'timestamp': datetime.fromtimestamp(doc[6], tz=timezone.utc).strftime('%d.%m.%Y %H:%M:%S'),
                'size' : doc[7]

            }
            documents.append(document)

        return documents
    
    def get_income_documents(self, sender):
        docs = self.contract.functions.getReceivedDocuments().call({'from': sender})
        documents = []
        for doc in docs:
            document = {
                'name' : doc[0],
                'hash' : doc[1],
                'sender' : doc[2],
                'recipient' : doc[3],
                'tr_type' : doc[4],
                'isSend' : doc[5],
                'timestamp': datetime.fromtimestamp(doc[6], tz=timezone.utc).strftime('%d.%m.%Y %H:%M:%S'),
                'size' : doc[7]

            }
            documents.append(document)

        return documents