import unittest
from mock import Mock
from mock import patch

import testfacet
import testsunos

from facet.platform.sunos import SunOSProvider 

class SunOSLoadAverageModuleTest(testsunos.AbstractSunOSTest):

    def setUp(self):
        self._module = None 

    def get_module(self):
        if not self._module:
            self._module = SunOSProvider.SunOSLoadAverageModule()
        return self._module
 
    @patch('kstat.Kstat')
    def test_get_load_average(self, mock_kstat):
        
        mock_kstat_results = {'avenrun_1min': 100*256.0, 'avenrun_5min': 200*256.0, 'avenrun_15min': 300*256.0, 'nproc': 500}
        mock_kstat.return_value.retrieve.return_value = mock_kstat_results
        
        self.assertTrue(self.get_module().get_load_average() == (100.0, 200.0, 300.0, 500, 0))
