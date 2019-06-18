import machine
import utime
from gy521 import GY521



gy521 = GY521(sda_pin=4, scl_pin=5)

while True:
    a, b, c = gy521.get_tilt_angles()
    print('alpha:' + str(round(a, 2)))
    print('beta:' + str(round(b, 2)))
    print('gamma:' + str(round(c, 2)))
    print('-------------------')
    utime.sleep_ms(2000)