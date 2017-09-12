import secrets
class Application():
	def __init__(self, name, license, description,time):
		self.id= secrets.token_hex(4)
		self.name = name
		self.license=license
		self.description= description
		self.time=time
		self.approve=False
		self.check=False

