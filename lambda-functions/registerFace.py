import json
from botocore.vendored import requests
import boto3
import uuid



def lambda_handler(event, context):
    try:
        name = event['currentIntent']['slots']['Name']
            
        pi_ip = '123.243.247.182:5000'
        full_api_url = "http://{}/register?name={}".format(pi_ip, name)
        
        response = requests.post(full_api_url, data=payload)
            
        if response.status_code == 200:
            botResponse = "I have taken some images of {}. Let me know if you want want me to learn what you look like".format(name)
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
        botResponse = "I can't seem to get any images of you please try again later"
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
