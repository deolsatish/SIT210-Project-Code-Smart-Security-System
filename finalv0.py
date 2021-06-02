import RPi.GPIO as GPIO
import time
#import smtplib
import cv2
import numpy as np
import os
from smbus import SMBus
import paho.mqtt.client as mqtt
import threading
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

pirpin=16

facialrec=False;

        
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pirpin, GPIO.IN)         #Read output from PIR motion sensor

gmail_user = 'baros.nebula@gmail.com'
gmail_password = '*********'

def SMTP_SEND_EMAIL():
    subject = "Super Important Message, Intruder Alert"
    body = "There is a suspicious character in front of the door at the time when the message was sent"
    sender_email = "baros.nebula@gmail.com"
    receiver_email = "deol.satish.2001.3@gmail.com"
    password = '*******'

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = "/home/pi/Desktop/Intruder.jpg"  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)
    
    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
        print("INtruder Alert Email SENT")
        
        
addr=0x8
bus=SMBus(1) #/dev/ic2-1
#bus.write_byte(addr,0x0)
#bus.write_byte(addr,0x1)
def LIGHT_ON(): # swicthing the light on using arduino
    bus.write_byte(addr,0x1)
def LIGHT_OFF():
    bus.write_byte(addr,0x0)
    
def MQTT_ARGON(intruderalert):
    client = mqtt.Client("deol_mqtt")
    client.connect("test.mosquitto.org",1883) #default port 1883
    client.publish("argonconnect", intruderalert)
    print("Just published " + intruderalert +" argonconnect")
    
print(dir (cv2.face))
recognizer = cv2.face.createLBPHFaceRecognizer()
recognizer.load('/home/pi/Desktop/haarcascade_frontalface_default.xml')
cascadePath = "/home/pi/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
items = ['Deol', 'Intruder'] 

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

def FACE_RECOGNITION():
    while True:

        ret, img =cam.read()
        img = cv2.flip(img, -1) # Flip vertically

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
           )

        for(x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])


            if (confidence < 100 and confidence >37):
                    id = 0
                    confidence = "  {0}%".format(round(100 - confidence)) 
            elif(confidence<37):
                    id = 1
                    confidence = "  {0}%".format(round(100 - confidence))
            else:
                    id = 1
                    confidence = "  {0}%".format(round(100 - confidence))
        
            cv2.putText(img, str(items[id]), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
            
            
            if(id==0):
                MQTT_ARGON("No_Intruder")
                print()
            #bus_.write_byte(addr, 0x1) # switch the house led on as the owner is home
                
            elif(id==1):
                x1=threading.Thread(target=MQTT_ARGON, args=("Intruder",))
                x2=threading.Thread(target=SMTP_SEND_EMAIL)
                x1.start()
                x2.start()
                x1.join()
                x2.join()
                #MQTT_ARGON("Intruder")
                #SMTP_SEND_EMAIL()
            #EMAIL()# the intruder is detected send the mail to the user
                cv2.imwrite('/home/pi/Desktop/Intruder.jpg', img) 
    
        cv2.imshow('camera',img) 

        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            LIGHT_OFF()
            cam.release()
            cv2.destroyAllWindows()
            break
        





def LightOn_OFF():
        LIGHT_ON()# this turns on the led of the house on for some period of time, this enables camera to work
        time.sleep(20)
        LIGHT_OFF()
        
def MOTION_DETCTION(pirPIN):
    print("Motion Detected")
    x1=threading.Thread(target=FACE_RECOGNITION)
    x2=threading.Thread(target=LightOn_OFF)
    x1.start()
    x2.start()
    x1.join()
    x2.join()
    
    
def PIR_SENSOR():
    GPIO.add_event_detect(pirpin,GPIO.RISING,callback=MOTION_DETCTION)
    while 1:
        time.sleep(0.5)
        
PIR_SESNOR();
        
        

# Do a bit of cleanup
if KeyboardInterrupt:
    print("Exit")
    
    GPIO.cleanup()
    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()



