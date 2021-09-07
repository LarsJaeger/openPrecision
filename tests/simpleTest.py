import importlib

from context import open_precision
import unittest

# simple unit test for file structure
from open_precision.core.sensor_manager import SensorManager


class MyTestCase(unittest.TestCase):
    def test_something(self):
        print("test starts")
        sensor_manager = SensorManager(None)
        # open_precision.utils.get_classes_of_module(open_precision.plugins.sensor_wrappers)
        self.assertEqual(True, False, "test001")  # add assertion here


if __name__ == '__main__':
    unittest.main()
