import machine
import ubinascii

from umqtt.robust import MQTTClient


class MQTT:
    def __init__(self, user_settings_dict):
        settings = user_settings_dict.get('mqtt')
        server = settings.get('brokerAddr')
        port = settings.get('brokerPort')
        username = settings.get('username')
        password = settings.get('password')
        client_id = 'hydrometer-' + str(ubinascii.hexlify(machine.unique_id()), 'UTF-8')
        self.enabled = settings.get('enabled')
        self.interval_ms = settings.get('pubIntervalMs')
        self.topic = settings.get('topic')
        if self.topic.endswith('/'):
            self.topic = self.topic[:-1]
        self.client = MQTTClient(client_id, server, port, username, password)
        self.client.connect()

    def is_enabled(self):
        return self.enabled

    def get_update_interval_ms(self):
        return self.interval_ms

    def connect(self):
        try:
            self.client.connect()
        except:
            print('Failed to connect to the MQTT broker.')

    def disconnect(self):
        self.client.disconnect()

    def publish(self, str_msg):
        try:
            self.connect()
        except:
            pass
        else:
            self.client.publish(self.topic, str_msg)
            self.disconnect()