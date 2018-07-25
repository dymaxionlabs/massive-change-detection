# coding=utf-8
"""MultibandDifferenceAlgorithm Test

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'Damián Silvani'
__date__ = '2018-07-25'
__copyright__ = '(C) 2018 by Dymaxion Labs'

import unittest

class MultibandDifferenceAlgorithmTest(unittest.TestCase):
    """Test multiband difference algorithm."""

    def setUp(self):
        """Runs before each test."""
        pass

    def tearDown(self):
        """Runs after each test."""
        pass

    def test_true(self):
        """Test that it works."""
        self.assertTrue(True)


if __name__ == "__main__":
    suite = unittest.makeSuite(MultibandDifferenceAlgorithmTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
