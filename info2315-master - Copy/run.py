from bottle import route, get, run, post, request, redirect, static_file
from bottle import request, response
from Crypto.Hash import MD5
import re
import numpy as np
from Database import Database
from Accounts import PublicAccount

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

#-----------------------------------------------------------------------------

# Check the login credentials
def check_login(username, password):
    login = False
    acc = db.get_account(username)
    if not acc: #account not found
        err_str = "Account does not exist"
        return err_str, login
    if not acc.verify_password(password):
        err_str = "Incorrect password"
        return err_str, login
    usr = acc #ok bc method only allowed if usr == None
    err_str, login = "Logged in", True
    return err_str, login

#-----------------------------------------------------------------------------
# Homepage
@route('/')

@route('/home')
def index():
	cookie= request.get_cookie('visited')
	if cookie=="nocookie":
		return fEngine.load_and_render("home")
	return fEngine.load_and_render("home",user=db.find_user_cookie(cookie))

# Display the login page
@get('/login')
def login():
    return fEngine.load_and_render("login")
@get('/logout')
def logout():
	response.set_cookie('visited',"nocookie")
	return fEngine.load_and_render("login")

# Attempt the login
@post('/login')
def do_login():
	db.load()
	username = request.forms.get('username')
	password = request.forms.get('password')
	visits = request.get_cookie('visited')

	if db.account_exists(username) and db.account_verify(username,password):
		response.set_cookie('visited',db.get_user_cookie(username))
		return fEngine.load_and_render("valid", username=username)
	else:
		#response.set_cookie('visited',None)
		return fEngine.load_and_render("invalid", reason="Username not found")

@get('/register')
def register():
    return fEngine.load_and_render("register")

@post('/register')
def do_register():
	username = request.forms.get('username')
	password = "{}".format(request.forms.get('password'))
	if db.account_exists(username):
		return fEngine.load_and_render("invalid", reason="account existed")
	else:
		rso = request.forms.get('rso')
		acc = PublicAccount(username, password, rso)
		user_id = acc.user_id
		db.add_public(acc)
		db.save()
		return fEngine.load_and_render("registered", user_id=user_id)

@get('/accounts')
def view_accounts():
    return str(db) + '''
</br>
<form action="/" method="get">
    <input value="Home" type="submit" />
</form>'''

@get('/reset')
def reset():
    db.reset()
    return fEngine.load_and_render("reset")

#Display Account page
@get('/publicAccount')
def about():
    return fEngine.load_and_render("publicAccount")

@get('/staffAccount')
def about():
    return fEngine.load_and_render("staffAccount")

@get('/safetyOfficerAccount')
def about():
    return fEngine.load_and_render("safetyOfficerAccount")

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
	return fEngine.load_and_render("standardUser/licenseApplied")

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
	return fEngine.load_and_render("staffUser/applicationapproval")

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
db = Database().load()
usr = None
fEngine = FrameEngine()
run(host='localhost', port=8081, debug=True)
