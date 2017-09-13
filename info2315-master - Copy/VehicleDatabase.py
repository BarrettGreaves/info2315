import _pickle as pickle
import os

save_name = "data2.b"
class VehicleDatabase:
	def __init__(self):
		self.vehicle_list=[]
		
	def get_vehicle(self,id):
		
		for a in self.vehicle_lists:
			if any(obj.id ==id for obj in self.a):
				return obj
		
		
		
	def add_vehicle(self, application):
		
			self.vehicle_list.append(application)
			self.save()
			return True
		
	def destroy(self,application):
		for app in self.vehicle_list:
			if app==application:
				app.destroy=True
	
				
				
				
				
				
	def save(self):
		with open(save_name, "wb") as output:
			pickle.dump(self, output)
			


	def load(self):
		if os.path.exists(save_name):
			with open(save_name, "rb") as f:
		
				return pickle.load(f)
		return ApplicationDatabase()
