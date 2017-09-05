import _pickle as pickle
import os

save_name = "data.b"

class Database:

	def __init__(self):
		self.user_lists = {"staff":[], "admin":[], "public":[], "rso":[]}

	def account_exists(self, user_id):
		for user_type in self.user_lists:
			if any(obj.user_id == user_id for obj in self.user_lists[user_type]):
				return True
		return False


#---ADDING TO LISTS------------------------------
	def add(self, lst, obj):
		try:
			self.user_lists[lst].append(obj)
			return True
		except:
			return False

	def add_staff(self, obj):
		return self.add("staff", obj)

	def add_admin(self, obj):
		return self.add("admin", obj)

	def add_public(self, obj):
		return self.add("public", obj)

	def add_rso(self, obj):
		return self.add("rso", obj)
#------------------------------------------------

#---REMOVING FROM LISTS--------------------------
	def remove(self, lst, obj):
		try:
			self.user_lists[lst].remove(obj)
			return True
		except:
			return False

	def remove_staff(self, obj):
		return self.remove("staff", obj)

	def remove_admin(self, obj):
		return self.remove("admin", obj)

	def remove_public(self, obj):
		return self.remove("public", obj)

	def remove_rso(self, obj):
		return self.remove("rso", obj)
#------------------------------------------------

#---SAVING/LOADING-------------------------------
	def save(self):
		with open(save_name, "wb") as output:
			pickle.dump(self, output)

	def load(self):
		if os.path.exists(save_name):
			with open(save_name, "rb") as f:
				return pickle.load(f)
		return Database()

	def reset_database():
		if os.path.exists(save_name):
			os.remove(save_name)
			return True
		return False
#------------------------------------------------








