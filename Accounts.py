import Crypto.Hash.MD5 as MD5
import secrets

class Accounts:

	def __init__(self, name, password, access):
		self.name = name
		self.salt = secrets.token_hex(8)
		self.sh_password = MD5.new((password + self.salt).encode()).hexdigest()
		self.access = access

	def verify_password(self, password):
		input_hash = MD5.new((password + self.salt).encode()).hexdigest()
		return secrets.compare_digest(input_hash, self.sh_password)

	def access_level(self):
		return self.access

	def secure_password(password):
		return len(password) < 8

class PublicAccount(Accounts):

	def __init__(self, name, password, rso=False):
		super().__init__(name, password, 0)
		self.user_id = secrets.token_hex(4)
		self.rso = rso

class StaffAccount(Accounts):

	def __init__(self, name, password):
		super().__init__(name, password, 1)

class AdminAccount(Accounts):

	def __init__(self, name, password):
		super().__init__(name, password, 9)