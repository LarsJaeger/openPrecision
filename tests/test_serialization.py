import unittest

from open_precision.core.interfaces.course_generator import CourseGenerator
from open_precision.core.interfaces.navigator import Navigator
from open_precision.core.managers.manager import Manager


class MyTestCase(unittest.TestCase):
    def test_something(self):
        man = Manager()
        man.plugins[Navigator].course = man.plugins[CourseGenerator].generate_course()
        print(f"a: {man.plugins[Navigator].course}")
        print(f"b: {man.plugins[Navigator].course.to_dict()}")


if __name__ == '__main__':
    unittest.main()
