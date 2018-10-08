import json
from botocore.vendored import requests


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
                "content": "SorRy I could not get the weather at this time please try again later "
            }
        }
    finally:
        return {
            "dialogAction": action
        }   
