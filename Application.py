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
		self.approve="In progress"
		
	def display(self):
		str=""
		str+="ApplicationID:"+self.id+"</br>"
		str+="Username:"+self.user+"</br>"
		str+="GivenName:"+self.givenName+"</br>"
		str+="Surname:"+self.surname+"</br>"
		str+="Dob:"+self.dob+"</br>"
		str+="Address:"+self.address+"</br>"
		str+="Postcode:"+self.postcode+"</br>"
		str+="Email:"+self.email+"</br>"
		str+="Number:"+self.number+"</br>"
		str+="Approval Status:"+self.approve+"</br>"
		return str
		
