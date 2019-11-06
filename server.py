################# Necessary IMPORTS ############################
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, JournalEntry

import bcrypt
 
#################### FLASK APP SET-UP ####################################
app = Flask(__name__)

app.secret_key = "ilovedogs" #CHANGE THIS AT SOME POINT

app.jinja_env.undefined = StrictUndefined #to prevent silent but deadly jinja errors

######################### HELPER FUNCTIONS ##############################
def encrypt_pass(password):
    '''Encrypts passwords using bcrypt'''
    b = password.encode('utf-8') # turning things to b str: b = mystring.encode('utf-8')
    password_hash = bcrypt.hashpw(b, bcrypt.gensalt())
    return password_hash

######################### ROUTES #####################################
@app.route('/') 
def index():
    '''Index. User can either 'create an account' or 'login here' '''
    
    #USE session to handle if it is a returning user to show create account vs login
    return render_template('index.html') 


@app.route('/create-account', methods=['GET'])
def create_account_form():

    return render_template('create_account_form.html')


@app.route('/create-account', methods=['POST'])
def create_user_process():
    '''User is able to create an account'''

    # Will get all this info back:
    email = request.form.get('email')
    password_hash = encrypt_pass(request.form.get('password'))
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    phone_number = request.form.get('phone_number')
    texting_enabled = bool(request.form.get('texting_enabled')) #fix 

   
   

#Instatitate a new user add and commit them to db
    new_user = User(email=email, 
                    password_hash=password_hash, 
                    fname=fname, 
                    lname=lname, 
                    phone_number=phone_number, 
                    texting_enabled=texting_enabled)

    db.session.add(new_user)
    db.session.commit()
 
    return redirect('/login')

@app.route('/login', methods=['GET'])
def login_form():
    '''Login form'''
    
    return render_template('login_form.html')


@app.route('/login', methods=['POST'])
def login_process():
    '''Authenticate user'''

# Will get this info back
    email = request.form.get('email')
    password = request.form.get('password')
    # b_password = password.encode('utf-8')

# Will query for the user with this email (emails are unique)
    user = User.query.filter_by(email=email).first()

#User authentication
    if not user:
        flash("Sorry, the user with that email doesn't exist. Please try again :) ")
        return redirect("/login")

   
    if bcrypt.checkpw((password.encode('utf-8')), user.password_hash): #this checks if the entered pass matches decrypted pass_hash
        # Will add user to session
        session["user_id"] = user.user_id

        # Will have a flash message
        flash("Welcome! We missed you <3")

        return redirect('/home')
    
    # if pass doesnt match:
    else:
        flash("Oops :0 Incorrect password! Please try again :)")
        return redirect("/login")



@app.route('/logout')
def logout_process():
    '''Log user out'''

    del session["user_id"] # delete session
    flash("See you soon:) You are now logged out.")
    return redirect("/") #root


@app.route('/home', methods=['GET'])
def show_homepage():
    '''Homepage. User's can make entries to the journal here '''

    return render_template('mk_journal_entry.html')


@app.route('/home', methods=['POST'])
def process_journal_entry():
    '''Save journal entry to backend'''
    
    #get data from form
    date = request.form.get('date')
    entry_type = request.form.get('entry_type')
    q1_text = request.form.get('q1_entry')
    q2_text = request.form.get('q2_entry')
    q3_text = request.form.get('q3_entry')
    happ_score = request.form.get('happ_score')

    #using that data instantiate a new journal entry
    new_journal_entry = JournalEntry(date=date,
                                    entry_type=entry_type,
                                    q1_text=q1_text,
                                    q2_text=q2_text,
                                    q3_text=q3_text,
                                    happ_score=happ_score)

    #add and commit to backend
    # db.session.add(new_journal_entry)
    # db.session.commit()

    return redirect('/history')

@app.route('/history')
def show_history():
    '''History of all entries'''
    
    return render_template('history_of_entries.html')


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





  