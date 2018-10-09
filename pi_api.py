#!/usr/bin/env python3
import os
import threading
from flask import Flask, request, render_template, jsonify
from sense_hat import SenseHat
from imutils.video import VideoStream
import face_recognition
import imutils
import pickle
import time
import cv2
import requests


def create_app():
    """Create a falsk application to serve the website"""

    app = Flask(__name__)
    sense = SenseHat()

    run_recognize = False
    thread_lock = threading.Lock()

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
    
    @app.route('/recognize', methods=['GET'])
    def recognize():
        '''Start facial recognition'''
        try:
            # Start facial recognision
            thread = threading.Thread(target=facial_recognition, daemon=True)
            thread.start()
            response = jsonify({"Status": "Successful", "Data": ""})
            response.status_code = 200
        except:
            response = jsonify({"Status": "Failed", "Data": ""})
            response.status_code = 400
        finally:
            return response

    @app.route('/stop-recognize', methods=['GET'])
    def stop_recognize():
        '''Stop facial recognition'''
        try:
            global run_recognize
            thread_lock.acquire()
            run_recognize = False
            thread_lock.release()

            response = jsonify({"Status": "Successful", "Data": ""})
            response.status_code = 200
        except:
            response = jsonify({"Status": "Failed", "Data": ""})
            response.status_code = 400
        finally:
            return response

    def facial_recognition():
        '''Run facial recognition '''
        print("[INFO] loading encodings...")
        data = pickle.loads(open('encodings.pickle', "rb").read())

        print("[INFO] starting video stream...")
        vs = VideoStream(src=0).start()
        writer = None
        time.sleep(1.0)

        run = True
        # loop over frames from the video file stream
        while run:
            frame = vs.read()

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb = imutils.resize(frame, width=240)
            r = frame.shape[1] / float(rgb.shape[1])

            boxes = face_recognition.face_locations(rgb, model='hog')
            encodings = face_recognition.face_encodings(rgb, boxes)
            names = []

            # loop over the facial embeddings
            for encoding in encodings:
                matches = face_recognition.compare_faces(data["encodings"], 
                        encoding)
                name = "Unknown"

                if True in matches:
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                name = max(counts, key=counts.get)

                # update the list of names
                names.append(name)
            
            # loop over the recognized faces
            for ((top, right, bottom, left), name) in zip(boxes, names):
                top = int(top * r)
                right = int(right * r)
                bottom = int(bottom * r)
                left = int(left * r)

                print('Person found: {}'.format(name))
                
                # print to sense hat LED matrix
                sense.show_message(name)
                # Set a flag to sleep the cam for fixed time
                time.sleep(1.5)

            # check if facial recognition as been stopped
            global run_recognize
            thread_lock.aquire()
            if not run_recognize:
                run = False
            thread_lock.release()
        
        # do a bit of cleanup
        cv2.destroyAllWindows()
        vs.stop()
        print("Facial Recognition Stopped")
                
    return app


if __name__ == '__main__':
    FLASK_APP = create_app()
    FLASK_APP.run(host='0.0.0.0', debug=True)
