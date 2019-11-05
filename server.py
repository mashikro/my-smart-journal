################# Necessary IMPORTS ############################
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, redirect 
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db
 
#################### FLASK APP SET-UP ####################################
app = Flask(__name__)
app.secret_key = "ilovedogs" #CHANGE THIS AT SOME POINT
app.jinja_env.undefined = StrictUndefined #to prevent silent but deadly jinja errors

######################### ROUTES #####################################
@app.route('/') # this will be where you can got to log in / create account
def index():
    '''Login. User can either 'create an account' or 'login here' '''
    
    #USE session to handle if it is a returning user to show create account vs login
    return '<html><body>Hey this doesnt exist yet, but you will be able to login here</body></html>'

@app.route('/create-account')
def create_user():
    '''User is able to create an account'''

    return '<html><body>I WANT you to be a user</body></html>'

@app.route('/home')
def show_homepage():
    '''Homepage. User's can make entries to the journal here '''

    return '<html><body>homepage</body></html>'

@app.route('/history')
def show_history():
    '''History of all entries'''
    pass

@app.route('/view-entry')
def show_single_entry():
    '''Single entry'''
    pass

@app.route('/happy')
def show_hap_stats():
    '''Happiness Stats page'''
    pass

@app.route('/profile')
def view_profile():
    '''Show Profile page/settings'''
    pass





####################### RUNNING MY SERVER ###############################
if __name__ == "__main__":
   
    app.debug=True # We have to set debug=True here, since it has to be True at the point that we invoke the DebugToolbarExtension

    connect_to_db(app)

    DebugToolbarExtension(app) # Use the DebugToolbar

    app.run(host="0.0.0.0") 
  