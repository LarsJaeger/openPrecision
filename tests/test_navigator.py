# test_template.py
# change 'template' to python file name of file to be tested
import unittest
import context
import time

from open_precision.core.managers.manager import Manager


class TestPositionBuilder(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @classmethod
    def setUpClass(cls) -> None:
        """This setup will only be executed once before the first tests"""

    @classmethod
    def tearDownClass(cls) -> None:
        """This teardown will only be executed once after all tests are done"""

    def test_method(self):
        man = Manager()
        try:
            while True:
                man.navigator.course = man.course_generator.generate_course()
                print(f"pos {counter}: {man.navigator.steering_angle}")
        except KeyboardInterrupt:
            print("KeyboardInterrupt")


def main():
    unittest.main()


if __name__ == "__main__":
    main()
