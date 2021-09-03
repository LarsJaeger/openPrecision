from context import open_precision
import unittest

import open_precision.plugins.sensor_adapters


# simple unit test for file structure

class MyTestCase(unittest.TestCase):
    def test_something(self):
        print("test starts")
        print(open_precision.plugins.sensor_adapters.__all__)
        #open_precision.utils.get_classes_of_module(open_precision.plugins.sensor_adapters)
        self.assertEqual(True, False, "test001")  # add assertion here


if __name__ == '__main__':
    unittest.main()
