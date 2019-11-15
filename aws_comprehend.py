import boto3
import model
import server
import json

client = boto3.client('comprehend')

def get_query(user_id=1):
    '''Use user_id to get user's journal entries for analysis'''
    q = model.User.query.get(user_id)
    list_entries = q.journal_entries
    # print('LIST OF ENTRIES:', list_entries)
    
    list_of_inputs = []

    for entry in list_entries:
        list_of_inputs.append(entry.q1_text)

    # print('LIST OF INPUTS:', list_of_inputs)

    return list_of_inputs   
    
def aws_make_request(user_string):
    '''Takes in user data and makes api call to AWS comprehend for 
    sentiment analysis and returns a response object'''
    
    response = client.detect_sentiment(
        Text='masha is so stupid and ugly. jk!', #just text and not textlist
        LanguageCode='en'
    )

    print(response)

    return response


# def apply_sentiment_on_each_data(user_all_data):
#     '''Applies AWS sentiment analysis on each piece of user data'''
#     response_objects = []

#     for single_data in user_all_data:
#         response = amazon_comprehend(single_data)


#     return response_objects


# def organize_reponse_objects(responses):
#     '''Takes in a list of response objects and returns (relevant data)'''

#     pass


# def main(user_id):
#     user_all_entries = get_query(user_id)
#     apply_sentiment_on_each_data(user_all_entries)




if __name__ == '__main__': 
    app = server.app
    app.debug=True
    model.connect_to_db(app) #reading top to bottom 
    print("connected to db.")
    # get_query(user_id)
   
    
#wrap function
#view - call this function 
#get data back
#use ajax to get json dict 
#format using charts js and display to user