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
    
    list_of_inputs = []

    for entry in list_entries:
        if len(entry.q1_text) > 5:
            list_of_inputs.append([entry.q1_text, 
                                    entry.q2_text,
                                    entry.q3_text])

    # print('LIST OF INPUTS:', list_of_inputs)

    return list_of_inputs   
    
def aws_make_request(user_string):
    '''Takes in user data and makes api call to AWS comprehend for 
    sentiment analysis and returns a response object'''
    
    response = client.detect_sentiment(
        Text=user_string, #just text and not textlist
        LanguageCode='en'
    )

    # print(response)

    return response


def apply_sentiment_on_each_data(user_all_data):
    '''Applies AWS sentiment analysis on each piece of user data'''
    response_objects = []

    for single_data in user_all_data:
        response = aws_make_request(single_data[0])
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
    '''Main function uses helper functions to make API request'''
    user_all_entries = get_query(user_id)
    responses = apply_sentiment_on_each_data(user_all_entries)
    organized_reponses = organize_reponse_objects(responses)

    #todo parse through response objects and return 
    #workable response objects for front end

    return organized_reponses


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