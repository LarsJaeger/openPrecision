from __future__ import print_function

import sys
import time

import ruamel.yaml

from open_precision.plugins.sensor_wrappers import sparkfun_icm20948_imu_adapter


class Main:
    imu = None
    lcd = None
    position = None
    keyboard = None

    def init_hardware(self):
        # init LCD
        # self.lcd = lcd.LCD()

        # init IMU
        # self.imu = sparkfun_icm20948_imu_adapter.IMU(self.config)

        # init KeyBoard
        # self.keyboard = FoilKeyboard([["1", "2", "3", "A"],
        #                              ["4", "5", "6", "B"],
        #                              ["7", "8", "9", "C"],
        #                              ["*", "0", "#", "D"]], [[21, 20, 16, 26], [19, 13, 6, 5]])
        pass

    def run(self):
        try:
            while True:
                print(self.imu.scaled_magnetometer)
                time.sleep(0.2)
        except KeyboardInterrupt:
            # here you put any code you want to run before the program
            # exits when you press CTRL+C
            pass  # print value of counter
        except:
            # this catches ALL other exceptions including errors.
            # You won't get any error messages for debugging
            # so only use it once your code is working
            pass
        finally:
            self.keyboard.disable()

    def __init__(self):
        self.init_hardware()
        self.run()

    def close(self):
        self.keyboard.close()


if __name__ == '__main__':
    try:
        Main()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)
