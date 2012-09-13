import unittest
from mock import Mock
from mock import patch

import testfacet
import testsunos

import facet
import facet.modules

class SunOSLoadAverageModuleTest(testsunos.AbstractSunOSTest):

    @patch('kstat.Kstat')
    def test_get_load_average(self, mock_kstat):

        module = self.get_module(facet.modules.FACET_MODULE_LOADAVG) 
    
        mock_kstat_results = {'avenrun_1min': 100*256.0, 'avenrun_5min': 200*256.0, 'avenrun_15min': 300*256.0, 'nproc': 500}
        mock_kstat.return_value.retrieve.return_value = mock_kstat_results
        
        self.assertTrue(module.get_load_average() == (100.0, 200.0, 300.0, 500, 0))
