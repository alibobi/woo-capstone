from flask import Blueprint, render_template, request, redirect, flash

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
	
	if username == "fail":
		flash('Username not allowed to login')
		return render_template('login.html')
	else:
        	return render_template('login_success.html')

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

	print(username)
	print(email)
	print(password)

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

