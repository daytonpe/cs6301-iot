# MQTT Publish Demo
# Publishes a message to be picked up by the raspberry pi. run this on your own computer.

import paho.mqtt.publish as publish

publish.single("cs6301/test", "TOGGLE LOCK", hostname="test.mosquitto.org")

print("Done")
