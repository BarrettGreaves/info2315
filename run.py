from bottle import route, get, run, post, request, redirect, static_file
from bottle import request, response
from Crypto.Hash import MD5
import re
import numpy as np
from Database import Database
from Accounts import PublicAccount, AdminAccount, StaffAccount, Accounts
from Application import Application
from ApplicationDatabase import ApplicationDatabase
from Vehicle import Vehicle
from VehicleDatabase import VehicleDatabase
from bottle import run, get, post, request, response
from Backend import Permissions

import requests
import json

#-----------------------------------------------------------------------------
# This class loads html files from the "template" directory and formats them using Python.
# If you are unsure how this is working, just
class FrameEngine:
    def __init__(this,
        template_path="templates/",
        template_extension=".html",
        **kwargs):
        this.template_path = template_path
        this.template_extension = template_extension
        this.global_renders = kwargs

    def load_template(this, filename):
        path = this.template_path + filename + this.template_extension
        file = open(path, 'r')
        text = ""
        for line in file:
            text += line
        file.close()
        return text

    def simple_render(this, template, **kwargs):
        template = template.format(**kwargs)
        return template

    def render(this, template, **kwargs):
        keys = this.global_renders.copy() #Not the best way to do this, but backwards compatible from PEP448, in Python 3.5+ use keys = {**this.global_renters, **kwargs}
        keys.update(kwargs)
        template = this.simple_render(template, **keys)
        return template

    def load_and_render(this, filename, header="header", tailer="tailer", **kwargs):
        template = this.load_template(filename)
        rendered_template = this.render(template, **kwargs)
        #rendered_template = this.load_template(header) + rendered_template
        #rendered_template = rendered_template + this.load_template(tailer)
        return rendered_template

#-----------------------------------------------------------------------------

# Allow image loading
@route('/img/<picture>')
def serve_pictures(picture):
    return static_file(picture, root='img/')

# Allow CSS
@route('/css/<css>')
def serve_css(css):
    return static_file(css, root='css/')

# Allow javascript
@route('/js/<js>')
def serve_js(js):
    return static_file(js, root='js/')

host_addr = "localhost"
frontend_port = 8080
backend_port = 8081

backend_str = "http://{host}:{port}".format(host=host_addr, port=backend_port)

#-----------------------------------------------------------------------------
# Homepage
@route('/')

@route('/home')
def index():
		return fEngine.load_and_render("home")



# Display the login page
@get('/login')
def login():
    return fEngine.load_and_render("home")

@get('/logout')
def logout():
	response.set_cookie('visited',"")
	return fEngine.load_and_render("home")

# Attempt the login
@post('/login')
def do_login():
	username = request.forms.get('username')
	password = request.forms.get('password')

	responses = requests.post("{target}/api/login/{username}/{password}"
    	.format(target=backend_str, username=username, password=password))
	result = json.loads(responses.text)
	if result["key"]=="fail":
		response.set_cookie('visited',"")
		return fEngine.load_and_render("invalid", reason="Username not found")
	else:
		response.set_cookie('visited', result["cookie"])
		if result["type"]=="public":
			if result["rso"]=="False":
				return fEngine.load_and_render("publicAccount", username=username)
			else:
				return fEngine.load_and_render("safetyOfficerAccount", username=username)
		else:
			return fEngine.load_and_render("staffAccount", username=username)

@get('/register')
def register():
    return fEngine.load_and_render("register")

@post('/register')
def do_register():
	username = request.forms.get('username')
	password = "{}".format(request.forms.get('password'))
	rso = request.forms.get('rso')

	response = requests.post("{target}/api/register/{username}/{password}/{rso}"
    	.format(target=backend_str, username=username, password=password,rso=rso))
	result = json.loads(response.text)
	bool = result["key"]

	if(bool == True):
		return fEngine.load_and_render("registered", user_id=username)
	else:
		return fEngine.load_and_render("invalid", reason="account existed")

@get('/accounts')
def view_accounts():
	response = requests.post("{target}/api/viewaccount".format(target=backend_str))
	return response.text

@get('/reset')
def reset():
    response = requests.post("{target}/api/reset".format(target=backend_str))
    return fEngine.load_and_render("reset")

#Display Account page
@get('/publicAccount')
def about():
    return fEngine.load_and_render("publicAccount",username="")

@get('/staffAccount')
def about():
    return fEngine.load_and_render("staffAccount",username="")

@get('/safetyOfficerAccount')
def about():
    return fEngine.load_and_render("safetyOfficerAccount",username="")

#Display license application page
@get('/applyLicense')
def license():
	return fEngine.load_and_render("standardUser/apply")
