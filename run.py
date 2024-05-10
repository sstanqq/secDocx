from flask import Flask, request
from app.views import views

myapp = Flask(__name__, 
              template_folder='app/templates', 
              static_folder='app/static')

myapp.register_blueprint(views, url_prefix='/')

if __name__ == '__main__':
    myapp.run(debug=True) 