import math
import utime


class GY521:
    def __init__(self, sda_pin, scl_pin):
        from imu import MPU6050
        # See instruction: https://github.com/micropython-IMU/micropython-mpu9x50/blob/master/README_MPU9150.md
        # already modified for esp32(sda=21, scl=22)/wemos D1 mini(sda=4, scl=5)
        self.imu = MPU6050(sda=sda_pin, scl=scl_pin)
        self.measured_angles = None
        utime.sleep_ms(500)  # allow stablization of the module

    def get_tilt_angles(self):
        """Export tilt angles in degree
        
        NOTE: beta represents the angle between the longer side of the GY521 module and the level surface
        
        Returns:
            [tuple] -- [the tilt angles in degree for 3 axis]
        """
        # read accel data from axis x, y, z
        ax, ay, az = self.imu.accel.xyz
        # https://www.cnblogs.com/21207-iHome/p/6059260.html
        # pitch angle (angle between x axis and level surface)
        alpha = round(math.atan(ax / math.sqrt(ay**2 + az**2)) * 180 / math.pi, 2)
        # roll angle (angle between y axis and level surface)
        beta = round(math.atan(ay / math.sqrt(ax**2 + az**2)) * 180 / math.pi, 2)
        # head angle (angle between z axis and gravity)
        gamma = round(math.atan(math.sqrt(ax**2 + ay**2) / az) * 180 / math.pi, 2)
        self.measured_angles = alpha, beta, gamma
        return self.measured_angles

    def read_angles(self):
        if not self.measured_angles:
            return self.get_tilt_angles()
        else:
            return self.measured_angles

    def get_smoothed_angles(self, samples=3):
        """Calculate smoothed tilt angles
        
        Keyword Arguments:
            sec {int} -- [duration smoothed in seconds] (default: {3})
        
        Returns:
            [tuple] -- [smoothed tilt angles for 3 axis, unit is degree]
        """
        if isinstance(samples, int):
            a = []
            b = []
            c = []
            for _ in range(samples):
                x, y, z = self.get_tilt_angles()
                a.append(x)
                b.append(y)
                c.append(z)

            def calc_avg(li):
                return round(sum(li) / len(li), 2)
            
            alpha_avg = calc_avg(a)
            beta_avg = calc_avg(b)
            gamma_avg = calc_avg(c)

            return alpha_avg, beta_avg, gamma_avg
