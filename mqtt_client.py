import ubinascii
import machine

from umqtt.robust import MQTTClient


class MQTT:
    def __init__(self, user_settings_dict):
        settings = user_settings_dict.get('mqtt')
        server = settings.get('brokerAddr')
        port = settings.get('brokerPort')
        username = settings.get('username')
        password = settings.get('password')
        client_id = 'hydrometer-' + str(ubinascii.hexlify(machine.unique_id()), 'UTF-8')
        self.topic = settings.get('topic')
        if self.topic.endswith('/'):
            self.topic = self.topic[:-1]
        self.client = MQTTClient(client_id, server, port, username, password)
        self.client.connect()

    def publish(self, str_data):
        self.client.publish(self.topic, str_data)
