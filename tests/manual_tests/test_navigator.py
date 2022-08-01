# test_template.py
# change 'template' to python file name of file to be tested
import math
import unittest
import time

from open_precision.core.plugin_base_classes.course_generator import CourseGenerator
from open_precision.core.plugin_base_classes.navigator import Navigator
from open_precision.manager import Manager


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
        man = Manager()
        man.plugins[Navigator].course = man.plugins[CourseGenerator].generate_course()
        try:
            while True:
                print(f"angle: {math.degrees(man.plugins[Navigator].steering_angle)}")
                time.sleep(5)
        except KeyboardInterrupt:
            print("KeyboardInterrupt")


def main():
    unittest.main()


if __name__ == "__main__":
    main()
