# MQTT Client demo
# Continuously monitor two different MQTT topics for data,
# check if the received data matches two predefined 'commands'

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import os

# sensor pin define
buzzer = 14
touch = 26
relay_in1 = 13
relay_in2 = 19
touchstatus = False

# GPIO port init
def init():
    # Create an MQTT client and attach our routines to it.
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.touchstatus = touchstatus

    client.connect_async("test.mosquitto.org", 1883, 60)

    # Process network traffic and dispatch callbacks. This will also handle
    # reconnecting. Check the documentation at
    # https://github.com/eclipse/paho.mqtt.python
    # for information ons how to use other loop*() functions
    client.loop_start()
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer,GPIO.OUT)
    GPIO.setup(relay_in1,GPIO.OUT)
    GPIO.setup(relay_in2,GPIO.OUT)
    GPIO.setup(touch,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    pass

# turn on buzzer
def buzzer_on():
    GPIO.output(buzzer,GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(buzzer,GPIO.HIGH)
    time.sleep(0.2)
    pass

# turn off buzzer
def buzzer_off():
    GPIO.output(buzzer,GPIO.HIGH)
    pass

# turn on relay
def relay_on():
    # open relay channal1 ana channal2
    GPIO.output(relay_in1,GPIO.LOW)
    GPIO.output(relay_in2,GPIO.LOW)

# turn off relay
def relay_off():
    GPIO.output(relay_in1,GPIO.HIGH)
    GPIO.output(relay_in2,GPIO.HIGH)


# read digital touch sensor
def read_touchsensor():
    global touchstatus
    if (GPIO.input(touch)==True):
        touchstatus = not touchstatus
        if touchstatus:
            print("Turn on relay")
            buzzer_on()
            relay_on()
        else:
            print("Turn off relay")
            buzzer_on()
            relay_off()
    pass

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("cs6301/test")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global touchstatus
    print("\n"+msg.topic+" "+str(msg.payload))

    if msg.payload == "TOGGLE LOCK":
        print("Toggling lock.")
        touchstatus = not touchstatus

        if touchstatus:
            print("Turn on relay -- DOOR LOCKED")
            buzzer_on()
            relay_on()
        else:
            print("Turn off relay -- DOOR UNLOCKED")
            buzzer_on()
            relay_off()


# main loop
def main():

    print("....System initializing...")
    init()
    buzzer_off()
    relay_off()
    print("....Ok")
    print("....Please touch")
    print("\n")



    while True:
        read_touchsensor()


if __name__ == '__main__':
    try:
        main()


        pass
    except KeyboardInterrupt:
        pass
    pass

GPIO.cleanup()

