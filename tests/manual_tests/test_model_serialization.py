import unittest

from open_precision.core.model.action import Action
from open_precision.core.plugin_base_classes.course_generator import CourseGenerator
from open_precision.core.plugin_base_classes.navigator import Navigator
from open_precision.system_hub import SystemHub


class MyTestCase(unittest.TestCase):
    def test_something(self):
        man = SystemHub()
        man.plugins[Navigator].current_course = man.plugins[CourseGenerator].generate_course()
        print(f"a: {man.plugins[Navigator].current_course}")
        print(f"b: {man.plugins[Navigator].current_course.asdict()}")

    def test_something2(self):
        my_action = '{"function_identifier": "config.load_config", "args": [1,2,3], "kw_args": {"yaml": "MyTest: 3"}}'
        print(Action.from_json(my_action))



if __name__ == '__main__':
    unittest.main()
