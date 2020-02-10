# Project 1
# Publish a sound message when a sound is detected

import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
import time

#GPI SETUP
channel = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
    if GPIO.input (channel):
        print("Sound Detected 1")
        publish.single("cs6301/test", "SOUND", hostname="test.mosquitto.org")
    else:
        print("Sound Detected 2")
        publish.single("cs6301/test", "SOUND", hostname="test.mosquitto.org")

# Here is where we actually detect the sound
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300) # let us know whne pin goes high or low
GPIO.add_event_callback(channel, callback) # assign function to GPIO PIN, Run function on change

#infinite loop
while True:
    time.sleep(1)