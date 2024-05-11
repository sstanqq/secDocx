from flask import Blueprint, render_template, request, jsonify
from app.web3.web3_interface import get_balance, get_accs
from app.ipfs.ipfs_interface import check_pinata_connection, upload_file_to_pinata, \
                                    download_file_from_pinata, delete_file_from_pinate
import os

views = Blueprint('main', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/mydocuments')
def my_documents():
    return render_template('my_documents.html')

@views.route('/transferdocuments')
def transfer_documents():
    return render_template('transfer_documents.html')

@views.route('/accounts')
def get_accounts():
    return jsonify({'accounts' : get_accs()})

@views.route("/upload", methods=["POST"])
def upload_document():
    if request.method == "POST":
        file = request.files["file"]

        temp_dir = 'temp'
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, file.filename)
        file.save(file_path)

        response = upload_file_to_pinata(file_path)
        print(response)

        os.remove(file_path)

        return jsonify({'result' : response})
    
@views.route("/download", methods=["POST"])
def download_document():
    if request.method == "POST":
        pass 

@views.route("/delete", methods=["POST"])
def delete_document():
    if request.method == "POST":
        pass  