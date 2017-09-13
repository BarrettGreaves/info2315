import secrets
class Vehicle():
	def __init__(self,user,vehicleType,rego,make,model,licence,address,postcode,purchase,number):
		self.id= secrets.token_hex(4)
		self.user=user
		self.vehicleType=vehicleType
		self.rego=rego
		self.make=make
		self.model=model
		self.licence=licence
		self.address=address
		self.postcode=postcode
		self.purchase=purchase
		self.number=number
		self.destroy=False
		

