import esp
import machine
import ujson
import utime

from battery import Battery
from gy521 import GY521
from microWebCli import MicroWebCli
from unit_convert import Unit
from wifi import WiFi

# disable os debug info
esp.osdebug(None)

# Loading hardware configurations from JSON file
print('--------------------')
print('Loading settings and configurations...')

with open('hardware_config.json', 'r') as f:
    json = f.read()
config = ujson.loads(json)
print('File "hardware_config.json" has been loaded!')

# Loading user settings from JSON file
with open('user_settings.json', 'r') as f:
    json = f.read()
settings = ujson.loads(json)
print('File "user_settings.json" has been loaded!')
print('--------------------')

# Initialize the GY521 module
print('Initializing GY521 module')
gy521 = GY521(config['gy521_pins']['sda'], config['gy521_pins']['scl'])
print('--------------------')

# Initialize the battery power management
print('Initializing power management')
battery = Battery(config['battery_adc_pin'])
print('--------------------')
# Initialize Wifi
print('Initializing WiFi')
wifi = WiFi()
print('--------------------')
print('All done.')
print('--------------------')

# 工作模式（定时deep-sleep）
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('Entering Working Mode...')
    # 1. Start WLAN in STA mode and connect to Fermenter ESP32 AP
    if settings['fermenterAp']['ssid']:
        sta_ip_addr = wifi.sta_connect(settings['fermenterAp']['ssid'], settings['fermenterAp']['pass'])
        if sta_ip_addr:
            print('STA IP: ' + sta_ip_addr)
    print('--------------------')
    # 2. Measure Lipo battery level
    battery_percent = battery.get_lipo_level()
    # 3. Measure tilt angle
    try:
        _, tilt, _ = gy521.get_smoothed_angles()
        # _, tilt, _ = gy521.get_tilt_angles()
    except:
        pass
    else:
        print('Tilt Angle: ' + str(tilt) + 'degree')
        print('Battery: ' + str(battery_percent) + '%')
        print('will go to sleep again in 15s')
        utime.sleep(15)
    # # 4. Calculate Specific Gravity
    #     with open('regression.json', 'r') as f:
    #         json = f.read()
    #     reg = ujson.loads(json)
    #     gravity = reg['a'] * tilt**2 + reg['b'] * tilt + reg['c']
    #     unit = Unit()
    #     if reg['unit'] == 'p':
    #         sg = unit.plato2sg(gravity)
    #     else:
    #         sg = round(gravity, 4)
    #     hydrometer_dict = {
    #         'currentGravity': sg,
    #         'batteryLevel': battery_percent,
    #         'updateIntervalSec': int(settings['deepSleepIntervalMs'] / 1000)
    #     }
    # # 5. Send Specific Gravity data & battery level to Fermenter ESP32 by HTTP
    #     send_data = MicroWebCli.JSONRequest('http://192.168.4.1/gravity', o=hydrometer_dict, connTimeoutSec=10)
    finally:
    # 6. Go deep sleep again, and will wake up after sometime to repeat above.
        print('Sleeping now...')
        machine.deepsleep(settings['deepSleepIntervalMs'])

# 校准模式
elif machine.reset_cause() == machine.SOFT_RESET:
    print('Entering Calibration Mode...')
    print('--------------------')

    # 1. Turn on the on-board green led to indicate calibration mode
    led = machine.Pin(config['led_pin'], machine.Pin.OUT)
    led.on()

    # 2. Start WLAN in AP & STA mode to allow wifi connection
    wifi.ap_start(settings['apSsid'])
    print('AP started')
    # get the AP IP of ESP32 itself, usually it's 192.168.4.1
    ap_ip_addr = wifi.get_ap_ip_addr()
    print('AP IP: ' + ap_ip_addr)
    # get the Station IP of ESP32 in the WLAN which ESP32 connects to
    if settings['wifi']['ssid']:
        sta_ip_addr = wifi.sta_connect(settings['wifi']['ssid'], settings['wifi']['pass'], verify_ap=True)
        if sta_ip_addr:
            print('STA IP: ' + sta_ip_addr)
    print('--------------------')

    # 3. Measure tilt angle every 5s in the background
    import _thread

    def measure_tilt():
        while True:
            try:
                gy521.get_tilt_angles()
            except:
                print('Error occurs when measuring tilt angles')
            utime.sleep(5)

    tilt_th = _thread.start_new_thread(measure_tilt, ())

    # 4. Set up DNS Server
    from microDNSSrv import MicroDNSSrv

    if MicroDNSSrv.Create({'*': '192.168.4.1'}):
        print("DNS service started.")
    else:
        print("Error to start MicroDNSSrv...")
    print('--------------------')

    # 6. Set up HTTP Server
    from httpserver import HttpServer

    web = HttpServer(gy521, wifi, settings)
    print('HTTP server initialized')
    web.start()
    utime.sleep(3)
    if web.is_started():
        print('HTTP service started')
    print('--------------------')

# 首次开机，用户有1分钟时间出发模式选择开关进去校准模式
# 1分钟之后程序会进入DEEP-SLEEP模式，再次唤醒后将开始工作
else:
    # Initialize the mode switch (a double-pole single-throw switch)
    print("Initializing the mode switch")
    mode_switch = machine.Pin(config['mode_switch_pin'], machine.Pin.IN, machine.Pin.PULL_UP)
    print('--------------------')

    print('First time power on...')
    print('If you wish to enter Calibration Mode, pls trigger the mode switch within 1 minute.')
    print('The system will go into Working Mode when 1 minute is out.')

    reboot_tim = machine.Timer(-1)
    # 1分钟后触发Deep-Sleep，再次唤醒后便进入工作模式开始采集数据
    reboot_tim.init(period=60000, mode=machine.Timer.ONE_SHOT, callback=lambda t: machine.deepsleep(settings['deepSleepIntervalMs']))

    irq_counter = 0

    # 通过干簧管开关触发重启，进入校准模式
    def switch_cb(pin):
        global irq_counter
        if irq_counter < 1:
            irq_counter += 1
            machine.disable_irq()
            print('Rebooting to enter Calibration Mode...')
            utime.sleep(3)
            machine.reset()

    mode_switch.irq(handler=switch_cb, trigger=machine.Pin.IRQ_FALLING)
    led = machine.Pin(config['led_pin'], machine.Pin.OUT)

    # Flashing the LED to indicate the system is standing by user's action
    while True:
        led.on()
        utime.sleep_ms(500)
        led.off()
        utime.sleep_ms(500)
