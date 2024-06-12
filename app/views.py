from flask import session, redirect
from flask import Blueprint, render_template, request, jsonify
from app.web3.web3_interface import check_connection
from app.ipfs.ipfs_interface import check_pinata_connection, upload_file_to_pinata, \
                                    download_file_from_pinata, delete_file_from_pinata

from web3 import Web3
from app.ipfs.utils import generate_hash

import os

views = Blueprint('main', __name__)

# Init smart-contract 
import json
from app.web3.contract_utils import DocumentStorageClient

contract_address = "0xF75b64ef6B892ec4657F7067e92d3895F3B63da0"
abi_file_path = "app/web3/abi.json"

with open(abi_file_path, 'r') as f:
    abi_json = json.load(f)

client = DocumentStorageClient(contract_address, abi_json)

@views.route('/')
def index():
    wallet_address = session.get('walletAddress')
    print(f'Wallet address: {wallet_address}')
    if not wallet_address:
        return render_template('index.html')
    
    # Get docs from blockchain 
    documents = client.get_user_documents(wallet_address)
    sorted_documents = sorted(documents, key=lambda x: x['timestamp'], reverse=True)

    return render_template('documents.html', documents=sorted_documents)

# Connect & disconnect wallet routes
@views.route('/connectwallet', methods=['POST'])
def connect_wallet():
    try:
        data = request.get_json()  
        wallet_address = data.get('walletAddress')
        print(f'Received wallet address: {wallet_address}')
        if wallet_address:
            session['walletAddress'] = Web3.to_checksum_address(wallet_address)
            return jsonify({'message': 'Wallet address saved'}), 200
        return jsonify({'error': 'No wallet address provided'}), 400
    except Exception as e:
        print(f'Error saving wallet address: {e}')
        return jsonify({'error': str(e)}), 500
    
@views.route('/disconnectwallet', methods=['POST'])
def disconnect_wallet():
    if 'walletAddress' in session:
        del session['walletAddress']
        return jsonify({'message': 'Wallet disconnected'}), 200
    return jsonify({'error': 'No wallet address in session'}), 400

@views.route('/transferdocuments')
def transfer_documents():
    # public key check
    wallet_address = session.get('walletAddress')
    if not wallet_address:
        return redirect('/')
    

    
    return render_template('transfer.html')

@views.route('/transactions')
def transactions():
    wallet_address = session.get('walletAddress')
    if not wallet_address:
        return redirect('/')

    transactions = client.get_user_documents(wallet_address)
    sorted_transactions = sorted(transactions, key=lambda x: x['timestamp'], reverse=True)

    tx_list = []
    for i, tx in enumerate(sorted_transactions[:20]):
        transaction = {'id' : i+1,
                       'name': tx['name'],
                       'timestamp' : tx['timestamp'],
                       'tx_type' : 'Хранение' if tx['tr_type'] == 0 else 'Отправка',
                       'sender' : tx['sender'],
                       'reciever' : '',
                       'status' : 'Выполнен'}
        tx_list.append(transaction)

    return render_template('transactions.html', transactions=tx_list)


@views.route("/upload", methods=["POST"])
def upload_document():
    # Check Pinata API connection
    if not check_pinata_connection():
        return jsonify({'error': 'Failed to connect to Pinata'}), 500
    # Check blockchain connection 
    if not check_connection:
        return jsonify({'error': 'Failed to connect to blockchain'}), 500

    if request.method == "POST":
        file = request.files["file"]

        # Save file to temp dir
        temp_dir = 'temp'
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, file.filename)
        file.save(file_path)

        file_name = file.filename
        file_size = os.path.getsize(file_path)

        # Calculate hash 
        temp_hash = generate_hash(file_path)

        # Upload to pinata
        response = upload_file_to_pinata(file_path)

        ipfshash = response['IpfsHash']
        timestamp = response['Timestamp']

        # Uncom then 
        # if temp_hash != ipfshash:
        #     return jsonify({'error': 'file integrity error'}), 500

        print(f'ipfs hash: {ipfshash}')
        print(f'timestamp: {timestamp}')

        # Blockchain transaction
        sender = session.get('walletAddress')
        client.upload_document(ipfshash, sender, file_name, file_size)

        os.remove(file_path)

        return jsonify({'result': response})
    
@views.route("/download", methods=["POST"])
def download_document():
    # Check Pinata API connection
    if not check_pinata_connection():
        return jsonify({'error': 'Failed to connect to Pinata'}), 500 
    if not check_connection():
        return jsonify({'error': 'Failed to connect to blockchain'}), 500  
    
    sender = session.get('walletAddress')
    documents = client.get_user_documents(sender)

    try:
        data = request.get_json()
        file_hash = data.get('file_hash')
        file_path = data.get('file_path')
        print(f'FILE_HASH: {file_hash}')
        print(f'FILE_PATH: {file_path}')

        sender = session.get('walletAddress')

        if not file_hash:
            return jsonify({'error': 'No file hash provided'}), 400

        if not sender:
            return jsonify({'error': 'No wallet address in session'}), 400

        # Get document data
        documents = client.get_user_documents(sender)
        res_doc = next((item for item in documents if item.get('hash') == file_hash), None)

        if not res_doc:
            return jsonify({'error': 'No such file connected to wallet address'}), 400
        
        file_name = res_doc['name']

        response = download_file_from_pinata(file_path, file_hash)
        return jsonify({'result': response})

    except Exception as e:
        print('Error downloading document')
        return jsonify({'error': str(e)}), 500

    


@views.route("/delete", methods=["POST"])
def delete_document():
    # Check Pinata API connection
    if not check_pinata_connection():
        return jsonify({'error': 'Failed to connect to Pinata'}), 500 

    try:
        data = request.get_json()
        file_hash = data.get('file_hash')
        print(f'FILE_HASH: {file_hash}')

        sender = session.get('walletAddress')

        if not file_hash:
            return jsonify({'error': 'No file hash provided'}), 400

        if not sender:
            return jsonify({'error': 'No wallet address in session'}), 400

        # Check if the file exists in the contract
        # document = client.get_document(file_hash)
        # if not document or document['sender'] != sender:
        #     return jsonify({'error': 'Document not found or you are not the owner'}), 404

        # Delete file from Pinata
        delete_response = delete_file_from_pinata(file_hash)
        if delete_response.status_code != 200:
            return jsonify({'error': 'Failed to delete file from Pinata'}), 500

        tx_receipt = client.delete_document(file_hash, sender)
        if not tx_receipt:
            return jsonify({'error': 'Failed to delete document from blockchain'}), 500

        return jsonify({'message': 'File successfully deleted'}), 200

    except Exception as e:
        print(f'Error deleting document: {e}')
        return jsonify({'error': str(e)}), 500
    
@views.route("/send", methods=["POST"])
def send_document():
    pass 