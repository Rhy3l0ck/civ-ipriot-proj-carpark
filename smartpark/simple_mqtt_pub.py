import paho.mqtt.client as paho

BROKER, PORT = "localhost", 1883

client = paho.Client()
client.connect(BROKER, PORT)
client.publish("lot/sensor", "Car goes out")

# KEEP ALIVE NOT IN PLACE, PUB DISCONNECTS AFTER PUBLISH
