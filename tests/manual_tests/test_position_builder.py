# test_template.py
# change 'template' to python file name of file to be tested
import unittest

from open_precision.core.plugin_base_classes.machine_state_builder import MachineStateBuilder
from open_precision.system_hub import SystemHub


class TestPositionBuilder(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @classmethod
    def setUpClass(cls) -> None:
        """This setup will only be executed once before the first manual_tests"""

    @classmethod
    def tearDownClass(cls) -> None:
        """This teardown will only be executed once after all manual_tests are done"""

    def test_method(self):
        man = SystemHub()
        counter = 0
        try:
            while True:
                counter += 1
                print("a")
                print(f"pos {counter}: {man.plugins[MachineStateBuilder].current_position}")
        except KeyboardInterrupt:
            print("KeyboardInterrupt")


def main():
    unittest.main()


if __name__ == "__main__":
    main()
