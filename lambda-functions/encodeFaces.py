import json
from botocore.vendored import requests
import boto3
import uuid



def lambda_handler(event, context):
    try:
        confirm = event['currentIntent']['slots']['Confirm']
        
        if confirm.lower() == 'yes':
            pi_ip = '123.243.247.182:5000'
            full_api_url = "http://{}/train".format(pi_ip)
            
            response = requests.post(full_api_url, data=payload)
                
            if response.status_code == 200:
                botResponse = "I have completed learning the new faces. Please start the facial recognition"
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
        else:
             botResponse = "For my to recognise you I need to learn what you look like. Please remember to train me later"
                action = {
                    "type": "Close",
                    "fulfillmentState": "Fulfilled",
                    "message": {
                        "contentType": "SSML",
                        "content": "<speak>{}</speak>".format(botResponse)
                        }
                    }

    except:
        botResponse = "Sorry I could not complete the training. Please try again"
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
