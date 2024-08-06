import json

import paho.mqtt.client as mqtt

class MQTT_Client:
    def __init__(self):

        self.mqttc = mqtt.Client()
        self.mqttc.connect("localhost", 1883, 60)
        self.mqttc.loop_forever()

    def mqtt_pub(self,action: dict):
        self.mqttc.publish(topic="House/action",payload=json.dumps(action))


