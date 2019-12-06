from model import User, JournalEntry, db

import datetime 

def get_entry_dates(user_id):
    '''Query for user data using user_id from session'''
    
    q = User.query.get(user_id)
    
    list_entries = q.journal_entries
    
    list_of_dates = []

    for entry in list_entries:
        list_of_dates.append(entry.date)

    return list_of_dates


def generate_date_range(start_date):
    '''generate a range of date objects'''

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
    '''compute how many days in a row a user 
    filled out their journal'''
    
    start_date = sorted(all_dates)[0]
    dates_range = generate_date_range(start_date)

    streaks = []
    streak_count = 0

    for date in dates_range:
        if date in all_dates:
            streak_count += 1
            streaks.append(streak_count)
        else:
            streak_count = 0
            streaks.append(streak_count)

    return (dates_range, streaks)


def main(user_id):
    '''Main function'''
    
    all_dates = get_entry_dates(user_id)

    if len(all_dates) > 0:
        dates_streaks = calculate_streak(all_dates)
        return dates_streaks

    return ([], [])
