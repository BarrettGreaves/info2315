import secrets
class Application():
	def __init__(self,user, givenName,surname,dob,address,postcode,email,number):
		self.id= secrets.token_hex(4)
		self.user=user
		self.givenName = givenName
		self.surname = surname 
		self.dob = dob
		self.address =address
		self.postcode = postcode
		self.email = email
		self.number =number
		self.approve=""
		

