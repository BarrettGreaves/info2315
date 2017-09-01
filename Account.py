import Crypto.Hash.MD5 as MD5
import secrets

class Account:

	def __init__(self, name, password):
		self.name = name
		self.__salt = secrets.token_hex(16)
		self.__sh_password = MD5.new((password + self.__salt).encode()).hexdigest()

	def verify_password(self, password):
		input_hash = MD5.new((password + self.__salt).encode()).hexdigest()
		return secrets.compare_digest(input_hash, __sh_password)
