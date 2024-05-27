from flask import session, redirect
from flask import Blueprint, render_template, request, jsonify
from app.web3.web3_interface import check_connection
from app.ipfs.ipfs_interface import check_pinata_connection, upload_file_to_pinata, \
                                    download_file_from_pinata, delete_file_from_pinate

from app.ipfs.utils import generate_hash

import os

views = Blueprint('main', __name__)

@views.route('/')
def index():
    wallet_address = session.get('walletAddress')
    print(f'Wallet address: {wallet_address}')
    if not wallet_address:
        return render_template('index.html')
    
    return render_template('documents.html')

# Connect & disconnect wallet routes
@views.route('/connectwallet', methods=['POST'])
def connect_wallet():
    try:
        data = request.get_json()  
        wallet_address = data.get('walletAddress')
        print(f'Received wallet address: {wallet_address}')
        if wallet_address:
            session['walletAddress'] = wallet_address
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
    # public key check
    wallet_address = session.get('walletAddress')
    if not wallet_address:
        return redirect('/')

    return render_template('transactions.html')


@views.route("/upload", methods=["POST"])
def upload_document():
    # Check Pinata API connection
    if not check_pinata_connection():
        return jsonify({'error': 'Failed to connect to Pinata'}), 500

    if request.method == "POST":
        file = request.files["file"]

        # Save file to temp dir
        temp_dir = 'temp'
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, file.filename)
        file.save(file_path)

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

        os.remove(file_path)

        return jsonify({'result': response})
    
@views.route("/download", methods=["POST"])
def download_document():
    # Check Pinata API connection
    if not check_pinata_connection():
        return jsonify({'error': 'Failed to connect to Pinata'}), 500 

    if request.method == "POST":
        pass 

@views.route("/delete", methods=["POST"])
def delete_document():
    # Check Pinata API connection
    if not check_pinata_connection():
        return jsonify({'error': 'Failed to connect to Pinata'}), 500 

    if request.method == "POST":
        pass  

@views.route("/send", methods=["POST"])
def send_document():
    pass 