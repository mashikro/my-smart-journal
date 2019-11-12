import server
import model
import os
import twilio
import schedule
import time
import datetime

ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']

if ((len(ACCOUNT_SID) < 1) or (len(AUTH_TOKEN) < 1)):
    raise Exception("failed to read twilio auth fron environ.")

def get_phone_nums():
    '''Query for user phone numbers'''
    
    q = model.User.query.filter_by(texting_enabled = 'true') 
    
    phone_nums = []

    for num in q:
        if len(num.phone_number) >= 10 and num.phone_number != '111 111 1111':
            phone_nums.append(num.phone_number)
    return phone_nums


def send_reminder(pnum):
    '''Use Twilio to send text message to pnum'''
    client = twilio.rest.Client(ACCOUNT_SID, AUTH_TOKEN )

    message = client.messages \
                    .create(
                         body="Hi! Reminder: Dont forget to take 5 mins out of your day to write in MySmartJournal. Link:",
                         from_='+1 917 746 5429',
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
    print('Sent all reminders ro users!')

schedule.every().day.at("17:00").do(send_all_reminders) # UTC time 5pm is 9am PST

    
#     schedule.every().day.at("9:30").do(job)

#     while True:
#         schedule.run_pending()
#         time.sleep(1)





# def job():
#     print("I'm working...")


# schedule.every(5).seconds.do(job)
# schedule.every().hour.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

#To verify people's num on my trial account: twilio.com/user/account/phone-numbers/verified

