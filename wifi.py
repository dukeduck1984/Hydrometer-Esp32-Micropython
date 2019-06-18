import machine
import network
import utime
import ubinascii


class WiFi:
    def __init__(self):
        self.ap_ip_addr = None
        self.sta_ip_addr = None
        self.ap = network.WLAN(network.AP_IF)  # Start AP mode
        self.sta = network.WLAN(network.STA_IF)  # Start STA mode
        utime.sleep_ms(200)
        self.sta.active(True)
        self.machine_id = ubinascii.hexlify(machine.unique_id()).decode().upper()

    def ap_start(self, ssid):
        """
        :param ssid: string; ESSID for the AP
        :return:
        """
        # Initialize the network
        self.ap.active(True)  # activate the AP interface
        self.ap.config(essid=ssid + self.machine_id)  # set ssid
        utime.sleep_ms(200)
        self.ap.config(dhcp_hostname=ssid + '.local')  # set hostname

    def get_ap_ip_addr(self):
        """
        Return IP address in AP mode
        """
        if self.ap.active():
            self.ap_ip_addr = self.ap.ifconfig()[0]  # get AP (ESP32 itself) IP address
            return self.ap_ip_addr
        else:
            return 'WiFi is off, please turn on the AP mode.'

    def get_sta_ip_addr(self):
        """
        Return IP address in STA mode if connected to an AP
        """
        if self.sta.isconnected():
            self.sta_ip_addr = self.sta.ifconfig()[0]
            return self.sta_ip_addr
        else:
            return False

    def scan_wifi_list(self):
        """
        Scan and return a list of available Access Points
        return: list;
        """
        aps = self.sta.scan()
        ap_list = [ap[0] for ap in aps]
        return ap_list

    def sta_connect(self, ap_ssid, ap_pass):
        """
        Connect to an Access Point by its SSID and Password
        return: string; the IP of the STA
        """
        self.sta.sta_connect(ap_ssid, ap_pass)
        utime.sleep_ms(500)
        return self.get_sta_ip_addr()

