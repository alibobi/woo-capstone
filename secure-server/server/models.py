from server.db import db
from dataclasses import dataclass
from sqlalchemy.orm import class_mapper

@dataclass
class User(db.Model):
	__tablename__ = "user"
	
	id = db.Column(db.Integer, primary_key=True)
	user_id : int = db.Column(db.BigInteger, default=db.Sequence('user_id_seq'), nullable=True)
	username : str = db.Column(db.String)
	email    : str = db.Column(db.String)
	password : bytes = db.Column(db.String)


def make_user(username: str, email:str, passwdhash: str):
	user = User(
		username = username,
		email    = email,
		password = passwdhash
	)

	return user
