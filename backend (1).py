from bottle import route, get, run, post, request, redirect, static_file
from bottle import request, response
from Crypto.Hash import MD5
import re
import numpy as np
from Database import Database
from Accounts import PublicAccount,StaffAccount,AdminAccount
from Application import Application
from ApplicationDatabase import ApplicationDatabase
from Vehicle import Vehicle
from VehicleDatabase import VehicleDatabase
import json
# Important globals
host = "localhost"
port = "8081"


# Our "Database"
users = {}

# API calls
@post('/api/useradd/<username:path>/<password:path>')
def useradd(username, password):
	global users
	if username in users:
		return "User already exists"
	users[username] = password
	return "User added"


@post('/api/register/<username:path>/<password:path>/<rso:path>')
def register(username, password , rso):
	a=False
	if db.account_exists(username):
		a=False
	else:

		acc = PublicAccount(username, password, rso)
		user_id = acc.user_id
		db.add_public(acc)
		db.save()
		a=True
	return {'key': a}



@post('/api/login/<username:path>/<password:path>')
def login(username, password):
	if db.account_exists(username) and db.account_verify(username,password):
		cookie=db.get_user_cookie(username)

		type=db.get_type(username)
		if type=="public":
			print(db.get_account(username).rso)
			return {'key':"success",'cookie':db.get_user_cookie(username),'type':db.get_type(username),'rso':db.get_account(username).rso}

		else:
			return {'key':"success",'cookie':db.get_user_cookie(username),'type':db.get_type(username)}

	else:
		return{'key':"fail"}

@post('/api/applyLicense/<givenName:path>/<surname:path>/<dob:path>/<address:path>/<postcode:path>/<email:path>/<number:path>/<cookie:path>')
def applyLicense(givenName,surname,dob,address,postcode,email,number,cookie):
	user=db.find_user_cookie(cookie)
	print(givenName)
	app= Application(user, givenName,surname,dob,address,postcode,email,number)
	print(app.display())
	adb.add_application(app)
	return "success"


@post('/api/applicationApproval')
def applicationApproval():

	return adb.display()

@post('/api/applicationApproval/<id:path>/<accept:path>')
def home(id,accept):
	adb.approve_application(adb.get_application(id),accept)


	adb.save()
	return

@post('/api/login/<cookie:path>')
def home(cookie):
	username=db.find_user_cookie(cookie)
	type=db.get_type(username)
	if type=="public":
		return {'key':"success",'username':username,'type':type,'rso':db.get_account(username).rso}
	else:
		return {'key':"success",'username':username,'type':db.get_type(username)}



@post('/api/reset')
def reset():
	db.reset()
	registerAdmin("admin", "admin")
	registerStaff("staff", "staff")
	return

@post('/api/viewaccount')
def view():
	return str(db) + '''
</br>
<form action="/" method="get">
    <input value="Home" type="submit" />
</form>'''


def registerStaff(username, password):
	a=False
	if db.account_exists(username):
		a=False
	else:

		acc = StaffAccount(username, password)

		db.add_staff(acc)
		db.save()
		a=True
	return {'key': a}

def registerAdmin(username, password):
	a=False
	if db.account_exists(username):
		a=False
	else:

		acc = AdminAccount(username, password)

		db.add_admin(acc)
		db.save()
		a=True
	return {'key': a}




# Rather than using paths, you could throw all the requests with form data filled using the
# requests module and extract it here.
adb=ApplicationDatabase().load()
vdb=VehicleDatabase().load()
db = Database().load()
registerStaff("staff", "staff")
registerAdmin("admin", "admin")
# Run the server
run(host=host, port=port)
