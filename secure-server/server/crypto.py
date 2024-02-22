import bcrypt

def generate_password_hash(password):
	salt = bcrypt.gensalt()
	hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

	return hashed_password.decode('utf-8')	

def verify_password(plaintext_password, hashed_password):
	return bcrypt.checkpw(plaintext_password.encode('utf-8'), hashed_password.encode('utf-8'))
