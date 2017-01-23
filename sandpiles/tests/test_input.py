import unittest

import os
import sys
import time
from os.path import dirname as dn, abspath as ap

main_path = dn(dn(dn(ap(__file__))))
sys.path.append(main_path)
from sandpiles import Sandpile


class Test(unittest.TestCase):
    def test_input(self):
        s_one = Sandpile(
            custom=1,
            grid=[5, ]
        ).grid
        s_two = Sandpile(
            custom=1,
            grid=[
                5, 5,
                5, 5
            ]
        ).grid
        s_three = Sandpile(
            custom=1,
            grid=[
                5, 5, 5,
                5, 5, 5,
                5, 5, 5
            ]
        ).grid
        s_four = Sandpile(
            single=5,
            times=5
        ).grid
        self.assertEqual(
            [[1]],
            s_one
        )
        self.assertEqual(
            [[3, 3],
             [3, 3]],
            s_two)
        self.assertEqual([
            [3, 1, 3],
            [1, 1, 1],
            [3, 1, 3]], s_three)
        self.assertEqual(
            [[1, 3, 0, 3, 1],
             [3, 3, 2, 3, 3],
             [0, 2, 1, 2, 0],
             [3, 3, 2, 3, 3],
             [1, 3, 0, 3, 1]],
            s_four)


if __name__ == '__main__':
    unittest.main()
