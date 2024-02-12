from flask import Flask, render_template
from server.db import db
from server.frontend_bp import frontend

# Create a Flask application
app = Flask(__name__)

def build_db() -> None:
    db.drop_all()
    db.create_all()

def run():
	app.secret_key = 'super secret key'
	app.config['SESSION_TYPE'] = 'filesystem'
	app.register_blueprint(frontend)
	app.run(debug=True, port=9999)



