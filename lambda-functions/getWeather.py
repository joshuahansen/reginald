import json
from botocore.vendored import requests
import boto3
import uuid



def lambda_handler(event, context):
    try:
        city = event['currentIntent']['slots']['City']
        user_api = 'df38ba0c99310b2d5670d0bf46f4ac69'
        unit = 'metric'
        api = 'http://api.openweathermap.org/data/2.5/weather'
        country_code = 'au'

        full_api_url = "{}?q={},{}&mode=json&units={}&APPID={}".format(api,city,country_code,unit,user_api)
        
        response = requests.get(full_api_url)
            
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            botResponse = "The weather in {} is {} degrees".format(city,temp)
            action = {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "SSML",
                    "content": "<speak>{}</speak>".format(botResponse)
                    }
                }
            }
        else:
            raise Exception()

    except:
        botResponse = "Sorry I could not get the weather at this time please try again later"
        action = {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "SSML",
                "content": "<speak>{}</speak>".format(botResponse)
            }
        }
    finally:
        try:
            intent = event['currentIntent']['name']
            transcript = event['inputTranscript']
            dbid = str(uuid.uuid4())
            dynamodb = boto3.resource("dynamodb")
            table = dynamodb.Table('LexHistory')
            table.put_item(
                Item={
                    'UUID': dbid,
                    'intent': intent,
                    'transcript': transcript,
                    'response': botResponse
                    }
                )
            
        except:
            action = {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": "Error Saving to Database uuid: {} intent: {} transcript: {} response: {}".format(dbid, intent, transcript, botResponse)
            }
        }
        return {
            "dialogAction": action
        }   
