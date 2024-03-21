from flask import Blueprint, render_template, request, redirect, flash, session
from server.db import db
from server.crypto import generate_password_hash, verify_password
from server.models import User 
#, make_user
import re

frontend = Blueprint("frontend", __name__)

@frontend.route("/")
@frontend.route("/index")
@frontend.route("/index.html")
def home():
        if 'user' in session:
            print(session["user"])
        return render_template('index.html')

@frontend.route("/login", methods=["GET"])
@frontend.route("/login.html", methods=["GET"])
def login_page():
	return render_template('login.html')

@frontend.route("/login", methods=["POST"])
@frontend.route("/login.html", methods=["POST"])
def login_attempt():
	username = request.form['username']
	username_pattern = re.compile(r'^[a-z0-9_\-\.]{3,16}$')
	if username_pattern.match(username):
		print("Username entered")
	else:
		# Username must only contain lowercase letters, numbers, -, ., or _, and must be between 3 and 16 chars
		flash("Login is invalid")
		return render_template('login.html')
 
	password = request.form['password']
	password_pattern = re.compile(r'^[a-zA-Z0-9_\-\!\@\#\$\%\^\&\*]{8,}$')
	if password_pattern.match(password):
		print("Password entered")
	else:
		# Password must be 8+ characters
		flash("Login is invalid")
		return render_template('login.html')

	user = User.query.filter_by(username=username).first()

	if user and verify_password(password, user.password):
		print("Logged in with user:", user) 
		session["user"] = username
		return redirect("/login_success")
        # return render_template('login_success.html')
	else:
		flash('Login failed')
		return render_template('login.html')


@frontend.route("/login_success", methods=["GET"])
@frontend.route("/login_success.html", methods=["GET"])
def login_success():
    #flash(session["user"])
    return render_template('login_success.html', username=session["user"])

@frontend.route("/create_account", methods=["GET"])
@frontend.route("/create_account.html", methods=["GET"])
def create_account_page():
    return render_template('create_account.html')


@frontend.route("/create_account", methods=["POST"])
@frontend.route("/create_account.html", methods=["POST"])
def create_account():
    # we're very intentionally whitelisting certain chars as opposed to blacklisting, we're more likely to forget things
	username = request.form['username']
	username_pattern = re.compile(r'^[a-z0-9_\-\.]{3,16}$')
	if username_pattern.match(username):
		print("Username format correct: " + username)
	else:
		# Username must only contain lowercase letters, numbers, -, ., or _, and must be between 3 and 16 chars
		flash("Username is invalid")
		return render_template('create_account.html')
 
	email = request.form['email']
	email_pattern = re.compile(r'^[a-zA-Z0-9._\-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$')
	if email_pattern.match(email):
		print("Email format correct: " + email)
	else:
		# Email must be an email
		flash("Email is invalid")
		return render_template('create_account.html')
 
	password = request.form['password']
	password_pattern = re.compile(r'^[a-zA-Z0-9_\-\!\@\#\$\%\^\&\*]{8,}$')
	if password_pattern.match(password):
		print("Password correct")
	else:
		# Password must be 8+ characters
		flash("Password is invalid, must be 8+ characters")
		return render_template('create_account.html')
 
	passwd_hash = generate_password_hash(password)
	
	new_user = User(username, email, passwd_hash)
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

