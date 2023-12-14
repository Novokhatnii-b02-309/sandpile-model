import unittest
from sandpile_func import *


class TestStringMethods(unittest.TestCase):

    def test_csv_to_np_1(self):
        res = csv_to_np('/test.csv')
        print(res)
        true_res = (np.array([
                    [1000, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [1000, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1000, 0, 0, 0, 0, 0]], dtype=np.uint32), 10, 10)
        print(true_res)
        is_equal1 = np.array_equal(res[0], true_res[0])
        is_equal2 = res[1] == true_res[1]
        is_equal3 = res[2] == true_res[2]
        is_equal = is_equal1 and is_equal2 and is_equal3
        self.assertTrue(is_equal)
