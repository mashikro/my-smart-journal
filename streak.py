from model import User, JournalEntry, db

import datetime 


def get_entry_dates(user_id):
    '''Query for user data'''

    print('=========== S T A R T ===================')
    
    q = User.query.get(user_id)
    
    list_entries = q.journal_entries
    
    list_of_dates = []

    for entry in list_entries:
        list_of_dates.append(entry.date)

    return list_of_dates

def generate_date_range(start_date):
    '''generates a range of date objects'''

    current_date = datetime.date.today()
    dates_range = [datetime.date.fromordinal(i) for i in range(start_date.toordinal(), 
                    current_date.toordinal() +1)]
    
    return dates_range

#input: list of datetime.date objects
#return: 2 list in a tuple (datetime.date objects and ints)
#first date - first entry
#last date - today
#no gaps
def calculate_streak(all_dates):
    '''function that computes how many days in a row a user 
    filled out their journal'''

    start_date = sorted(all_dates)[0]
    dates_range = generate_date_range(start_date)

    print(dates_range)


def main(user_id):
    all_dates = get_entry_dates(user_id)
    result = calculate_streak(all_dates)

    return result

#7th and 9th missing
test_dates = [datetime.date(2019, 11, 6),  datetime.date(2019, 11, 8), datetime.date(2019, 11, 10), datetime.date(2019, 11, 13), datetime.date(2019, 11, 14)]

