################# Necessary IMPORTS ############################
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, redirect, session, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension

import os

from model import connect_to_db, db, User, JournalEntry

import bcrypt

from streak import main

from happiness import get_happiness_data

from aws_comprehend import do_sentiment_analysis

from aws_comp_key_phrases import create_actions_list
 
#################### FLASK APP SET-UP ####################################
app = Flask(__name__)

app.secret_key = os.environ['FLASK_SECRET_KEY']

app.jinja_env.undefined = StrictUndefined #to prevent silent but deadly jinja errors

######################### HELPER FUNCTIONS ##############################
def encrypt_pass_bytes(password):
    '''Encrypts passwords using bcrypt'''
   
    b = password.encode('utf-8') # turning things to b str: b = mystring.encode('utf-8')
    password_hash = bcrypt.hashpw(b, bcrypt.gensalt())
    return password_hash

######################### ROUTES #####################################
@app.route('/') 
def index():
    '''Index. User can either 'create an account' or 'login here' '''
    
    return render_template('index.html') 


# @app.route('/create-account', methods=['GET'])
# def create_account_form():
#     '''User's can create an account'''

#     return render_template('create_account_form.html')


@app.route('/create-account', methods=['POST'])
def create_user_process():
    '''Add user to the database'''

# Will get all this info back:
    email = request.form.get('email')
    password_hash = encrypt_pass_bytes(request.form.get('password'))
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    phone_number = request.form.get('phone_number')
    texting_enabled = (request.form.get('texting_enabled') == 'true') #checks 'true' == 'true'

#checks if a user w that email already exists, if 'True' redirects them to try again.
    user = User.query.filter_by(email=email).first()

    if user:
        flash('''Sorry this email is already being used. 
            Try again with a different email address.''')
        
        return redirect('/')
    
#Instatitate a new user add and commit them to db
    new_user = User(email=email, 
                    password_hash=password_hash, 
                    fname=fname, 
                    lname=lname, 
                    phone_number=phone_number, 
                    texting_enabled=texting_enabled)

    db.session.add(new_user)
    db.session.commit()
 
    return redirect('/')


# @app.route('/login', methods=['GET'])
# def login_form():
#     '''Login form'''
    
#     return render_template('login_form.html')


@app.route('/login', methods=['POST'])
def login_process():
    '''Authenticate user'''

# Will get this info back
    email = request.form.get('email')
    password = request.form.get('password')

# Will query for the user with this email (emails are unique)
    user = User.query.filter_by(email=email).first()

#User authentication
    if not user:
        flash("Sorry, the user with that email doesn't exist. Please try again :) ")
        return redirect('/')
   
    if bcrypt.checkpw((password.encode('utf-8')), user.password_hash): #this checks if the entered pass matches decrypted pass_hash
        # Will add user to session
        session['user_id'] = user.user_id
        # print('LOOOOOOOOK',session['user_id'])

        # Will have a flash message
        flash('Welcome! We missed you <3')

        return redirect('/home')
    
    # if pass doesnt match:
    else:
        flash('Oops :0 Incorrect password! Please try again :)')
        return redirect('/')


@app.route('/logout')
def logout_process():
    '''Log user out and remove from session'''
    user_id = session.get('user_id')
    
    if user_id:
        del session['user_id'] # delete session
        flash('See you soon:) You are now logged out.')
    
    return redirect("/") #root


@app.route('/home', methods=['GET'])
def show_homepage():
    '''Homepage. User's can make journal entries'''

    user_id = session.get('user_id')

    if user_id:
        return render_template('mk_journal_entry.html')
    else:
        return redirect('/')


@app.route('/home', methods=['POST'])
def process_journal_entry():
    '''Save journal entry to database'''
    
    #get data from form
    date = request.form.get('date')
    entry_type = request.form.get('entry_type')
    
    q1_text_mor = request.form.get('mor_q1_entry')
    q2_text_mor = request.form.get('mor_q2_entry')
    q3_text_mor = request.form.get('mor_q3_entry')
    
    q1_text_night = request.form.get('night_q1_entry')
    q2_text_night = request.form.get('night_q2_entry')
    q3_text_night = request.form.get('night_q3_entry')

    happ_score = request.form.get('happ_score')
   

    #using that data instantiate a new journal entry depending on entry type
    if entry_type == 'morning':
        new_journal_entry = JournalEntry(user_id = session['user_id'],
                                        date=date,
                                        entry_type=entry_type,
                                        q1_text=q1_text_mor,
                                        q2_text=q2_text_mor,
                                        q3_text=q3_text_mor,
                                        happ_score=happ_score)
    else:
        new_journal_entry = JournalEntry(user_id = session['user_id'],
                                date=date,
                                entry_type=entry_type,
                                q1_text=q1_text_night,
                                q2_text=q2_text_night,
                                q3_text=q3_text_night,
                                happ_score=happ_score)

    # add and commit to backend
    db.session.add(new_journal_entry)
    db.session.commit()

    return redirect('/history')


