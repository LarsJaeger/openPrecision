import unittest

from open_precision.core.model.action import Action
from open_precision.core.plugin_base_classes.course_generator import CourseGenerator
from open_precision.core.plugin_base_classes.navigator import Navigator
from open_precision.managers.persistence_manager import PersistenceManager
from open_precision.managers.system_manager import SystemManager


class MyTestCase(unittest.TestCase):
    def test_something(self):
        man = SystemManager()
        man.plugins[Navigator].course = man.plugins[CourseGenerator].generate_course()
        print(f"a: {man.plugins[Navigator].course}")
        print(f"b: {man.plugins[Navigator].course.asdict()}")

    def test_something2(self):
        man = PersistenceManager(None)
        my_action = '{"function_identifier": "config.load_config", "args": [1,2,3], "kw_args": {"yaml": "MyTest: 3"}}'
        print(Action.from_json(my_action))



if __name__ == '__main__':
    unittest.main()
