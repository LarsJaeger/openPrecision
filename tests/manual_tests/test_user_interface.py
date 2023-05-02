# test_template.py
# change 'template' to python file name of file to be tested
import unittest

from open_precision.managers.system_manager import SystemManager


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
        man = SystemManager()


def main():
    unittest.main()


if __name__ == "__main__":
    main()
