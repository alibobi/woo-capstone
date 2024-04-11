from flask import Blueprint, render_template, request, redirect, flash, session
from server.db import db
from server.crypto import generate_password_hash, verify_password
from server.models import User #, make_user
import re
from server.utils import get_b64encoded_qr_image
from flask_login import login_user, logout_user, login_required

auth = Blueprint("auth", __name__)

@auth.route("/configure_mfa")
@auth.route("/configure_mfa.html")
def configure_mfa():
    current_user = User.query.filter_by(username=session["user"]).first() 
    secret = current_user.secret_token
    uri = current_user.get_authentication_setup_uri()
    base64_qr_image = get_b64encoded_qr_image(uri)
    return render_template('configure_mfa.html', username=session["user"], secret=secret, qr_image=base64_qr_image)


@auth.route("/change_password", methods=["GET"])
@auth.route("/change_password.html", methods=["GET"])
@login_required
def change_password_page():
    return render_template('change_password.html', username=session["user"])


@auth.route("/change_password", methods=["POST"])
@auth.route("/change_password.html", methods=["POST"])
def change_password():
    old_pw = request.form['old_pw']
    new_pw = request.form['new_pw']
    new_pw_conf = request.form['new_pw_conf']

    # Get the current user's information 
    user = User.query.filter_by(username=session["user"]).first()

    # Ensure new password matches password rules and best practices
    password_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\_\-\!\@\#\$\%\^\&\*])[a-zA-Z0-9_\-\!\@\#\$\%\^\&\*]{8,}$')
    if session["user"] in new_pw:
        flash("Password cannot contain your username")
        return render_template('change_password.html', username=session["user"])
    else:
        if password_pattern.match(new_pw):
            print("Password well formatted")
        else:
            # Password must be 8+ characters
            flash("Password must be 8+ characters and contain one lowercase letter, one uppercase letter, one digit, and one special character.")
            return render_template('change_password.html', username=session["user"])
 
    # Check that the user's old password entered matches the password currently set for the user account
    # Helps to enforce security by making the user prove they know their password and so that an attacker
    # can't change a user's password without having explicit knowledge of the current one 
    # If the passwords don't match, throw an error 
    if user and not verify_password(old_pw, user.password):
        print("Logged in with user:", user) 
        flash("Old password is incorrect")
        return render_template('change_password.html', username=session["user"])
    
    # Verify the new password
    if user and not (new_pw == new_pw_conf):
        print("Logged in with user:", user) 
        flash("New passwords do not match")
        return render_template('change_password.html', username=session["user"])

    # Case where all new password info is valid and user can reset their password
    if user and verify_password(old_pw, user.password) and (new_pw == new_pw_conf):
        # SET USER'S NEW PASSWORD AND CHANGE IT IN DATABASE
        new_passwd_hash = generate_password_hash(new_pw)
        user.password = new_passwd_hash
        db.session.commit()
        return render_template('login_success.html', username=session["user"])
    else:
        return render_template('change_password.html', username=session["user"])


@auth.route("/verify_2fa", methods=['GET'])
@auth.route("/verify_2fa.html", methods=['GET'])
def mfa():
    return render_template('verify_2fa.html')


@auth.route("/verify_2fa", methods=['POST'])
@auth.route("/verify_2fa.html", methods=['POST'])
def verify_2fa():
    otp = request.form.get('otp')
    print(otp)
    current_user = User.query.filter_by(username=session["user"]).first()
    print(current_user.is_otp_valid(otp))

    if current_user.is_otp_valid(otp):
        current_user.is_two_factor_authentication_enabled = True
        db.session.commit()
        login_user(current_user)
        # Redirect user to login if MFA is successfully enabled 
        return redirect('login_success.html')
    else: 
        flash("Invalid OTP")
        # Allow user to retry MFA enable
        return render_template('verify_2fa.html')

@auth.route("/logout", methods=['GET'])
@login_required
def logout():
    session.pop("user", None)
    logout_user()
    return redirect("/index.html")


@auth.route("/education")
@auth.route("/education.html")
@login_required
def education():
        return render_template('education.html', username=session["user"])
