##############CREATING TO DATABASE############################
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
# import datetime

# from collections import defaultdict

db = SQLAlchemy()

####################MODEL DEFINITIONS##########################

class User(db.Model):
    '''All user and user info will live here'''
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(50), nullable=False )
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique= True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False) #not sure how long this will be yet
    phone_number = db.Column(db.String(30), nullable=False)
    texting_enabled = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""



class JournalEntry(db.Model):
    '''All user's journal entries will live here'''

    __tablename__ = 'journal_entries'

    entry_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date = db.Column(db.Date, nullable=False) #confirm timezone=False OR change to db.Date()
    entry_type = db.Column(db.String(10), nullable=False)
    text = db.Column(db.Text, nullable=False)
    happ_score = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref='journal_entries') #should i make it entries because its one to many?

    def __repr__(self):
        """Provide helpful representation when printed."""

##############CONNECTING TO DATABASE##########################

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///journals'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app #FLASK IS NOT CREATED YET

    connect_to_db(app)
    print("Connected to DB.")