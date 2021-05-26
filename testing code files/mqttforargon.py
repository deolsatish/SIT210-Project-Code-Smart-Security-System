import paho.mqtt.client as mqtt
import time
def MQTT_ARGON():
    client = mqtt.Client("deol_mqtt")
    client.connect("test.mosquitto.org",1883) #default port 1883
    client.publish("argonconnect", "No_Intruder")
    print("Just published " + "No_Intruder" +"smartsecurityproject")
while True:
    MQTT_ARGON()
    time.sleep(3);