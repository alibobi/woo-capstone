from flask import Blueprint, render_template, request, redirect, flash, session
from server.db import db
from server.crypto import generate_password_hash, verify_password
from server.models import User #, make_user
import re
from server.utils import get_b64encoded_qr_image

auth = Blueprint("auth", __name__)

@auth.route("/configure_mfa")
@auth.route("/configure_mfa.html")
def configure_mfa():
    current_user = User.query.filter_by(username=session["user"]).first() 
    secret = current_user.secret_token
    uri = current_user.get_authentication_setup_uri()
    base64_qr_image = get_b64encoded_qr_image(uri)
    return render_template('configure_mfa.html', username=session["user"], secret=secret, qr_image=base64_qr_image)


@auth.route("/change_password")
@auth.route("/change_password.html")
def change_password():
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

    return render_template('verify_2fa.html')

@auth.route("/logout", methods=['GET'])
def logout():
    session.pop("user", None)
    return redirect("/index.html")

