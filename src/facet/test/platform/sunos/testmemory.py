import unittest
from mock import Mock
from mock import patch

import testfacet
import testsunos

from facet.platform.sunos import SunOSProvider 

class SunOSMemoryStatModuleTest(testsunos.AbstractSunOSTest):

    def setUp(self):
        self._module = None 

    def get_module(self):
        if not self._module:
            self._module = SunOSProvider.SunOSMemoryStatModule()
        return self._module
 
    @patch('kstat.Kstat')
    def test_get_memory_used(self, mock_kstat):
        pass

    @patch('kstat.Kstat')
    def test_get_memory_total(self, mock_kstat):
        pass

    @patch('kstat.Kstat')
    def test_get_memory_free(self, mock_kstat):
        pass 
