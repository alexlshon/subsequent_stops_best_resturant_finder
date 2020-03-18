import unittest
import hungry.cta as cta
from random import randint


class TestProcessingFunctions(unittest.TestCase):

    def test_get_elem_index(self):
        int_list = [x for x in range(0, 1000, 1)]
        for i in range(0, 200, 1):
            rint = randint(0, 1000)
            self.assertEqual(rint, cta.get_elem_index(int_list, rint))


if __name__ == '__main__':
    unittest.main()
