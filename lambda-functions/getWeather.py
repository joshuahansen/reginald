import json
from botocore.vendored import requests


def lambda_handler(event, context):
    try:
        city = event['currentIntent']['slots']['City']
        response = requests.get("http://www.bom.gov.au/fwo/IDV60901/IDV60901.95936.json")
            
        if response.status_code == 200:
            data = response.json()
            temp = data['observations']['data'][0]['air_temp']
            res = "The weather in {} is {} degrees".format(city,temp)
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
                "content": "Sorry I could not get the weather at this time please try again later "
            }
        }
    finally:
        return {
            "dialogAction": action
        }     
