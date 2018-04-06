# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 13:28:23 2018

@author: ej
"""
import unittest
import datetime
from sessionization import check_field_length, convert_datetime
from sessionization import *

class TestFactorial(unittest.TestCase):
    """
    Our basic test class
    """
    def return_group():  
        g1=('101.81.133.jja', datetime(2017, 6, 30, 0, 0), '1608552.00001047469-17-004337-index.htm2', '2017-06-30', '00:00:00')
        g2=('101.81.133.jja', datetime(2017, 6, 30, 0, 5), '1027281.00000898430-02-001167-index.htm3', '2017-06-30', '00:00:05')
        g3=('101.81.133.jja', datetime(2017, 6, 30, 0, 10), '1027281.00000898430-02-001167-index.htm3', '2017-06-30', '00:00:10')
        grp=[g1,g2,g3]
        return grp
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
        is_true=isinstance(convert_datetime(tlt,0), datetime)
        self.assertTrue(is_true)
        
    #test 3
    def test_convert_unique_doc_request(self):
        tlt=['', '', '', '', '1618174.0', '0001140361-17-026711', '.txt']
        tlf2=[]
        # if string empty return index error 
        self.assertRaises(IndexError,convert_unique_doc_request,tlf2,0)
        # properly formatted string returns datetime object
        is_true=isinstance(convert_unique_doc_request(tlt,0),str)
        self.assertTrue(is_true)
        
    # test 4
    def test_is_session_over(self):
        a=datetime(2017, 6, 30, 0, 0, 4)
        b=datetime(2017, 6, 30, 0, 0, 5)
        c=datetime(2017, 6, 30, 0, 0, 6)
        d=datetime(2017, 6, 30, 0, 0, 4)
        e=datetime(2017, 6, 30, 0, 0, 6)
        f=datetime(2017, 6, 30, 0, 0, 8)
        g=datetime(2017, 6, 30, 0, 0, 6)
        h=datetime(2017, 6, 30, 0, 0, 7)
        i=datetime(2017, 6, 30, 0, 0, 8)
        ct=datetime(2017, 6, 30, 0, 0, 10) #current time (10 seconds)
        
        st=[("ip1",a,'s'),("ip1",b,'s'),("ip1",c,'s')] #session should end
        sf1=[("ip2",d,'s'),("ip2",e,'s'),("ip2",f,'s')] 
        sf2=[("ip3",g,'s'),("ip3",h,'s'),("ip3",i,'s')]
        tups=st+sf1+sf2
        
        self.assertTrue(is_session_over("ip1",tups,ct,3))
        self.assertFalse(is_session_over("ip2",tups,ct,3))
        
        
    def test_group_to_entry(self):   
        g1=('101.81.133.jja', datetime(2017, 6, 30, 0, 0), '1608552.00001047469-17-004337-index.htm2', '2017-06-30', '00:00:00')
        g2=('101.81.133.jja', datetime(2017, 6, 30, 0, 5), '1027281.00000898430-02-001167-index.htm3', '2017-06-30', '00:00:05')
        g3=('101.81.133.jja', datetime(2017, 6, 30, 0, 10), '1027281.00000898430-02-001167-index.htm3', '2017-06-30', '00:00:10')
        grp=[g1,g2,g3]
        #self.assertgroup_to_entry
        
        

if __name__ == '__main__':
    unittest.main()

