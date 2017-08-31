import _pickle as pickle
import os

save_name = "data.b"

class Database:

	def __init__(self):
		self.__staff_list = []
		self.__admin_list = []
		self.__public_list = []
		self.__rso_list = []

#---ADDING TO LISTS------------------------------
	def add(self, lst, obj):
		try:
			lst.append(obj)
			return True
		except:
			return False

	def add_staff(self, obj):
		return add(self, __staff_list, obj)

	def add_admin(self, obj):
		return add(self, __admin_list, obj)

	def add_public(self, obj):
		return add(self, __public_list, obj)

	def add_rso(self, obj):
		return add(self, __rso_list, obj)
#------------------------------------------------

#---REMOVING FROM LISTS--------------------------
	def remove(self, lst, obj):
		try:
			lst.remove(obj)
			return True
		except:
			return False

	def remove_staff(self, obj):
		return remove(self, __staff_list, obj)

	def remove_admin(self, obj):
		return remove(self, __admin_list, obj)

	def remove_public(self, obj):
		return remove(self, __public_list, obj)

	def remove_rso(self, obj):
		return remove(self, __rso_list, obj)
#------------------------------------------------

#---SAVING/LOADING-------------------------------
	def save(self):
		with open(save_name, "wb") as output:
			pickle.dump(self, output)

	def load(self):
		if os.path.exists(save_name):
			with open(save_name, "rb") as f:
				return pickle.load(f)
		return __init__(self)

	def reset_database():
		if os.path.exists(save_name):
			os.remove(save_name)
			return True
		return False
#------------------------------------------------








