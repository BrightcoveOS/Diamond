#!/usr/bin/python
# coding=utf-8
################################################################################
import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

import facet
import facet.modules

class AbstractFacetTest(unittest.TestCase):
    
    def setUp(self):
        self.facet = facet.Facet(test_option = 'bar') 

    def tearDown(self):
        self.facet = None 

class FacetProviderTest(AbstractFacetTest):
    pass

class FacetLoadAverageTest(AbstractFacetTest):
    
    def test_loadavg_module(self):
        self.assertTrue('loadavg' in self.facet)
        self.assertTrue('loadavg' in self.facet.list())
        self.assertTrue('loadavg' in self.facet.provider.modules.keys()) 
        self.assertTrue(issubclass(self.facet.loadavg.__class__, facet.modules.LoadAverageModule)) 

    def test_get_load_average(self):
        self.assertTrue(isinstance(self.facet['loadavg'].get_load_average(), tuple))

class FacetCPUStatTest(AbstractFacetTest):

    def test_cpu_module(self):
        self.assertTrue('cpu' in self.facet)
        self.assertTrue('cpu' in self.facet.list())
        self.assertTrue('cpu' in self.facet.provider.modules.keys()) 
        self.assertTrue(issubclass(self.facet.cpu.__class__, facet.modules.CPUStatModule)) 
    
    def test_get_cpu_count(self):
        self.assertTrue(self.facet['cpu'].get_cpu_count() > 0) 

    def test_get_cpu_usage(self):
        self.assertTrue(isinstance(self.facet.cpu.get_cpu_usage(), dict))


if __name__ == "__main__":
    unittest.main()
