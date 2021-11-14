import unittest

from open_precision.plugins.position_builders.gps_compass import GpsCompassPositionBuilder
from open_precision.core.config_manager import ConfigManager


class ConfigManagerTest(unittest.TestCase):
    def test_config_manager(self):
        conf = ConfigManager('../config.yml')
        conf.register_value(self, 'depend.some_config_val.blup.ble', 5)
        print('Wert: ' + str(conf.get_value(self, 'depend.some_config_val.blup.ble')))
        self.assertEqual(False, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
