# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 13:28:23 2018

@author: ej
"""
import unittest
from sessionization import check_field_length

class TestFactorial(unittest.TestCase):
    """
    Our basic test class
    """
    
    def test_check_field_length(self):
        # methods that start with test treated as test case
        self.assertTrue(check_field_length(range(0,15),0))


if __name__ == '__main__':
    unittest.main()

