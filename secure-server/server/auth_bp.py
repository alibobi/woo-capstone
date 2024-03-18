from flask import Blueprint, render_template, request, redirect, flash, session
from server.db import db
from server.crypto import generate_password_hash, verify_password
from server.models import User, make_user
import re

auth = Blueprint("auth", __name__)

@auth.route("/configure_mfa")
@auth.route("/configure_mfa.html")
def configure_mfa():
    return render_template('configure_mfa.html', username=session["user"])


@auth.route("/change_password")
@auth.route("/change_password.html")
def change_password():
    return render_template('change_password.html', username=session["user"])

