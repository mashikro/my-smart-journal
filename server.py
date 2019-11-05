################# Necessary IMPORTS ############################
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, redirect 
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db

import bcrypt
 
#################### FLASK APP SET-UP ####################################
app = Flask(__name__)

app.secret_key = "ilovedogs" #CHANGE THIS AT SOME POINT

app.jinja_env.undefined = StrictUndefined #to prevent silent but deadly jinja errors

######################### ROUTES #####################################
@app.route('/') # this will be where you can got to log in / create account
def index():
    '''Index. User can either 'create an account' or 'login here' '''
    
    #USE session to handle if it is a returning user to show create account vs login
    return render_template('index.html') 


@app.route('/create-account', methods=['GET'])
def create_account_form():

    return render_template('create_account.html')


@app.route('/create-account', methods=['POST'])
def create_user_process():
    '''User is able to create an account'''

# Will get all this info back:
    # email
    # password (bcrypt.hashpw(b'', bcrypt.gensalt()))
    # fname
    # lname
    # phone_num
    # texting_enabled

#Instatitate a new user add and commit them to db
    # new_user = User()

    # db.session.add(new_user)
    # db.session.commit()
 
    return '<html><body>I WANT you to be a user</body></html>'

@app.route('/login', methods=['GET'])
def login_form():
    '''Login form'''
    pass


@app.route('/login', methods=['POST'])
def login_process():
    '''Authenticate user'''
# Will get this info back
    # email
    # password (bcrypt.checkpw(password, hashed))

    # turning things to b str: b = mystring.encode('utf-8')



# Will query for the user with this email (emails are unique)
    # user = User.query.filter_by(email=email).first()

#User authentication
    # if not user:
    #     flash("Sorry, the user with that email doesn't exist. Please try again :)")
    #     return redirect("/login")

    # if user.password != password:
    #     flash("Oops :0 Incorrect password! Please try again :)")
    #     return redirect("/login")

# Will add user to session
    # session["user_id"] = user.user_id

# Will have a flash message
    # flash("Welcome back! We missed you <3")

    # return redirect('/home')

@app.route('/logout')
def logout_process():
    '''Log user out'''

    # del session["user_id"] # delete session
    # flash("See you soon:) You are now logged out.")
    # return redirect("/") #root

@app.route('/home', methods=['GET'])
def show_homepage():
    '''Homepage. User's can make entries to the journal here '''

    return '<html><body>homepage</body></html>'

@app.route('/home', methods=['POST'])
def process_journal_entry():
    '''Save journal entry to backend'''
    #get data from form
    #using that data instantiate a new journal entry

    # db.session.add(new_journal_entry)
    # db.session.commit()

    pass

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





  