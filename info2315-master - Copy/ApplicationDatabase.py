import _pickle as pickle
import os

save_name = "data1.b"
class ApplicationDatabase:
	def __init__(self):
		self.application_list=[]
		
	def get_application(self,id):
		
		for a in self.application_list:
			if any(obj.id == id for obj in self.a):
				return obj
		
		
		
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
		return Database()
