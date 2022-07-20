import unittest

import context
from open_precision.core.managers.package_plugin_manager import PackagePluginManager


class MyTestCase(unittest.TestCase):
    def test_something(self):
        print("test starts")
        sensor_manager = PackagePluginManager(
            None,
            "open_precision.core.interfaces.sensor_types",
            "open_precision.plugins.sensor_wrappers",
        )
        # open_precision.utils.get_classes_of_module(open_precision.plugins.sensor_wrappers)
        print("test ends")
        self.assertEqual(True, True, "test001")  # add assertion here


if __name__ == "__main__":
    unittest.main()
