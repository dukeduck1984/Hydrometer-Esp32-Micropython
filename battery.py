import machine
import utime


class Battery:
    def __init__(self, adc_pin):
        self.adc = machine.ADC(machine.Pin(adc_pin))
        self.lipo_percent = None
    
    def measure_lipo_level(self):
        """
        wiring diagram: https://learn.adafruit.com/using-ifttt-with-adafruit-io/wiring#battery-tracking
        measure lipo battery level by ADC
        lipo battery level 4.2V - 3.14V
        the 1M & 300K voltage divider bring the battery voltage down to 969mV max ~ 725mV min

        Returns:
            [int] -- [lipo level percentage, eg. 85, unit is %]
        """
        mv_max = 969
        mv_min = 725
        # ADC read value should be 3306 when battery is full at 4.2v
        val_max = int(mv_max / 1200 * 4095)
        # ADC read value should be 2474 when battery is empty at 3.14v
        val_min = int(mv_min / 1200 * 4095)
        # # read value for 5 times, returned value 0-4095 equals 0-1200mv
        # adc_values = [self.adc.read() for _ in range(5)]
        # adc_values.sort()
        # adc_values = adc_values[1:4]
        # adc_value = sum(adc_values) / len(adc_values)
        adc_value = self.adc.read()
        self.lipo_percent = int(round((adc_value - val_min) / (val_max - val_min) * 100, 0))
        if self.lipo_percent > 100:
            self.lipo_percent = 100
        if self.lipo_percent < 0:
            self.lipo_percent = 0
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
