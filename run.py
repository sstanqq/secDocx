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

myapp.register_blueprint(views, url_prefix='/')

print(f'Connection to Ganache: {check_connection()}\n')

if __name__ == '__main__':
    myapp.run(debug=True) 