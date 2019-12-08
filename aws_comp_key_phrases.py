import model
import json
# import server

def get_query(user_id):
    '''Use user_id to get user's journal entries for analysis'''
   
    q = model.User.query.get(user_id)
    list_entries = q.journal_entries
    
    user_entries_q2 = []

    for entry in list_entries:
        if len(entry.q2_text) > 5:
            user_entries_q2.append(entry.q2_text)

    return user_entries_q2


def count_data(q2_entries): 
    '''Takes in a list of journal entries for q2 and returns a dict with the count of each word'''
    
    lst_of_words = []
    
    for item in q2_entries:
        lst_of_words.extend(item.split())

    # words_to_ignore = {'the', 'a', 'is', 'with', 'for', 'an' 'and', 'or', 'of', 'to', 'on', 'my', 
    #                     'they', 'i', 'more', 'many', 'while', 'lot', 'much', 'be', 'out', 'am'}
    words_to_ignore = {"i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", 
                        "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", 
                        "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", 
                        "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", 
                        "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
                        "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", 
                        "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", 
                        "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", 
                        "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", 
                        "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", 
                        "very", "s", "t", "can", "will", "just", "don", "should", "now"}
    
    new_lst_words = []
    
    for entry in lst_of_words:
        new_lst_words.append(entry.lower())

    words_count = {}
    
    for entry in new_lst_words:
        if not (entry in words_to_ignore):
            count = lst_of_words.count(entry)
            words_count[entry] = count
    
    return words_count


def create_actions_list(user_id):
    '''Uses helper functions to generate data for word cloud'''

    user_data = get_query(user_id)
    
    dict_words_count = count_data(user_data)

    return dict_words_count


if __name__ == '__main__': 
    app = server.app
    app.debug=True
    model.connect_to_db(app)  
    print("connected to db.")


########## Func for future feature (not being used yet) ######################
import boto3

client = boto3.client('comprehend') 

def make_request(user_input):
    '''Makes a request to AWS Comprehend API and returns a response object'''

    response = client.detect_key_phrases(
        Text= user_input, #this needs to be a str
        LanguageCode='en'  # |'es'|'fr'|'de'|'it'|'pt'|'ar'|'hi'|'ja'|'ko'|'zh'|'zh-TW'
    )



