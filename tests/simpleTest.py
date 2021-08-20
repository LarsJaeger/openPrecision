import numpy as np

from context import openPrecision
import unittest


# simple unit test for file structure

class MyTestCase(unittest.TestCase):
    def test_something(self):
        print("test starts")
        print(openPrecision.utils.get_rotation_matrix_ypr(np.array([5, 5, 5])))
        self.assertEqual(True, False, "test001")  # add assertion here


if __name__ == '__main__':
    unittest.main()
