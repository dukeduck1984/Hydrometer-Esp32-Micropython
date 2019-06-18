import machine



class DeepSleep:
    def __init__(self, sleep_sec, board_type='esp8266'):
        """[Initialize deepsleep function]
        Intended for ESP8266 (eg. Wemos D1 mini) or ESP32 (loboris firmware only)
        **NOTE**: for esp8266 board, GPIO pin 16 must be connected to RST (reset) pin in order to use deepsleep
        
        Arguments:
            sleep_sec {int} -- [wake up the machine from deepsleep after how long time (in seconds)]
        
        Keyword Arguments:
            board {str} -- [select board type, either 'esp8266' or 'esp32'] (default: {'esp8266'})
        """
        if isinstance(sleep_sec, int):
            self.sleep_sec = sleep_sec
        else:
            print('sleep_sec arg must be "int" type.')
            return
        
        if board_type == 'esp8266' or board_type == 'esp32':
            self.board_type = board_type
        else:
            print('board_type arg must be either "esp8266" or "esp32".')
    

    def go_sleep(self):
        if self.board_type == 'esp8266':
            # configure RTC.ALARM0 to be able to wake the device
            rtc = machine.RTC()
            rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
            # set RTC.ALARM0 to fire after set seconds (waking the device)
            rtc.alarm(machine.RTC.ALARM0, self.sleep_sec*1000)
            # put the device to sleep
            machine.deepsleep()
        elif self.board_type == 'esp32':
            machine.deepsleep(self.sleep_sec*1000)

