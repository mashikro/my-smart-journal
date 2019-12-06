import server
import model
import os
from twilio.rest import Client
import schedule
import time
import datetime

ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_PNUM = os.environ['TWILIO_PHONE_NUMBER']

def check_for_credentials(account_sid, auth_token):
    '''Checks to validate our credentials.''' 
    if ((len(account_sid) < 1) or (len(auth_token) < 1)):
        raise Exception("Failed to read twilio auth fron environ.")
    else: 
        print('Account Sid and Auth token are good to go :)')

def get_phone_nums():
    '''Query for user phone numbers'''
    
    q = model.User.query.filter_by(texting_enabled = 'true') 
    
    phone_nums = []

    for num in q:
        phone_nums.append(num.phone_number)
    return phone_nums


def send_reminder(pnum):
    '''Use Twilio to send text message to pnum'''
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages \
                    .create(
                         body="Hi 👋 from MySmartJournal! 🧠 Reminder: Don't forget to take 5 mins out of your day to write ✍️ in your gratitude journal. 🙏",
                         from_= TWILIO_PNUM,
                         to=('+1'+ pnum)
                     )

    print('Sent reminder to', pnum, "SID:", message.sid)


def send_to_all(phone_nums):
    '''Takes a list of phone nums and loops over each one and calls send_reminder'''

    for num in phone_nums:
        send_reminder(num) #num needs to be a string

def send_all_reminders():
    '''Combines grabbing phone numbers from db with sending reminders 
    to each phone number'''
    
    send_to_all(get_phone_nums())
    print('Sent all reminders to users!')


# schedule.every().day.at("17:00").do(send_all_reminders) # UTC time 5pm is 9am PST
schedule.every().minute.do(send_all_reminders)


def run_scheduler():
    '''Run the schedule forever'''
    while True:
        schedule.run_pending()
        time.sleep(1)


def main():
    '''Main func. Calls other functions'''
    app = server.app
    app.debug=True
    model.connect_to_db(app, "journals")
    print("connected to db.")
    check_for_credentials(ACCOUNT_SID, AUTH_TOKEN)
    run_scheduler()


if __name__ == '__main__':
    main()


#To verify people's num on my trial account: twilio.com/user/account/phone-numbers/verified

