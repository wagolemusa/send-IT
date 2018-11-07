import re
class Validation():
	def password_verify(password,confirm_password):
		if password == confirm_password:
			return True
		else:
			return False

	def valid_email(email):
		if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) != None:
			return True
		else:
			return False

