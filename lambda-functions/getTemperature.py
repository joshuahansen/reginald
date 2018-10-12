import json
from botocore.vendored import requests
import boto3
import uuid


def lambda_handler(event, context):
    try:
        pi_ip = '123.243.247.182:5000'
        full_api_url = "http://{}/temperature".format(pi_ip)
        
        response = requests.get(full_api_url)
            
        if response.status_code == 200:
            data = response.json()
            temp = data['data']
            botResponse = "The temperature near me is {} degrees".format(temp)
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
        botResponse = "Sorry I could not get the temperature, please try again later "
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
