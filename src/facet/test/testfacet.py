#!/usr/bin/python
# coding=utf-8
################################################################################
import sys
import os
import unittest
import time
import logging
import optparse
import inspect
import traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

import facet
import facet.modules

class AbstractFacetTest(unittest.TestCase):
    
    def setUp(self):
        self.facet = facet.Facet(test_option = 'bar') 

    def tearDown(self):
        self.facet = None 

class AbstractFacetModuleTest(unittest.TestCase):

    def get_platform_provider(self):
        raise NotImplementedError() 
    
    def get_fixture_path(self, fixture_name):
        file = os.path.join(os.path.dirname(inspect.getfile(self.__class__)),
                            'fixtures',
                            fixture_name)
        if not os.access(file, os.R_OK):
            print "Missing Fixture " + file
        return file

    def get_fixture(self, fixture_name):
        file = open(self.get_fixture_path(fixture_name), 'r')
        data = StringIO(file.read())
        file.close()
        return data
    
    def get_module(self, module_type):
        if not hasattr(self, '_module'):
            self._module = None
        if not self._module:
            platform_provider_class = self.get_platform_provider()
            platform_provider = platform_provider_class()
            self._module = platform_provider.modules[module_type]
        return self._module

class FacetLoadAverageTest(AbstractFacetTest):
    
    def test_loadavg_module(self):
        self.assertTrue('loadavg' in self.facet)
        self.assertTrue('loadavg' in self.facet.list())
        self.assertTrue('loadavg' in self.facet.provider.modules.keys()) 
        self.assertTrue(issubclass(self.facet.loadavg.__class__, facet.modules.LoadAverageModule)) 

    def test_get_load_average(self):
        self.assertTrue(isinstance(self.facet.loadavg.get_load_average(), tuple))

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
        
        #print "used: %f" % (float(self.facet.memory.get_memory_used()) / 1024.0 / 1024.0)
        #print "total: %f" % (float(self.facet.memory.get_memory_total()) / 1024.0 / 1024.0)
        #print "free: %f" % (float(self.facet.memory.get_memory_free()) / 1024.0 / 1024.0)
        #
        #print "swap used: %f" % (float(self.facet.memory.get_swap_used()) / 1024.0 / 1024.0)
        #print "swap total: %f" % (float(self.facet.memory.get_swap_total()) / 1024.0 / 1024.0)
        #print "swap free: %f" % (float(self.facet.memory.get_swap_free()) / 1024.0 / 1024.0)
    
    def test_get_memory_used(self):    
        self.assertTrue(self.facet.memory.get_memory_used() > 0)

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

class FacetDiskStatTest(AbstractFacetTest):
    
    def test_get_disks(self):
        self.assertTrue(len(self.facet.disk.get_disks()) > 0)

    def test_get_mounts(self):
        self.assertTrue(len(self.facet.disk.get_mounts()) > 0)

def get_facet_provider_tests(platform):
    
    facet_provider_name = facet.get_platform_provider_name(platform) 
    facet_provider_test_path = os.path.join(os.path.dirname(__file__), 'platform', facet_provider_name)

    # If the platform provider path does not exist, assume unsupported platform
    if not os.path.exists(facet_provider_test_path):
        raise NotImplementedError("Provider directory does not exist: %s. Platform not supported." % facet_provider_test_path) 

    return load_facet_provider_tests(facet_provider_test_path)

def load_facet_provider_tests(path):
    tests = {} 
    for f in os.listdir(path):
        test_path = os.path.abspath(os.path.join(path, f))
        if (os.path.isfile(test_path)
                and len(f) > 3
                and f[-3:] == '.py'
                and f[0:4] == 'test'):
            sys.path.append(os.path.dirname(test_path))
            sys.path.append(os.path.dirname(os.path.dirname(test_path)))
            modname = f[:-3]
            try:
                # Import the module
                tests[modname] = __import__(modname, globals(), locals(), ['*'])
                #print "Imported module: %s" % (modname)
            except Exception:
                print "Failed to import module: %s. %s" % (modname, traceback.format_exc())

    for f in os.listdir(path):
        test_path = os.path.abspath(os.path.join(path, f))
        if os.path.isdir(test_path):
            tests = dict(tests.items() + load_facet_provider_tests(test_path).items())

    return tests
 
if __name__ == "__main__":

    # Disable log output for the unit tests
    log = logging.getLogger("diamond")
    log.disabled = True

    # Initialize Options
    parser = optparse.OptionParser()
    parser.add_option("-v",
                      "--verbose",
                      dest="verbose",
                      default=1,
                      action="count",
                      help="verbose")
    
    parser.add_option("-p",
                      "--platform",
                      dest="platform",
                      default=sys.platform, 
                      help="platform")

    # Parse Command Line Args
    (options, args) = parser.parse_args()

    # Load Platform Specific Tests
    platform_tests = get_facet_provider_tests(options.platform) 
    tests = []
    for test_module in platform_tests:
        for attr_name in dir(platform_tests[test_module]):
            attr = getattr(platform_tests[test_module], attr_name) 
            if inspect.isclass(attr):            
                if issubclass(attr, unittest.TestCase):
                    #print "Found Test: %s " % (attr_name)
                    tests.append(unittest.TestLoader().loadTestsFromTestCase(attr))

    # Load Base Tests
    if options.platform == sys.platform:
        # Note: if platform is overriden to a different platform, do not run base tests
        for attr_name in globals(): 
            attr = globals()[attr_name] 
            if inspect.isclass(attr):            
                if issubclass(attr, unittest.TestCase):
                    #print "Found Test: %s " % (attr_name)
                    tests.append(unittest.TestLoader().loadTestsFromTestCase(attr))

    suite = unittest.TestSuite(tests)
    unittest.TextTestRunner(verbosity=options.verbose).run(suite)
