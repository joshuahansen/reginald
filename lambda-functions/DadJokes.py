import json
from botocore.vendored import requests


def lambda_handler(event, context):
    try:
        headers = {
            'Accept': 'application/json',
        }
        response = requests.get('https://icanhazdadjoke.com/', headers=headers)
            
        if response.status_code == 200:
            data = response.json()
            res = data["joke"]
            action = {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": res
                    }
                }
        else:
            raise Exception()

    except:
        action = {
            "type": "Close",
            "fulfillmentState": "Failed",
            "message": {
                "contentType": "PlainText",
                "content": "Sorry I could not think of a good joke at this time. Ask me again later"
            }
        }
    finally:
        return {
            "dialogAction": action
        }     
