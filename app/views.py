from flask import Blueprint, render_template, request, jsonify
from app.web3.web3_interface import get_balance, get_accs
from app.ipfs.ipfs_interface import check_pinata_connection, upload_file_to_pinata, \
                                    download_file_from_pinata, delete_file_from_pinate
import os

views = Blueprint('main', __name__)

@views.route('/')
def index():
    documents = [
        {'name': 'Document2.pdf', 'hash': 'QmZc3...E7X5', 'created_at': '14.05.2024 12:43:10'},
        {'name': 'Секретно2.pdf', 'hash': 'QmAd4...F6W6', 'created_at': '14.05.2024 12:41:35'},
        {'name': 'Реферат.docx', 'hash': 'QmBe5...G5V7', 'created_at': '03.02.2023 05:12:19'},
        {'name': 'Доклад.docx', 'hash': 'QmCf6...H4U8', 'created_at': '16.03.2023 13:27:05'},
        {'name': 'ТЭО_Станкевич.docx', 'hash': 'QmDg7...I3T9', 'created_at': '05.04.2024 15:34:12'},
        {'name': 'Отчет.docx', 'hash': 'QmEh8...J2S0', 'created_at': '01.12.2022 22:01:13'},
        {'name': 'Алгоритм_поиска_А1.pdf', 'hash': 'QmFi9...K1R1', 'created_at': '12.05.2024 11:02:56'},
        {'name': 'Алгоритм_сохр_А1.pdf', 'hash': 'QmGj0...L0Q2', 'created_at': '12.05.2024 10:20:15'},
        {'name': 'Алгоритм_автор_А1.pdf', 'hash': 'QmHk1...M9P3', 'created_at': '12.05.2024 09:10:31'},
        {'name': 'ПЗ_Станкевич.docx', 'hash': 'QmIl2...N8O4', 'created_at': '11.04.2024 17:18:03'},
    ]

    return render_template('test.html')
    # return render_template('my_documents.html', documents=documents)

@views.route('/mydocuments')
def my_documents():
    documents = [
        {'name': 'Document2.pdf', 'hash': '12345', 'created_at': '2024-05-15 12:00:00'},
        {'name': 'Секретно2.pdf', 'hash': '12345', 'created_at': '2024-05-15 12:00:00'},
        {'name': 'Реферат.docx', 'hash': '67890', 'created_at': '2024-05-16 12:00:00'},
        {'name': 'Доклад.docx', 'hash': '67890', 'created_at': '2024-05-16 12:00:00'},
        {'name': 'ТЭО_Станкевич.docx', 'hash': '67890', 'created_at': '2024-05-16 12:00:00'},
        {'name': 'Отчет.docx', 'hash': '67890', 'created_at': '2024-05-16 12:00:00'},
        {'name': 'Алгоритм_поиска_А1.pdf', 'hash': '67890', 'created_at': '2024-05-16 12:00:00'},
        {'name': 'Алгоритм_сохр_А1.pdf', 'hash': '67890', 'created_at': '2024-05-16 12:00:00'},
        {'name': 'Алгоритм_автор_А1.pdf', 'hash': '67890', 'created_at': '2024-05-16 12:00:00'},
        {'name': 'ПЗ_Станкевич.docx', 'hash': '12345', 'created_at': '2024-05-15 12:00:00'},
    ]

    return render_template('my_documents.html', documents=documents)

@views.route('/transferdocuments')
def transfer_documents():
    return render_template('transfer_documents.html')

@views.route('/transactions')
def transactions():
    return render_template('index.html')


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