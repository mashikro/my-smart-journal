

def make_request(user_input):
    '''Makes a request to AWS Comprehend API and returns a response object'''

    response = client.detect_key_phrases(
        Text= user_input, #this needs to be a str
        LanguageCode='en'  # |'es'|'fr'|'de'|'it'|'pt'|'ar'|'hi'|'ja'|'ko'|'zh'|'zh-TW'
    )