from flask import Blueprint, render_template, request, redirect, url_for

frontend = Blueprint("frontend", __name__)

@frontend.route("/")
@frontend.route("/index")
@frontend.route("/index.html")
def home():
	return render_template('index.html')

@frontend.route("/login")
@frontend.route("/login.html")
def login():
	return render_template('login.html')

@frontend.route("/create_account", methods=["GET"])
@frontend.route("/create_account.html", methods=["GET"])
def create_account_page():
        return render_template('create_account.html')


@frontend.route("/create_account", methods=["POST"])
@frontend.route("/register.php", methods=["POST"])
def create_account():
	username = request.form['username']
	email = request.form['email']
	password = request.form['password']	

	print(username)
	print(email)
	print(password)

	print("/create_account_success")
	return redirect("/create_account_success")


@frontend.route("/create_account_success")
def create_account_success():
        return "Account created successfully"



