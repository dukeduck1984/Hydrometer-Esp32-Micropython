import machine
import ujson
import utime
from gy521 import GY521
from battery import Battery
from deepsleep import DeepSleep
from wifi import WiFi




# get settings from JSON file

with open('config.json', 'r') as f:
    json = f.read()
settings = ujson.loads(json)


gy521 = GY521(settings['gy521_pins']['sda'], settings['gy521_pins']['scl'])
_, tilt_angle, _ = gy521.get_tilt_angles()

power = Battery()

# for ESP8266, NOT ESP32 loboris
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    # Wake from Deep Sleep
    print('Woke from a deep sleep and will get the job done before sleeping again!')

    # Set deepsleep interval to 15mins
    sleep = DeepSleep(settings['deepsleep_interval'], board_type='esp8266')
    # TODO
    # 1. Start WLAN in STA mode and connect to Fermenter ESP32 AP


    # 2. Measure tilt angle and calculate Specific Gravity


    # 3. Send Specific Gravity data to Fermenter ESP32 by HTTP


    # 4. Go deep sleep again, and will wake up after sometime to repeat above.
    # Finish measuring & data tranfer and go back to sleep
    # sleep.go_sleep()
else:
    # Normal start up or soft/hard reset
    # For setting up and calibration
    print('Standing by...')
    print('You can connect to the Setup page via WiFi...')

    # Turn on the onboard blue led to indication standby status
    led = machine.Pin(2, machine.Pin.OUT)
    led(0)

    # Set deepsleep interval to 15mins
    sleep = DeepSleep(15*60, board_type='esp8266')

    # TODO
    # 1. Start WLAN in AP & STA mode to allow wifi connection
    wifi = WiFi()
    wifi.ap_start(settings['ap_ssid'])

    # 2. Select AP ssid and save settings
    # 3. Flip the tube to trigger deepsleep action and will go to working status when reset from deepsleep
    # use a pin irq to trigger sleep.go_sleep()

