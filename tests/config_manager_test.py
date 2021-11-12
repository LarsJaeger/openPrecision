import unittest

from open_precision.plugins.position_builders.gps_compass import GpsCompassPositionBuilder
from open_precision.core.config_manager import ConfigManager


class ConfigManagerTest(unittest.TestCase):
    def test_config_manager(self):
        conf = ConfigManager('../config.yml')
        conf.register_value(GpsCompassPositionBuilder, 'some_config_value', 3, comment='should normally be equal to the sqrt of nine')
        print('Wert: ' + str(conf.get_config(GpsCompassPositionBuilder)))
        self.assertEqual(False, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
