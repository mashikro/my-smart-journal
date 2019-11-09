from model import User, JournalEntry, db

from datetime import date, timedelta,datetime

def calculate_streak(user_email):
    '''function that computes how many days in a row a user 
    filled out their journal'''

    print('=========== S T A R T ===================')
    
    q = User.query.filter_by(email=user_email).first()
    print('LOOOOOOOOOK', q)
    
    list_entries = q.journal_entries
    print(list_entries)
    
    list_of_dates = []
    #list iterate over
    for entry in list_entries:
        print(entry.date)
        list_of_dates.append(entry.date)

    print(list_of_dates)
    
    d = sorted(list_of_dates)
    # print('SOOOOORTED', d)
    # [datetime.date(2019, 11, 6), datetime.date(2019, 11, 7), datetime.date(2019, 11, 8), datetime.date(2019, 11, 10), datetime.date(2019, 11, 13), datetime.date(2019, 11, 14)]
    
    first_day = d[0]
    current_date = date.today()

    dates_dict = {}

    first_day_str = str(first_day)
    current_date_str = str(current_date)

    start = datetime.strptime(first_day_str, '%Y-%m-%d')

    end = datetime.strptime(current_date_str, '%Y-%m-%d')

    step = datetime.timedelta(days=1)

    while start <= end:
        print(start.date())
        dates_dict[start.date()] = 0
        start += step

    print(dates_dict)





    # # Figure out which dates are missing
    # date_set = set(d[0] + timedelta(x) for x in range((d[-1] - d[0]).days))
    # # print('DATE SET', date_set)
    # #{datetime.date(2019, 11, 6), datetime.date(2019, 11, 10), datetime.date(2019, 11, 9), datetime.date(2019, 11, 12), datetime.date(2019, 11, 7), datetime.date(2019, 11, 13), datetime.date(2019, 11, 11), datetime.date(2019, 11, 8)}
    
    # #list of missing dates
    # missing = sorted(date_set - set(d))
    # # MISSING DATE 2019-11-09
    # # MISSING DATE 2019-11-11
    # # MISSING DATE 2019-11-12

    # for i in missing:
    #     # print('MISSING DATE', i)


    
    print('=========== E N D ===================')



