from flask import Blueprint, render_template, request, redirect, flash
from server.db import db
from server.crypto import generate_password_hash, verify_password
from server.models import User, make_user

frontend = Blueprint("frontend", __name__)

@frontend.route("/")
@frontend.route("/index")
@frontend.route("/index.html")
def home():
	return render_template('index.html')

@frontend.route("/login", methods=["GET"])
@frontend.route("/login.html", methods=["GET"])
def login_page():
	return render_template('login.html')

@frontend.route("/login", methods=["POST"])
@frontend.route("/login.html", methods=["POST"])
def login_attempt():
	username = request.form['username']
	password = request.form['password']
	passwd_hash = generate_password_hash(password)

	user = User.query.filter_by(username=username).first()

	if user and verify_password(password, user.password):
		print("Logged in with user:", user) 
		return render_template('login_success.html')
	else:
		flash('Login failed')
		return render_template('login.html')


@frontend.route("/create_account", methods=["GET"])
@frontend.route("/create_account.html", methods=["GET"])
def create_account_page():
        return render_template('create_account.html')


@frontend.route("/create_account", methods=["POST"])
@frontend.route("/create_account.html", methods=["POST"])
def create_account():
	username = request.form['username']
	email = request.form['email']
	password = request.form['password']	
	passwd_hash = generate_password_hash(password)
	
	new_user = make_user(username, email, passwd_hash)
	db.session.add(new_user)
	db.session.commit()
	
	if(username == "fail"):
		flash('User already exists')
		return render_template('create_account.html')
	else:
		return redirect("/create_account_success")

@frontend.route("/create_account_success")
def create_account_success():
	return render_template('account_success.html')


@frontend.route("/forgot_password")
def forgot_password():
	return render_template('forgot_password.html')

