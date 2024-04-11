from flask import Flask, render_template
from server.db import db
from server.configurations import DATABASE_URI, SECRET_KEY
from server.frontend_bp import frontend
from server.auth_bp import auth
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from datetime import timedelta
from server.models import User

import os
import ssl
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER) 

current_dir = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(current_dir, '../cert/')
cert_file_path = os.path.join(ASSETS_DIR, 'woo-cert.pem')
key_file_path = os.path.join(ASSETS_DIR, 'woo-key.pem')
context.load_cert_chain(cert_file_path, key_file_path)

# Create a Flask application
app = Flask(__name__)

def build_db() -> None:
    db.drop_all()
    db.create_all()

def run():
        app.secret_key = 'super secret key'
        app.config['SESSION_TYPE'] = 'filesystem'
#        app.config["SESSION_PERMANENT"] = False
        app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
        Session(app)
        app.secret_key = SECRET_KEY
        csrf = CSRFProtect(app)

	# initialize limiter
	# don't need limiter var rn because not doing anything special
#	limiter = Limiter(
#                get_remote_address,
#		app=app,
#		default_limits=["50 per minute", "5 per second"]
#	)
 
        app.register_blueprint(frontend)
        app.register_blueprint(auth)

        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)
	
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        #app.config['SQLALCHEMY_DATABASE_URI']=DATABASE_URI
        app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
        db.init_app(app)

        #UNCOMMENT THIS IF WE WANT DATABASE TO RESTART ON EVERY RUN
        with app.app_context():
           build_db()
	

        app.run(debug=False, ssl_context=context, port=9999)
