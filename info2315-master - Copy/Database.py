import _pickle as pickle
import os

save_name = "data.b"

class Database:

	def __init__(self):
		self.user_lists = {"staff":[], "admin":[], "public":[]}

	def __str__(self):
		s = ""
		for key in self.user_lists:
			s += key + ": "
			for acc in self.user_lists[key]:
				s += acc.name + " "
			s += "</br>"
		return s

	def account_exists(self, name):
		for user_type in self.user_lists:
			if any(obj.name == name for obj in self.user_lists[user_type]):
				return True
		return False
	def account_verify(self,name,password):
		for user_type in self.user_lists:
			for obj in self.user_lists[user_type]:
				if obj.name == name:
					return obj.verify_password(password)
	def get_type(self,name):
		for user_type in self.user_lists:
			for obj in self.user_lists[user_type]:
				if obj.name == name:
					return user_type
		return "error"
	def get_user_id(self,name):
		for obj in self.user_lists[user_type]:
			if obj.name == name:
				return obj.user_id
		return ""
	def get_user_cookie(self,name):
		for user_type in self.user_lists:
			for obj in self.user_lists[user_type]:
				if obj.name == name:
					return obj.cookie
		return None
	def find_user_cookie(self,cookie):
		for user_type in self.user_lists:
			for obj in self.user_lists[user_type]:
				if obj.cookie == cookie:
					return obj.name
		return None
		

	def get_account(self, name):
		for user_type in self.user_lists:
			for obj in self.user_lists[user_type]:
				if obj.name == name:
					return obj
		return None

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

	def reset(self):
		#if logs are persisent, overwrite file rather than removing
		if os.path.exists(save_name):
			os.remove(save_name)
		self.user_lists = {"staff":[], "admin":[], "public":[]}
#------------------------------------------------








