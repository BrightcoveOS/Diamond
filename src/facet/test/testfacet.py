#!/usr/bin/python
# coding=utf-8
################################################################################
import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

import facet

class AbstractFacetTest(unittest.TestCase):
    
    def setUp(self):
        self.facet = facet.Facet() 

    def tearDown(self):
        self.facet = None 

class FacetProviderTest(AbstractFacetTest):
    pass

class FacetLoadAverageTest(AbstractFacetTest):
    
    def test_get_load_average(self):
        pass 

if __name__ == "__main__":
    unittest.main()
