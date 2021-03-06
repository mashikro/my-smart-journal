############## CREATING TO DATABASE ############################
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy.dialects.postgresql import ENUM

# from collections import defaultdict

db = SQLAlchemy()

#################### MODEL DEFINITIONS ##########################

class User(db.Model):
    '''All user and user info will live here'''
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(50), nullable=False )
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique= True, nullable=False)
    password_hash = db.Column(db.LargeBinary, nullable=False) #storing passwords as byte strings
    phone_number = db.Column(db.String(30), nullable=False)
    texting_enabled = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<User: email-{email} fname-{fname}>'.format(email=self.email, 
                                                            fname=self.fname)


class JournalEntry(db.Model):
    '''All user's journal entries will live here'''

    __tablename__ = 'journal_entries'

    entry_type_enum = ENUM('morning', 'night', name='entry_type_enum')

    entry_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    entry_type = db.Column(entry_type_enum, nullable=False)
    date = db.Column(db.Date, nullable=False) #confirm timezone=False OR change to db.Date()
    q1_text = db.Column(db.Text, nullable=False)
    q2_text = db.Column(db.Text, nullable=False)
    q3_text = db.Column(db.Text, nullable=False)
    happ_score = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref='journal_entries') #should i make it entries because its one to many?

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '''<JournalEntry: date-{date} 
                entry_type-{entry_type} 
                entry_id-{entry_id} 
                user_email-{user_email}>'''.format(date=self.date, 
                                                    entry_type=self.entry_type,
                                                    entry_id=self.entry_id,
                                                    user_email=self.user.email)
################# EXAMPLE DATA FOR TESTING #####################
def example_data():
    """Create some sample data."""

    some_user = User(user_id=1,
                    fname='Misha', 
                    lname='Bear', 
                    email='mbear@gmail.com', 
                    password_hash=b'123', 
                    phone_number="3475123182", 
                    texting_enabled=True)

    an_entry = JournalEntry(entry_id=1,
                            user_id=1,
                            entry_type='morning', 
                            date="11/27/2019",
                            q1_text="happy, smiley",
                            q2_text="study",
                            q3_text="I am smart",
                            happ_score=5)

    db.session.add_all([some_user, an_entry])
    db.session.commit()

############## CONNECTING TO DATABASE ##########################

def connect_to_db(app, dbname):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{dbname}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app 

    connect_to_db(app, "journals")
    print("Connected to DB.")