@app.route('/history')
def show_history():
    '''History of all entries. Users can sort/filter. Graph of streaks are displayed'''

    user_id = session.get('user_id')
    journal_entries = JournalEntry.query.filter_by(user_id=user_id)

    sorting = request.args.get('sort')
    filtering = request.args.get('filter')

    if user_id: 
        
        if sorting:
            journal_entries = journal_entries.order_by(JournalEntry.date.desc())

        if filtering:
            journal_entries = journal_entries.filter_by(entry_type=filtering)  
        
        journal_entries = journal_entries.all()

        return render_template('history_of_entries.html', 
                                journal_entries_lst=journal_entries)

    else:
        return redirect('/')


@app.route('/view-entry/<int:entry_id>')
def show_single_entry(entry_id):
    '''View single entry based on entry type'''

    single_journal_entry = JournalEntry.query.filter_by(entry_id=entry_id).first()

    if single_journal_entry.entry_type == 'morning':
        return render_template('single_entry_view.html', single_journal_entry=single_journal_entry)
    else:
        return render_template('night_single_entry_view.html', single_journal_entry=single_journal_entry)


@app.route('/profile')
def view_profile():
    '''Show Profile page/settings'''

    user_id = session.get('user_id')

    if user_id:
        user = User.query.filter_by(user_id=user_id).first()
        return render_template('profile_page.html', user=user)    
    else:
        return redirect('/')


@app.route('/happy')
def show_happ_chart():
    '''Show happiness data. Show actionable items through word cloud.'''

    user_id = session.get('user_id')
    
    if user_id:
        return render_template('happy.html')
    else:
        return redirect('/')


@app.route('/happy.json')
def get_happ_stats():
    '''Get data ready for happiness graph'''

    #user session to get which user
    user_id = session.get('user_id')

    # call func and pass in user_id as param
    result = get_happiness_data(user_id)

    #data for happiness chart
    data_dict = {
            "labels": result[0],
            "datasets": [
                {
                    "label": 'Happiness Trend',
                    "borderColor": "#fef9ff",
                    "data": result[1],
                    "backgroundColor": "#71EDCE",
                    "hoverBackgroundColor": "#71EDCE",
                }]
        }

    return jsonify(data_dict)


# @app.route('/streak')
# def show_streak_chart():
#     '''Show streak data page'''    

#     user_id = session.get('user_id')
    
#     if user_id:
#         return render_template('streak.html')    
#     else:
#         return redirect('/')
    

@app.route('/streak.json')
def get_streak_stats():
    '''Get data ready for streak graph'''
  
    #user session to get which user
    user_id = session.get('user_id')

    # call func and pass in user_id as param
    result = main(user_id)

    data_dict = {
        "labels": result[0],
        "datasets": [
            {
                "label": 'Streak Trend',
                "borderColor": "#fef9ff",
                "data": result[1],
                "backgroundColor": "#71EDCE",
                "hoverBackgroundColor": "#71EDCE",
            }]
    }

    return jsonify(data_dict)


@app.route('/sentiment-analysis')
def show_sentiment_analysis_data():
    '''Show user data where sentiment analysis was performed'''    

    user_id = session.get('user_id')
    
    if user_id:
        return render_template('sentiment_analysis.html')
    else:
        return redirect('/')


@app.route('/sentiment-analysis.json')
def get_sentiment_analysis_data():
    '''Get data ready for sentiment analysis graph'''
  
    #user session to get which user
    user_id = session.get('user_id')

    # call func and pass in user_id as param
    result = do_sentiment_analysis(user_id)

    print('loook here masha', result[0])
    
    positives = []
    negatives = []
    neutrals = []

    #format data for json
    for inner_dict in result[1]:     
        positives.append(round(inner_dict['Positive'], 4))
        negatives.append(round(inner_dict['Negative'], 4))
        neutrals.append(round(inner_dict['Neutral'], 4))

    data_dict = {
        "labels": result[0],
        "datasets": [
            {
            "label": "Postive",
            "backgroundColor": "#71EDCE",
            "data": positives
            },
            {
            "label": "Negative",
            "backgroundColor": "#CC3553",
            "data": negatives
            }, 
            {
            "label": "Neutral",
            "backgroundColor": "#F2DC5D",
            "data": neutrals
            }
        ]
    }

    return jsonify(data_dict)


# @app.route('/action')
# def show_action_data():
#     '''Show user data where sentiment analysis was performed'''    

#     user_id = session.get('user_id')
    
#     if user_id:
#         return render_template('action.html') 

#     else:
#         return redirect('/')


@app.route('/action.json')
def get_action_data():
    '''Get data ready for happiness/action world cloud'''
  
    #user session to get which user
    user_id = session.get('user_id')

    # call func and pass in user_id as param & get a dict back
    result = create_actions_list(user_id) 

    list_words = list(result.items())

    data = {'data': list_words}

    return jsonify(data)
    

####################### RUNNING MY SERVER ###############################
if __name__ == "__main__":
   
    app.debug=True # We have to set debug=True here, since it has to be True at the point that we invoke the DebugToolbarExtension

    connect_to_db(app, "journals")

    DebugToolbarExtension(app) # Use the DebugToolbar

    app.run(host="0.0.0.0") 





  