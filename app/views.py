from flask import session, redirect, Blueprint, render_template, request, jsonify
from web3 import Web3
from datetime import datetime, timezone
import os
import json

from app.web3.contract_utils import DocumentStorageClient
from app.ipfs.utils import generate_hash
from app.ipfs.ipfs_interface import check_pinata_connection, upload_file_to_pinata, download_file_from_pinata, delete_file_from_pinata
from app.web3.web3_interface import check_connection

views = Blueprint('main', __name__)

# Инициализация контракта
contract_address = "0xAC4346A6ae79d0569054f8b863c2ba55BFF4871d"  # Замените на адрес вашего смарт-контракта
abi_file_path = "app/web3/abi.json"  # Путь к файлу ABI вашего смарт-контракта

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
    print(documents)
    income_docs = client.get_income_documents(wallet_address)
    print(income_docs)
    # sorted_documents = sorted(documents, key=lambda x: x['timestamp'], reverse=True)

    return render_template('documents.html', documents=documents, income_docs=income_docs)

# Подключение кошелька
@views.route('/connectwallet', methods=['POST'])
def connect_wallet():
    try:
        data = request.get_json()  
        wallet_address = data.get('walletAddress')
        if wallet_address:
            session['walletAddress'] = Web3.to_checksum_address(wallet_address)
            return jsonify({'message': 'Wallet address saved'}), 200
        return jsonify({'error': 'No wallet address provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Отключение кошелька
@views.route('/disconnectwallet', methods=['POST'])
def disconnect_wallet():
    if 'walletAddress' in session:
        del session['walletAddress']
        return jsonify({'message': 'Wallet disconnected'}), 200
    return jsonify({'error': 'No wallet address in session'}), 400

# Загрузка документа
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
        client.upload_document(sender, ipfshash, file_name, file_size)

        os.remove(file_path)

        return jsonify({'result': response})

# Скачивание документа
@views.route("/download", methods=["POST"])
def download_document():
    # Проверка соединения с Pinata API
    if not check_pinata_connection():
        return jsonify({'error': 'Failed to connect to Pinata'}), 500 
    # Проверка соединения с блокчейном
    if not check_connection():
        return jsonify({'error': 'Failed to connect to blockchain'}), 500  
    
    try:
        data = request.get_json()
        document_hash = data.get('documentHash')
        file_path = data.get('filePath')

        if not document_hash:
            return jsonify({'error': 'No document hash provided'}), 400

        sender = session.get('walletAddress')

        if not sender:
            return jsonify({'error': 'No wallet address in session'}), 400

        # Получение данных о документе
        owner = client.get_document_owner(document_hash)
        recipient = client.get_document_recipient(document_hash)
        transaction_type = client.get_transaction_type(document_hash)
        is_sent = client.is_document_sent(document_hash)

        if owner != sender and recipient != sender:
            return jsonify({'error': 'You are not authorized to download this document'}), 403

        # Скачивание файла с Pinata
        response = download_file_from_pinata(file_path, document_hash)
        return jsonify({'message': 'Document downloaded successfully', 'response': response}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Удаление документа
@views.route("/delete", methods=["POST"])
def delete_document():
    # Проверка соединения с Pinata API
    if not check_pinata_connection():
        return jsonify({'error': 'Failed to connect to Pinata'}), 500 

    try:
        data = request.get_json()
        document_hash = data.get('documentHash')

        if not document_hash:
            return jsonify({'error': 'No document hash provided'}), 400

        sender = session.get('walletAddress')

        if not sender:
            return jsonify({'error': 'No wallet address in session'}), 400

        # Удаление файла из Pinata
        delete_response = delete_file_from_pinata(document_hash)
        if delete_response.status_code != 200:
            return jsonify({'error': 'Failed to delete file from Pinata'}), 500

        # Удаление документа с блокчейна
        tx_receipt = client.delete_document(sender, document_hash)
        if not tx_receipt:
            return jsonify({'error': 'Failed to delete document from blockchain'}), 500

        return jsonify({'message': 'Document deleted successfully', 'txReceipt': tx_receipt}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Передача документов
@views.route('/transferdocuments')
def transfer_documents():
    wallet_address = session.get('walletAddress')
    if not wallet_address:
        return redirect('/')
    
    # income_docs = client.get_income_documents(wallet_address)
    income_docs = client.get_income_documents(wallet_address)
    user_docs = client.get_user_documents(wallet_address)
    
    return render_template('transfer.html', user_docs=user_docs, income_docs=income_docs)

@views.route("/send", methods=["POST"])
def send_document():
    # Проверка соединения с Pinata API
    if not check_pinata_connection():
        return jsonify({'error': 'Failed to connect to Pinata'}), 500
    # Проверка соединения с блокчейном
    if not check_connection():
        return jsonify({'error': 'Failed to connect to blockchain'}), 500
    
    try:
        data = request.get_json()
        document_hash = data.get('documentHash')
        recipient_address = data.get('recipientAddress')

        if not document_hash or not recipient_address:
            return jsonify({'error': 'Invalid document hash or recipient address'}), 400

        sender = session.get('walletAddress')

        if not sender:
            return jsonify({'error': 'No wallet address in session'}), 400

        tx_receipt = client.send_document(sender, document_hash, recipient_address)
        if not tx_receipt:
            return jsonify({'error': 'Failed to send document'}), 500

        return jsonify({'message': 'Document sent successfully', 'txReceipt': str(tx_receipt)}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@views.route('/transactions')
def transactions():
    wallet_address = session.get('walletAddress')
    if not wallet_address:
        return redirect('/')

    transactions = client.get_user_documents(wallet_address)
    sorted_transactions = sorted(transactions, key=lambda x: x['timestamp'], reverse=True)

    tx_list = []

    return render_template('transactions.html', transactions=tx_list)
