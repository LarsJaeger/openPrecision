import unittest

from open_precision.core.plugin_base_classes.course_generator import CourseGenerator
from open_precision.core.plugin_base_classes.navigator import Navigator
from open_precision.managers.system_manager import SystemManager


class MyTestCase(unittest.TestCase):
    def test_something(self):
        man = SystemManager()
        man.plugins[Navigator].course = man.plugins[CourseGenerator].generate_course()
        print(f"a: {man.plugins[Navigator].course}")
        print(f"b: {man.plugins[Navigator].course.asdict()}")


if __name__ == '__main__':
    unittest.main()
