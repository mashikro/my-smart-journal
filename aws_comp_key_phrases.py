import boto3
import model
import json
# import server

client = boto3.client('comprehend') 


def get_query(user_id):
    '''Use user_id to get user's journal entries for analysis'''
   
    q = model.User.query.get(user_id)
    list_entries = q.journal_entries
    
    user_entries_q2 = []
    dates_for_entries = []

    for entry in list_entries:
        if len(entry.q2_text) > 5:
            user_entries_q2.append(entry.q2_text)
            dates_for_entries.append(entry.date)

    print('User entries to Q22222', user_entries_q2)
    return (user_entries_q2, dates_for_entries)

#this function is not being used yet
def make_request(user_input):
    '''Makes a request to AWS Comprehend API and returns a response object'''

    response = client.detect_key_phrases(
        Text= user_input, #this needs to be a str
        LanguageCode='en'  # |'es'|'fr'|'de'|'it'|'pt'|'ar'|'hi'|'ja'|'ko'|'zh'|'zh-TW'
    )

# def detect_key_phrases(user_data_as_list):

#     response_objects = []

#     for single_data in user_data_as_list:
#         response = make_request(single_data)
#         response_objects.append(response)

#     return response_objects

def count_data(q2_entries): #input is a list
    '''Returns a dict with the count of each word'''
    
    lst_of_words = []
    
    for item in q2_entries:
        lst_of_words.extend(item.split())

    words_count = {}
    words_to_ignore = {'the', 'a', 'is', 'with', 'for', 'an' 'and', 'or', 'of', 'to', 'on', 'my', 'they', 'i'}
    
    for entry in lst_of_words:
        # entry = entry.lower()
        if not (entry in words_to_ignore):
            count = lst_of_words.count(entry)
            words_count[entry] = count
    
    return words_count


def create_actions_list(user_id):
    '''Uses helper functions to generate data for word cloud'''

    user_data = get_query(user_id)
    
    dict_words_count = count_data(user_data[0])

    print('USER_DATA[0]', user_data[0])

    print('LOOOOOOOOOK HERE MASHA', make_request(set(user_data[0])))

    return (dict_words_count, user_data[1])


if __name__ == '__main__': 
    app = server.app
    app.debug=True
    model.connect_to_db(app)  
    print("connected to db.")


