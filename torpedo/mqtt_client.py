import utime

# from umqtt.robust import MQTTClient
from lib.umqtt.simple2 import MQTTClient


class MQTT:
    def __init__(self, user_settings_dict):
        settings = user_settings_dict.get('mqtt')
        server = settings.get('brokerAddr')
        port = settings.get('brokerPort')
        username = settings.get('username')
        password = settings.get('password')
        # client_id = 'hydrometer-' + str(ubinascii.hexlify(machine.unique_id()), 'UTF-8')
        client_id = settings.get('clientId')
        self.enabled = settings.get('enabled')
        self.interval_ms = settings.get('pubIntervalMs')
        the_topic = settings.get('topic')
        if the_topic.endswith('/'):
            the_topic = the_topic[:-1]
        self.topic = str.encode(the_topic) if isinstance(the_topic, str) else the_topic
        self.client = MQTTClient(
            client_id=client_id,
            server=server,
            port=port,
            user=username,
            password=password,
            keepalive=10
        )

    def is_enabled(self):
        return self.enabled

    def manually_enable(self):
        self.enabled = True

    def manually_disable(self):
        self.enabled = False

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
            utime.sleep_ms(1000)
        except:
            print('Failed to publish the data to the MQTT broker.')
        else:
            msg = str.encode(str_msg) if isinstance(str_msg, str) else str_msg
            print(msg)
            self.client.publish(self.topic, msg)
            utime.sleep_ms(1000)
            self.disconnect()
            print('Data have been sent to MQTT broker.')