#PUBLIC
#-----------------------------------------------------------------------------
#Apply for license
@post('/applyLicense')
def do_license():
	givenName = request.forms.get('givenName')
	surname = request.forms.get('surname')
	dob = request.forms.get('dob')
	address = request.forms.get('address')
	postcode = request.forms.get('postcode')
	email = request.forms.get('email')
	number = request.forms.get('number')
	cookie= request.get_cookie('visited')

	responses = requests.post("{target}/api/applyLicense/{givenName}/{surname}/{dob}/{address}/{postcode}/{email}/{number}/{cookie}"
    	.format(target=backend_str, givenName=givenName, surname=surname,dob=dob,address=address,postcode=postcode,email=email,number=number,cookie=cookie))
	if responses.text=="success":
		return fEngine.load_and_render("standardUser/licenseApplied")
	else:
		fEngine.load_and_render("home")

#Display Vehicle Registration page
@get('/registerVehicle')
def registerVehicle():
	return fEngine.load_and_render("standardUser/registerVehicle")

#Register vehicle
@post('/registerVehicle')
def do_registerVehicle():
	vehicleType = request.forms.get('type')
	rego = request.forms.get('rego')
	make = request.forms.get('make')
	model = request.forms.get('model')
	licence = request.forms.get('licence')
	address = request.forms.get('address')
	postcode = request.forms.get('postcode')
	purchase = request.forms.get('purchase')
	number = request.forms.get('number')
	vec=Vehicle(user,vehicleType,rego,make,model,licence,address,postcode,purchase,number)

	return fEngine.load_and_render("standardUser/registeredVehicle")

#Display current fines
@get('/viewFines')
def viewFines():
	return fEngine.load_and_render("standardUser/finedemeritview")

#Display destroyed vehicle form
@get('/destroyed')
def destroyed():
	return fEngine.load_and_render("standardUser/destroyed")


@post('/destroyed')
def do_destroyed():
	rego = request.forms.get('rego')
	message = request.forms.get('message')
	suburb = request.forms.get('suburb')
	road = request.forms.get('road')
	police = request.forms.get('police')
	return fEngine.load_and_render("standardUser/destroyedConfirmation")

#Display vehicle sale form
@get('/vehicleSale')
def vehicleSale():
	return fEngine.load_and_render("standardUser/sellVehicle")

@post('/vehicleSale')
def do_vehicleSale():
	vehicleType = request.forms.get('type')
	rego = request.forms.get('rego')
	make = request.forms.get('make')
	oldModel = request.forms.get('model')
	newname = request.forms.get('newname')
	sold = request.forms.get('sold')
	price = request.forms.get('price')
	return fEngine.load_and_render("standardUser/saleConfirmation")

@get('/renewLicense')
def renewLicense():
	return fEngine.load_and_render("standardUser/renewalform")

@post('/renewLicense')
def do_renewLicense():
	givenName = request.forms.get('givenName')
	surname = request.forms.get('surname')
	dob = request.forms.get('dob')
	address = request.forms.get('address')
	postcode = request.forms.get('postcode')
	email = request.forms.get('email')
	number = request.forms.get('number')
	licence = request.forms.get('licence')
	expired = request.forms.get('expired')
	return fEngine.load_and_render("standardUser/renewalConfirmation")

#STAFF
#-----------------------------------------------------------------------------
@get('/applicationApproval')
def applicationApproval():
	responses = requests.post("{target}/api/applicationApproval".format(target=backend_str))
	ApplicationList= responses.text
	return fEngine.load_and_render("staffUser/applicationapproval",ApplicationList=ApplicationList)

@post('/applicationApproval')
def applicationApproval():
	id=request.forms.get('id')
	accept=request.forms.get('accept')
	responses = requests.post("{target}/api/applicationApproval/{id}/{accept}"
    	.format(target=backend_str, id=id,accept=accept))

	responses = requests.post("{target}/api/applicationApproval".format(target=backend_str))
	ApplicationList= responses.text

	return fEngine.load_and_render("staffUser/applicationapproval",ApplicationList=ApplicationList)

@get('/destructionApproval')
def destructionApproval():
	return fEngine.load_and_render("staffUser/destructionApproval")

@get('/vehicleSaleApproval')
def vehicleSaleApproval():
	return fEngine.load_and_render("staffUser/vehicleSaleApproval")

@get('/payments')
def payments():
	return fEngine.load_and_render("staffUser/payments")

#SAFETY OFFICER
#-----------------------------------------------------------------------------
@get('/fines')
def fines():
	return fEngine.load_and_render("rsoUser/demerit")

@post('/fines')
def do_fines():
	firstname = request.forms.get('firstname')
	lastname = request.forms.get('lastname')
	license = request.forms.get('license')
	licenseType = request.forms.get('type')
	vehicle = request.forms.get('vehicle')
	return fEngine.load_and_render("rsoUser/demerit")



#-----------------------------------------------------------------------------


usr = None
fEngine = FrameEngine()
backend = Backed().load()

run(host=host_addr, port=frontend_port)
