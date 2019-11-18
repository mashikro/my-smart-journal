import boto3
import model
import server
import json

client = boto3.client('comprehend')

def get_query(user_id):
    '''Use user_id to get user's journal entries for analysis'''
    q = model.User.query.get(user_id)
    list_entries = q.journal_entries
    # print('LIST OF ENTRIES:', list_entries)
    
    user_entries_q1 = []
    dates_for_entries = []

    for entry in list_entries:
        if len(entry.q1_text) > 5:
            user_entries_q1.append(entry.q1_text)
            dates_for_entries.append(entry.date)

    return (user_entries_q1, dates_for_entries)  #first item goes into sentiment analysis
    
def aws_make_request(user_string):
    '''Takes in user data and makes api call to AWS comprehend for 
    sentiment analysis and returns a response object'''
    
    response = client.detect_sentiment(
        Text=user_string, #just text and not textlist
        LanguageCode='en'
    )

    return response


def apply_sentiment_on_each_data(user_journal_entries):
    '''Applies AWS sentiment analysis on each piece of user data'''
    response_objects = []

    for single_data in user_journal_entries:
        print('SINGLE DATA', single_data)
        response = aws_make_request(single_data)
        print('THIS IS EACH RESPONSE:', response)
        response_objects.append(response)

    return response_objects


def organize_reponse_objects(responses):
    '''Takes in a list of response objects and returns (relevant data)
    # Response object: 

    # dict1 = {
    # 'Sentiment': 'POSITIVE', 
    # 'SentimentScore': {'Positive': 0.5676356554031372, 
    #                     'Negative': 0.0007096294430084527, 
    #                     'Neutral': 0.431611567735672, 
    #                     'Mixed': 4.310160147724673e-05}, 
    # 'ResponseMetadata': {'RequestId': '03abbb39-be95-4b40-ada3-87f84203f968', 
    #                     'HTTPStatusCode': 200, 
    #                     'HTTPHeaders': {'x-amzn-requestid': '03abbb39-be95-4b40-ada3-87f84203f968', 'content-type': 'application/x-amz-json-1.1', 'content-length': '162', 'date': 'Fri, 15 Nov 2019 23:31:08 GMT'}, 
    # 'RetryAttempts': 0}
    # }
    # >>> dict1['Sentiment']
    # 'POSITIVE' 
    # >>> dict1['SentimentScore']
    # {
    # 'Positive': 0.5676356554031372, 
    # 'Negative': 0.0007096294430084527, 
    # 'Neutral': 0.431611567735672, 
    # 'Mixed': 4.310160147724673e-05
    } '''

    sentiment = [] #1 item list
    sentiment_score = [] #2 list nested in 1 list 

    for response in responses:
        sentiment.append(response['Sentiment'])
        sentiment_score.append((response['SentimentScore'].keys(), 
                                response['SentimentScore'].values()))  
    
    return (sentiment, sentiment_score) #tuple with 2 lists 


def main(user_id):
    '''Main function uses helper functions to make API request
    ((['POSITIVE', 'POSITIVE', 'NEUTRAL', 'NEUTRAL'], 
    [(dict_keys(['Positive', 'Negative', 'Neutral', 'Mixed']), 
    dict_values([0.5676356554031372, 0.0007096294430084527, 0.431611567735672, 4.310160147724673e-05])), 
    (dict_keys(['Positive', 'Negative', 'Neutral', 'Mixed']), 
    dict_values([0.7936040759086609, 0.004303410183638334, 0.20203734934329987, 5.515471275430173e-05])), 
    (dict_keys(['Positive', 'Negative', 'Neutral', 'Mixed']), 
    dict_values([0.3683869540691376, 0.006351249758154154, 0.625140905380249, 0.00012093513942090794])), 
    (dict_keys(['Positive', 'Negative', 'Neutral', 'Mixed']), 
    dict_values([0.00895390473306179, 0.027104999870061874, 0.9639381170272827, 3.0295936994662043e-06]))]), 
    [datetime.date(2019, 11, 11), datetime.date(2019, 11, 13), datetime.date(2019, 11, 15), datetime.date(2019, 11, 15)])
    '''
    
    # returns two item tuple (entries list and dates list)
    journal_entries_dates = get_query(user_id)
    #first item in 'journal_entries_dates' which is a list of all queries
    responses = apply_sentiment_on_each_data(journal_entries_dates[0]) 
    #returns two item tuple
    organized_reponses = organize_reponse_objects(responses)

    #returning 'organized_response' which is a tuple w 2 items and list of dates
    return (organized_reponses, journal_entries_dates[1]) 


if __name__ == '__main__': 
    app = server.app
    app.debug=True
    model.connect_to_db(app)  
    print("connected to db.")
   
    
#wrap function
#view - call this function 
#get data back
#use ajax to get json dict 
#format using charts js and display to user