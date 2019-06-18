#
#  For Wemos D1 Mini (ESP8266)
#


import machine
import utime


class Battery:
    """For Wemos D1 mini ONLY
    
    NOTE: There is only 1 ADC pin on Wemos D1 mini which is the A0 pin
    """

    def __init__(self):
        self.adc = machine.ADC(0)
        self.lipo_percent = None

    
    def measure_lipo_level(self):
        """
        wiring diagram: https://learn.adafruit.com/using-ifttt-with-adafruit-io/wiring#battery-tracking
        measure lipo battery level by ADC
        lipo battery level 4.2V - 3.14V
        the 1M & 220K voltage divider bring the battery voltage down to 758mV max ~ 567mV min
        the ADC read will be performed for 5 times and get rid of the max & min, then get the avg value

        Returns:
            [int] -- [lipo level percentage, eg. 85, unit is %]
        """
        mv_max = 758
        mv_min = 567
        # ADC read value should be 776 when battery is full at 4.2v
        val_max = mv_max / 1000 * 1024
        # ADC read value should be 581 when battery is empty at 3.14v
        val_min = mv_min / 1000 * 1024
        # read value for 5 times, returned value 0-1024 equals 0-1000mv
        adc_values = [self.adc.read() for _ in range(5)]
        adc_values.sort()
        adc_values = adc_values[1:4]
        adc_value = sum(adc_values) / len(adc_values)
        
        self.lipo_percent = int(round((adc_value - val_min) / (val_max - val_min) * 100, 0))

        return self.lipo_percent


def get_lipo_level(self):
    """Return last measured lipo level
    
    Returns:
        [int] -- [lipo level percentage, eg. 85, unit is %]
    """

    if self.lipo_percent:
        return self.lipo_percent
    else:
        return self.measure_lipo_level()

