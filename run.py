from flask import Flask, request
from app.views import views
from app.web3.web3_interface import check_connection

import os
from dotenv import load_dotenv
load_dotenv()

myapp = Flask(__name__, 
              template_folder='app/templates', 
              static_folder='app/static')

myapp.secret_key = os.getenv('FLASK_SEC_TOKEN') 

@myapp.template_filter('shorten')
def shorten_filter(s):
    if len(s) <= 9:
        return s
    return s[:4] + '...' + s[-5:]

@myapp.template_filter('format_size')
def format_size(value):
    for unit in ['', 'КБ', 'МБ', 'ГБ', 'ТБ']:
        if value < 1024.0:
            return f"{value:.2f} {unit}"
        value /= 1024.0


myapp.register_blueprint(views, url_prefix='/')

print(f'Connection to Ganache: {check_connection()}\n')

if __name__ == '__main__':
    myapp.run(debug=True) 