from flask import Flask, render_template
from server.db import db
from server.configurations import DATABASE_URI
from server.frontend_bp import frontend
from flask_sqlalchemy import SQLAlchemy

# Create a Flask application
app = Flask(__name__)

def build_db() -> None:
    db.drop_all()
    db.create_all()

def run():
	app.secret_key = 'super secret key'
	app.config['SESSION_TYPE'] = 'filesystem'
	app.register_blueprint(frontend)

	#app.config['SQLALCHEMY_DATABASE_URI']=DATABASE_URI
	app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
	db.init_app(app)

	with app.app_context():
		build_db()
	

	app.run(debug=True, port=9999)



