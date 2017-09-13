from bottle import route, get, run, post, request, redirect, static_file
from bottle import request, response
from Crypto.Hash import MD5
import re
import numpy as np
from Database import Database
from Accounts import PublicAccount
from Application import Application
from ApplicationDatabase import ApplicationDatabase

from time import gmtime, strftime

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
        rendered_template = this.load_template(header) + rendered_template
        rendered_template = rendered_template + this.load_template(tailer)
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


    if username != "admin": # Wrong Username
        err_str = "Incorrect Username"
        return err_str, login
    
    if password != "password":
        err_str = "Incorrect Password"
        return err_str, login

    login_string = "Logged in!"
    login = True
    return login_string, login
    
#-----------------------------------------------------------------------------
# Homepage
@route('/')

@route('/home')
def index():
	cookie= request.get_cookie('visited')
	if cookie=="":
		return fEngine.load_and_render("index",user="")
	
	return fEngine.load_and_render("index",user=db.find_user_cookie(cookie))

# Display the login page
@get('/login')
def login():
    return fEngine.load_and_render("login")
@get('/logout')
def logout():
	response.set_cookie('visited',"")
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
		response.set_cookie('visited',"")
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
# Apply for license
@get('/apply_license')
def apply_license():
    return fEngine.load_and_render("apply_license")
@get('/accept_revoke')
def accept_revoke():
    return fEngine.load_and_render("accept_revoke")
@post('/accept_revoke')
def do_accept_revoke():
	id=request.forms.get('id')
	ar=request.forms.get('accept')
	if ar:
		adb.approve_application(adb.get_application(id))
	else:
		adb.revoke_application(adb.get_application(id))
	
	
	
	
    return fEngine.load_and_render("accept_revoke")
@post('/apply_license')
def do_apply_license():
	
	license = request.forms.get('license')
	description = request.forms.get('description')
	cookie= request.get_cookie('visited')
	user=db.find_user_cookie(cookie)
	
	if user is not None:
		app= Application(user,license,description,strftime("%Y-%m-%d %H:%M:%S", gmtime()))	
		adb.add_application(app)
	
	adb.save()
	adb.load()
	print(str(adb))
	adb.save()
	return fEngine.load_and_render("apply_license")	
@get('/applications')
def applications():
	
	adb.load()
	return str(adb)



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

@get('/about')
def about():
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.", 
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace diversity and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from generation X and is on the runway heading towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return fEngine.load_and_render("about", garble=np.random.choice(garble))

#-----------------------------------------------------------------------------
adb=ApplicationDatabase().load()
db = Database().load()

fEngine = FrameEngine()
run(host='localhost', port=8082, debug=True)
