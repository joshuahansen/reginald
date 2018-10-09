#!/usr/bin/env python3
import os
import threading
from flask import Flask, request, render_template, jsonify
from sense_hat import SenseHat


def create_app():
    """Create a falsk application to serve the website"""

    app = Flask(__name__)
    sense = SenseHat()

    def calibrate_temp(sense_temp):
        cpu_temp = get_cpu_temp()
        return round(sense_temp - ((cpu_temp - sense_temp)/1.5), 2)

    def get_cpu_temp():
        res = os.popen("vcgencmd measure_temp").readline()
        cpu_temp = float(res.replace("temp=", "").replace("'C\n", ""))
        return cpu_temp

    @app.route('/temperature', methods=['GET'])
    def temperature():
        """Function used to return temperature of pi"""
        try:
            temp = sense.get_temperature()
            cal_temp = calibrate_temp(temp)

            response = jsonify({"Status": "Successful", "Data": cal_temp})
            response.status_code = 200
        except:
            response = jsonify({"Status": "Failed", "Data": ""})
            response.status_code = 400
        finally:
            return response

    @app.route('/humidity', methods=['GET'])
    def humidity():
        """Function used to return humidity of pi"""
        try:
            hum = sense.get_humidity()

            response = jsonify({"Status": "Successful", "Data": hum})
            response.status_code = 200
        except:
            response = jsonify({"Status": "Failed", "Data": ""})
            response.status_code = 400
        finally:
            return response

    @app.route('/message', methods=['POST'])
    def message():
        '''Function to display message on LED matrix'''
        try:
            message = request.json['message']

            sense.show_message(message)
            
            response = jsonify({"Status": "Successful", "Data": message})
            response.status_code = 200
        except:
            response = jsonify({"Status": "Failed", "Data": ""})
            response.status_code = 400
        finally:
            return response
    
    @app.route('/register', methods=['GET'])
    def register():
        '''Register face for facial recognition'''
        try:
            name = request.args.get('name')
            # Run add face
            response = jsonify({"Status": "Successful", "Data": "{} photos where taken for facial recognition".format(name)})
            response.status_code = 200
        except:
            response = jsonify({"Status": "Failed", "Data": ""})
            response.status_code = 400
        finally:
            return response

    @app.route('/train', methods=['GET'])
    def train():
        '''Train datasets for facial recognition'''
        try:
            # Train facial recognision
            #thread = threading.Thread(target=train, daemon=True)
            #thread.start()
            response = jsonify({"Status": "Successful", "Data": ""})
            response.status_code = 200
        except:
            response = jsonify({"Status": "Failed", "Data": ""})
            response.status_code = 400
        finally:
            return response
    
    @app.route('/recognise', methods=['GET'])
    def recofnise():
        '''Start facial recognition'''
        try:
            # Start facial recognision
            response = jsonify({"Status": "Successful", "Data": ""})
            response.status_code = 200
        except:
            response = jsonify({"Status": "Failed", "Data": ""})
            response.status_code = 400
        finally:
            return response

    return app


if __name__ == '__main__':
    FLASK_APP = create_app()
    FLASK_APP.run(host='0.0.0.0', debug=True)
