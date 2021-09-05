import importlib

from context import open_precision
import unittest



# simple unit test for file structure

class MyTestCase(unittest.TestCase):
    def test_something(self):
        print("test starts")
        plugin_module = importlib.import_module("open_precision.plugins.sensor_adapters.bno055_aos_adapter.py", ".")
        print(plugin_module)
        # open_precision.utils.get_classes_of_module(open_precision.plugins.sensor_adapters)
        self.assertEqual(True, False, "test001")  # add assertion here


if __name__ == '__main__':
    unittest.main()
