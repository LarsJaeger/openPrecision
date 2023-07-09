import unittest

import neomodel

from open_precision.core.model import map_model, DataModelBase
from open_precision.core.model.course import Course
from open_precision.core.model.location import Location
from open_precision.core.model.path import Path
from open_precision.core.model.waypoint import Waypoint


class MyTestCase(unittest.TestCase):
    def test_model(self):
        #map_model("neo4j+s://neo4j:Qa89VmwaJINAYWqNm6ZYAWJFq8HXQB7LMH0UbZtFtkk@25c438c1.databases.neo4j.io:7687")
        map_model("neo4j://neo4j:password@127.0.0.1:7687")

        waypoint = Waypoint(location=Location(x=1.0, y=2.0, z=3.0))
        path = Path()
        course = Course(name="test1", description="bla")
        course.save()
        path.save()
        waypoint.save()
        course.add_path(path)
        path.add_waypoint(waypoint)
        print(list(course.CONTAINS))
        print(list(path.IS_CONTAINED_BY))
        course_json = course.to_json()
        print(course_json)
        reconstr_course = DataModelBase.from_json(course_json)
        print("reconstr. type: " + str(type(reconstr_course)))
        print("reconstr. object: " + str(reconstr_course))
        self.assertEqual(reconstr_course)
if __name__ == '__main__':
    unittest.main()
