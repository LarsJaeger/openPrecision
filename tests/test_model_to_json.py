import json
import math
import unittest
import context
import time

from open_precision.core.interfaces.course_generator import CourseGenerator
from open_precision.core.interfaces.navigator import Navigator
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
        course = man.plugins[CourseGenerator].generate_course()
        print(course.asdict())


def main():
    unittest.main()


if __name__ == "__main__":
    main()
