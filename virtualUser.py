import requests
import time
from random import randint

host_addr = "localhost"
port = "8080"
site = "http://{host}:{port}".format(host=host_addr, port=port)
randomUser = randint(0,4)

#Request types

home = "/home"
login = "/login"
register = "/register"
registered = "/registered"
applyLicense = "/applyLicense"
publicAccount = "/publicAccount"
viewFines = "/viewFines"
logout = "/logout"
registerVeh = "/registerVehicle"
destroyed = "/destroyed"
staffAccount = "/staffAccount"
applications = "/applicationApproval"
payments = "/payments"
reset = "/reset"
accounts = "/accounts"

#PUBLIC
def publicUserOne():
	requests.get(site + home)
	time.sleep(5)
	requests.post(site + register, data = {'username': 'Freeda.Innocent', 'password': '123456', 'rso': False})
	requests.get(site + registered)
	time.sleep(2)
	requests.get(site + login)
	time.sleep(3)
	requests.post(site + login, data = {'username': 'Freeda.Innocent', 'password': '123456'})
	requests.get(site + publicAccount)
	time.sleep(3)
	requests.get(site + applyLicense)
	time.sleep(5)
	requests.post(site + applyLicense, data = {'givenName': 'Freeda','surname': 'Innocent','dob': '1999-01-01','address': '1%20Security%20Place','postcode':'2000','email':'freeda.innocent@2315.com','number':'0400500600'})
	requests.get(site + publicAccount)
	time.sleep(3)
	requests.get(site + viewFines)
	time.sleep(3)
	requests.post(site + logout)
	return

def publicUserTwo():
	requests.get(site + home)
	time.sleep(2)
	requests.post(site + register, data = {'username': 'Jeane.Poole', 'password': 'password', 'rso': False})
	requests.get(site + registered)
	time.sleep(5)
	requests.get(site + login)
	time.sleep(3)
	requests.post(site + login, data = {'username': 'Jeane.Poole', 'password': 'password'})
	requests.get(site + publicAccount)
	time.sleep(6)
	requests.get(site + registerVeh)
	time.sleep(2)
	requests.post(site + registerVeh, data = {'vehicleType': 'Sedan','rego': 'AQQ124','make': 'VW','model': 'Golf','licence':'18555883','address':'1%20Security%20Place','postcode':'2000','purchase':'2017-01-01','number': '0400000000'})
	requests.get(site + publicAccount)
	time.sleep(4)
	requests.get(site + destroyed)
	requests.post(site + destroyed, data = {'rego': 'AQQ124','message': 'Car accident.','suburb': 'Sydney','road': 'George St','police':True})
	time.sleep(5)
	requests.post(site + logout)
	return

#STAFF

def staffOne():
	requests.get(site + home)
	time.sleep(5)
	requests.get(site + login)
	time.sleep(3)
	requests.post(site + login, data = {'username': 'staff', 'password': 'staff'})
	requests.get(site + staffAccount)
	time.sleep(3)
	requests.get(site + applications)
	time.sleep(4)
	requests.post(site + applications, data = {'id': 'b837be50', 'accept': True})
	requests.get(site + staffAccount)
	time.sleep(3)
	requests.post(site + logout)
	return

def staffTwo():
	requests.get(site + home)
	time.sleep(5)
	requests.get(site + login)
	time.sleep(3)
	requests.post(site + login, data = {'username': 'staff', 'password': 'staff'})
	requests.get(site + staffAccount)
	time.sleep(3)
	requests.get(site + payments)
	requests.get(site + staffAccount)
	time.sleep(3)
	requests.post(site + logout)
	return

#ADMIN

def adminOne():
	requests.get(site + home)
	time.sleep(5)
	requests.get(site + login)
	time.sleep(3)
	requests.get(site + reset)
	time.sleep(3)
	requests.get(site + accounts)
	return


if randomUser == 0:
	publicUserOne()
elif randomUser == 1:
	publicUserTwo()
elif randomUser == 2:
	staffOne()
elif randomUser == 3:
	staffTwo()
else:
	adminOne()
