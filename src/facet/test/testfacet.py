#!/usr/bin/python
# coding=utf-8
################################################################################
import sys
import os
import unittest
import time

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

    def test_get_cpu_counters(self):
        self.assertTrue(isinstance(self.facet.cpu.get_cpu_counters(), dict))

class FacetMemoryStatTest(AbstractFacetTest):
    
    def test_memory_module(self):
        self.assertTrue('memory' in self.facet)
        self.assertTrue('memory' in self.facet.list())
        self.assertTrue('memory' in self.facet.provider.modules.keys()) 
        self.assertTrue(issubclass(self.facet.memory.__class__, facet.modules.MemoryStatModule)) 
        
        print "used: %f" % (float(self.facet.memory.get_memory_used()) / 1024.0 / 1024.0)
        print "total: %f" % (float(self.facet.memory.get_memory_total()) / 1024.0 / 1024.0)
        print "free: %f" % (float(self.facet.memory.get_memory_free()) / 1024.0 / 1024.0)
        
        print "swap used: %f" % (float(self.facet.memory.get_swap_used()) / 1024.0 / 1024.0)
        print "swap total: %f" % (float(self.facet.memory.get_swap_total()) / 1024.0 / 1024.0)
        print "swap free: %f" % (float(self.facet.memory.get_swap_free()) / 1024.0 / 1024.0)
    
    def test_get_memory_used(self):    
        self.assertTrue(self.facet.memory.get_memory_used() == self.facet.memory.get_memory_total() - self.facet.memory.get_memory_free())

    def test_get_memory_total(self):
        self.assertTrue(self.facet.memory.get_memory_total() > 0)

    def test_get_memory_free(self):
        self.assertTrue(self.facet.memory.get_memory_free() > 0)

    def test_get_swap_used(self):
        self.assertTrue(self.facet.memory.get_swap_used() == self.facet.memory.get_swap_total() - self.facet.memory.get_swap_free())

    def test_get_swap_total(self):       
        self.assertTrue(self.facet.memory.get_swap_total() > 0)

    def test_get_swap_free(self):
        self.assertTrue(self.facet.memory.get_swap_free() > 0)
 
if __name__ == "__main__":
    unittest.main()
