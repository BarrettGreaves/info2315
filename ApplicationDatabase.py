import _pickle as pickle
import os

save_name = "data1.b"
class ApplicationDatabase:
	def __init__(self):
		self.application_list=[]
		
	def get_application(self,id):
		
		for a in self.application_list:
			if a.id == id :
				return a
		
	def display(self):
		str=""
		for a in self.application_list:
			str+=a.display()
		return str
		
	def add_application(self, application):
		
			self.application_list.append(application)
			self.save()
			return True
		

	def approve_application(self,application,str):
		for app in self.application_list:
			if app==application:
				app.approve=str
				
				
				
				
				
				
	def save(self):
		with open(save_name, "wb") as output:
			pickle.dump(self, output)
			


	def load(self):
		if os.path.exists(save_name):
			with open(save_name, "rb") as f:
				return pickle.load(f)
		return Database()
