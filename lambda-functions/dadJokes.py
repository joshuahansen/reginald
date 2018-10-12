import json
from botocore.vendored import requests
import boto3
import uuid


def lambda_handler(event, context):
    try:
        headers = {
            'Accept': 'application/json',
        }
        response = requests.get('https://icanhazdadjoke.com/', headers=headers)
            
        if response.status_code == 200:
            data = response.json()
            botResponse = data["joke"]
            action = {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "SSML",
                    "content": "<speak>{}</speak>".format(botResponse)
                    }
                }
        else:
            raise Exception()

    except:
        botResponse = "Sorry I could not think of a good joke at this time. Ask me again later"
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
