# USAGE
# Specify the name of the person
#     python3 faceDetection.py -n Josh

## Acknowledgement
## This code is adapted from:
## https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
'''
Face detection registration to take new images for facial recognition
Requires user to have 10 normal pictures and 10 smiling pictures
'''
import numpy as np
import cv2
import os
from sense_hat import SenseHat

sense = SenseHat()

g = (0,255,0)
c = (0,0,0)

# display a box on the LED matrix
def faceLED():
    '''
    Display a green box on led matrix
    '''
    face = [
        g, g, g, g, g, g, g, g,
        g, c, c, c, c, c, c, g,
        g, c, c, c, c, c, c, g,
        g, c, c, c, c, c, c, g,
        g, c, c, c, c, c, c, g,
        g, c, c, c, c, c, c, g,
        g, c, c, c, c, c, c, g,
        g, g, g, g, g, g, g, g
    ]
    sense.set_pixels(face)


def register(name):
    # use name as folder name
    folder = './dataset/{}'.format(name)

    # Create a new folder for the new name
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Load face, eyes and smile cascades
    faceCascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)
    cap.set(3,640) # set Width
    cap.set(4,480) # set Height

    img_counter = 0

    while img_counter < 10:
        ret, img = cap.read()

        if not ret:
            print("Camera did not connect")
            break
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,     
            minSize=(20, 20)
            )

        # if a face is detected display box on sense hat
        if len(faces) > 0:
            faceLED()
        else:
            sense.clear((0,0,0))

        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]

            img_name = "{}/{:04}.jpg".format(folder,img_counter)
            cv2.imwrite(img_name, img[y:y+h,x:x+w])
            print("{} face written!".format(img_name))
            img_counter += 1
            

    cap.release()
    cv2.destroyAllWindows()
