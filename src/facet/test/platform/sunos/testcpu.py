import unittest
from mock import Mock
from mock import patch

import testfacet
import testsunos

import facet

from facet.platform.sunos import SunOSProvider 

class SunOSCPUStatModuleTest(testsunos.AbstractSunOSTest):

    def setUp(self):
        self._module = None 

    def get_module(self):
        if not self._module:
            self._module = SunOSProvider.SunOSCPUStatModule()
        return self._module
 
    @patch('kstat.Kstat')
    def test_get_cpu_count(self, mock_kstat):

        mock_kstat_results = testsunos.MockKstatResults()
        mock_kstat_results.set_stats('unix', 0, 'system_misc', {'ncpus': 1}) 
        mock_kstat.return_value.retrieve.side_effect = mock_kstat_results.get_stats
       
        self.assertTrue(self.get_module().get_cpu_count() == 1)

    @patch('kstat.Kstat')
    def test_get_cpu_counters(self, mock_kstat):

        mock_kstat_results = testsunos.MockKstatResults()
        mock_kstat_results.set_stats('unix', 0, 'system_misc', {'ncpus': 1}) 
        mock_kstat_results.set_stats('cpu', 0, 'sys', {'cpu_ticks_idle': 10, 'cpu_ticks_kernel': 20, 'cpu_ticks_user': 30, 'cpu_ticks_wait': 40}) 
        mock_kstat.return_value.retrieve.side_effect = mock_kstat_results.get_stats
        
        cpu_counters = self.get_module().get_cpu_counters(cpu=0)
        
        self.assertTrue(len(cpu_counters) == 4)
        self.assertTrue('user' in cpu_counters.keys())
        self.assertTrue('system' in cpu_counters.keys())
        self.assertTrue('idle' in cpu_counters.keys())
        self.assertTrue('iowait' in cpu_counters.keys())
        self.assertTrue(cpu_counters['idle'] == 10)
        self.assertTrue(cpu_counters['system'] == 20)
        self.assertTrue(cpu_counters['user'] == 30)
        self.assertTrue(cpu_counters['iowait'] == 40)

    @patch('kstat.Kstat')
    def test_get_cpu_counters_with_unknown_cpu(self, mock_kstat):
        
        mock_kstat_results = testsunos.MockKstatResults()
        mock_kstat_results.set_stats('unix', 0, 'system_misc', {'ncpus': 1}) 

        self.assertRaises(facet.FacetError, self.get_module().get_cpu_counters, cpu=1)

    @patch('kstat.Kstat')
    def test_get_cpu_counters_total(self, mock_kstat):

        mock_kstat_results = testsunos.MockKstatResults()
        mock_kstat_results.set_stats('unix', 0, 'system_misc', {'ncpus': 2}) 
        mock_kstat_results.set_stats('cpu', 0, 'sys', {'cpu_ticks_idle': 10, 'cpu_ticks_kernel': 20, 'cpu_ticks_user': 30, 'cpu_ticks_wait': 40}) 
        mock_kstat_results.set_stats('cpu', 1, 'sys', {'cpu_ticks_idle': 10, 'cpu_ticks_kernel': 20, 'cpu_ticks_user': 30, 'cpu_ticks_wait': 40}) 
        mock_kstat.return_value.retrieve.side_effect = mock_kstat_results.get_stats
        
        cpu_counters = self.get_module().get_cpu_counters()
        
        self.assertTrue(len(cpu_counters) == 4)
        self.assertTrue('user' in cpu_counters.keys())
        self.assertTrue('system' in cpu_counters.keys())
        self.assertTrue('idle' in cpu_counters.keys())
        self.assertTrue('iowait' in cpu_counters.keys())
        self.assertTrue(cpu_counters['idle'] == 20)
        self.assertTrue(cpu_counters['system'] == 40)
        self.assertTrue(cpu_counters['user'] == 60)
        self.assertTrue(cpu_counters['iowait'] == 80)
