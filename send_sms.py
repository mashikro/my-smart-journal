from twilio.rest import Client
import schedule
import time
from model import User, JournalEntry, db
import os

ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
print(ACCOUNT_SID)
print(AUTH_TOKEN)

def get_phone_nums():
    '''Query for user data'''
    
    q = User.query.filter_by(texting_enabled = 'true') 
    
    phone_nums = []

    for num in q:
        phone_nums.append(num.phone_number)

    return phone_nums


def send_reminder(number):
    client = Client(ACCOUNT_SID, AUTH_TOKEN )

    message = client.messages \
                    .create(
                         body="Hi! Reminder: Dont forget to take 5 mins out of your day to write in MySmartJournal. Link:",
                         from_='+1 917 746 5429',
                         to=number
                     )

    print(message.sid)


def send_to_all(phone_nums):
    '''Takes a list of phone nums and loops over each one and calls send_reminder'''

    for num in phone_nums:
        send_reminder(num) #num needs to be a string

def main():
    phone_num_list = get_phone_nums()
    send_to_all(phone_num_list)
    
    schedule.every().day.at("9:30").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)





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
