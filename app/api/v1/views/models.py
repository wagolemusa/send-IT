users = []

class User:
	def __init__(self):
		self.user_info = {}
		self.users = users

	def register_user(self, firstname, lastname,  username, phone, country, email, password):
   	
		self.user_info['user_id'] = len(self.users)+1
		self.user_info['firstname'] = firstname
		self.user_info['lastname'] = lastname
		self.user_info['username'] = username
		self.user_info['phone'] = phone
		self.user_info['country'] = country	
		self.user_info['email'] = email
		self.user_info['password'] = password
		users.append(self.user_info)
		return self.user_info

	def reset_password(self, email, password, password_confirmation):
		for user in users:
			if email == user['email']:
				if password == password_confirmation:
					self.user_info['password'] = password
				return "Password reset successfully"

	def login_user(self, username, password):
		for user in users:
			if username == user['username'] and password == user['password']:
				return user
			else:
				return "Wrong email/password combination"