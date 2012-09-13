import mock
import unittest

class MockKstatResults(object):
    
    def __init__(self):
        self._stats = {}

    def set_stats(self, module, instance, name, stats):
        self._stats[(module, instance, name)] = stats 

    def get_stats(self, module, instance, name):
        return self._stats[(module, instance, name)] 

class AbstractSunOSTest(unittest.TestCase):
    pass
