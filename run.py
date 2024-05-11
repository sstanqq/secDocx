from flask import Flask, request
from app.views import views
from app.web3.web3_interface import check_connection

myapp = Flask(__name__, 
              template_folder='app/templates', 
              static_folder='app/static')

myapp.register_blueprint(views, url_prefix='/')

print(f'Connection to Ganache: {check_connection()}\n')
# addr = '0xdCa5E3F869230a6C4923697628EC8F2EeDDe3D9f'
# print(f'Addr: {addr}\nBalance: {get_balance(addr)}')
# send_transaction(addr, '')

if __name__ == '__main__':
    myapp.run(debug=True) 