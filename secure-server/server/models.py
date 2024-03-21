from server.db import db
from dataclasses import dataclass
from sqlalchemy.orm import class_mapper
from server.configurations import Config

import pyotp

@dataclass
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    user_id : int = db.Column(db.BigInteger, default=db.Sequence('user_id_seq'), nullable=True)
    username : str = db.Column(db.String)
    email    : str = db.Column(db.String)
    password : bytes = db.Column(db.String)
    is_two_factor_authentication_enabled = db.Column(db.Boolean, nullable=False, default=False)
    secret_token = db.Column(db.String, unique=True)

    def __init__(self, username, email, passwdhash):
            self.username = username
            self.email = email
            self.password = passwdhash
            self.secret_token = pyotp.random_base32()

#def make_user(username: str, email:str, passwdhash: str):
#    user = User(
#            username = username,
#            email    = email,
#            password = passwdhash,
#            secret_token = pyotp.random_base32()
#            )
#
#    return user

    def is_otp_valid(self, user_otp):
        totp = pyotp.parse_uri(self.get_authentication_setup_uri())
        return totp.verify(user_otp)

    def get_authentication_setup_uri(self):
        return pyotp.totp.TOTP(self.secret_token).provisioning_uri(name=self.username, issuer_name=Config.APP_NAME)
