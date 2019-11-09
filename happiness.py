from model import User, JournalEntry, db

def get_happiness_data(user_id):
    '''Query for user's happiness data'''

    print('=========== S T A R T ===================')
    
    q = User.query.get(user_id)

    list_entries = q.journal_entries
    # print(list_entries)
    
    list_of_dates = [] 
    list_of_happ_scores = []
    #list iterate over
    for entry in list_entries:
        print(entry.date, entry.happ_score)
        list_of_dates.append(entry.date)
        list_of_happ_scores.append(entry.happ_score)

    # print(list_of_dates_happ_score)

    print('=========== E N D ===================')

    return (list_of_dates, list_of_happ_scores)