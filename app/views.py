from flask import Blueprint, render_template, request, jsonify
from app.web3.web3_interface import create_ethereum_address, get_balance, get_accs

views = Blueprint('main', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/create_account')
def create_account():
    sk, addr = create_ethereum_address()

    return jsonify({
        'address' : addr,
        'private key' : sk, 
        'balance' : get_balance(addr)
    })

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
def upload():
    if request.method == "POST":
        # Обработка загрузки файла и его сохранение
        file = request.files["file"]

        # Передача файла в функцию для загрузки на блокчейн
        # upload_file_to_blockchain(file)
        return "File uploaded successfully!"