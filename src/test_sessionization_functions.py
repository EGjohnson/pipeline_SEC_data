# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 13:28:23 2018

@author: ej
"""
import unittest
import datetime
from sessionization import check_field_length, convert_datetime

class TestFactorial(unittest.TestCase):
    """
    Our basic test class
    """
    #test 1
    def test_check_field_length(self):
        # methods that start with test treated as test case
        self.assertTrue(check_field_length(range(0,15),0))
        self.assertFalse(check_field_length(range(0,12),0))
        self.assertTrue(check_field_length(range(0),0)) 
       
    #test 2
    def test_convert_datetime(self):
        tlt=['106.120.173.jie', '2017-06-30', '00:00:02']
        tlf=['106.120.173.jie', '2017-06-30', '00:00']
        # if strings not in proper format returns value error
        self.assertRaises(ValueError,convert_datetime,tlf,0)
        # properly formatted string returns datetime object
        is_true=isinstance(convert_datetime(tlt,0), datetime.datetime)
        self.assertTrue(is_true)
        
    #test 3



if __name__ == '__main__':
    unittest.main()

