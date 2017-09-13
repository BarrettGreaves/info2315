import _pickle as pickle
import os

save_name = "data1.b"
class ApplicationDatabase:
	def __init__(self):
		self.application_list=[]
		
	
	
		
	def __str__(self):
		s = ""
    
		for key in self.application_list:
			
			s+=key.id
			s+="></form>"
			s+=key.id
			s+=key.name
			s+=key.time
			s+=key.license
			
			s+=key.description
			s+="<br/>"
			s+=
			
			
		return s
	
	def get_application(self,id):
		
		for a in self.user_lists:
			if any(obj.id == name for obj in self.a):
				return obj.id
		
		
		
	def add_application(self, application):
		
			self.application_list.append(application)
			self.save()
			return True
		
	def revoke_application(self,application):
		for app in self.application_list:
			if app==application:
				app.check=True
	def approve_application(self,application):
		for app in self.application_list:
			if app==application:
				app.approve=True
				app.check=True
				
				
				
				
				
	def save(self):
		with open(save_name, "wb") as output:
			pickle.dump(self, output)
			


	def load(self):
		if os.path.exists(save_name):
			with open(save_name, "rb") as f:
		
				return pickle.load(f)
		return ApplicationDatabase()
