import numpy as np

import sensor_io.imu
from sensor_io import imu


def calibrate():
    my_imu = sensor_io.imu.IMU(None)
    m_min = my_imu.scaled_magnetometer
    m_max = my_imu.scaled_magnetometer
    try:
        print(
            "Rotiere die IMU langsam nacheinander um alle drei Achsen und drücke anschließen STRG + C !"
        )
        magnetometer_values = my_imu.scaled_magnetometer
        while True:
            if magnetometer_values is not my_imu.scaled_magnetometer:
                magnetometer_values = my_imu.scaled_magnetometer
                for value in range(0, 3):
                    if magnetometer_values[value] < m_min[value]:
                        m_min[value] = magnetometer_values[value]
                    if magnetometer_values[value] > m_max[value]:
                        m_max[value] = magnetometer_values[value]

    except KeyboardInterrupt:
        print("min: " + str(m_min))
        print("max: " + str(m_max))
        correction = np.subtract(m_max, m_min)
        correction = np.dot(correction, 0.5)
        correction = np.subtract(m_max, correction)
        correction = np.dot(correction, -1)
        print("correction:")
        print(correction)

    finally:
        pass


if __name__ == "__main__":
    calibrate()
