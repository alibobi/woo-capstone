from flask import Flask, render_template
from server.db import db
from server.configurations import DATABASE_URI
from server.frontend_bp import frontend
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Create a Flask application
app = Flask(__name__)

def build_db() -> None:
    db.drop_all()
    db.create_all()

def run():
	app.secret_key = 'super secret key'
	app.config['SESSION_TYPE'] = 'filesystem'
 
	# initialize limiter
	# don't need limiter var rn because not doing anything special
	limiter = Limiter(
		get_remote_address,
		app=app,
		default_limits=["50 per minute", "1 per second"]
	)
 
	app.register_blueprint(frontend)

	#app.config['SQLALCHEMY_DATABASE_URI']=DATABASE_URI
	app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
	db.init_app(app)

	with app.app_context():
		build_db()
	

	app.run(debug=True, port=9999)
