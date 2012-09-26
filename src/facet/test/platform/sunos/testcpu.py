#!/usr/bin/python
# coding=utf-8
################################################################################
import unittest
from mock import Mock
from mock import patch

import testfacet
import testsunos

import facet
import facet.modules

from facet.platform.sunos import SunOSProvider 

class SunOSCPUStatModuleTest(testsunos.AbstractSunOSTest):
 
    @patch('kstat.Kstat')
    def test_get_cpu_count(self, mock_kstat):
        
        module = self.get_module(facet.modules.FACET_MODULE_CPU)

        mock_kstat_results = testsunos.MockKstatResults()
        mock_kstat_results.set_stats('unix', 0, 'system_misc', {'ncpus': 1}) 
        mock_kstat.return_value.retrieve.side_effect = mock_kstat_results.retrieve_stats
       
        self.assertTrue(module.get_cpu_count() == 1)

    @patch('kstat.Kstat')
    def test_get_cpu_counters(self, mock_kstat):

        module = self.get_module(facet.modules.FACET_MODULE_CPU)

        mock_kstat_results = testsunos.MockKstatResults()
        mock_kstat_results.set_stats('unix', 0, 'system_misc', {'ncpus': 1}) 
        mock_kstat_results.set_stats('cpu', 0, 'sys', {'cpu_ticks_idle': 10, 'cpu_ticks_kernel': 20, 'cpu_ticks_user': 30, 'cpu_ticks_wait': 40}) 
        mock_kstat.return_value.retrieve.side_effect = mock_kstat_results.retrieve_stats
        
        cpu_counters = module.get_cpu_counters(cpu=0)
        
        self.assertTrue(len(cpu_counters) == 4)
        self.assertTrue('user' in cpu_counters.keys())
        self.assertTrue('kernel' in cpu_counters.keys())
        self.assertTrue('idle' in cpu_counters.keys())
        self.assertTrue('wait' in cpu_counters.keys())
        self.assertTrue(cpu_counters['idle'] == 10)
        self.assertTrue(cpu_counters['kernel'] == 20)
        self.assertTrue(cpu_counters['user'] == 30)
        self.assertTrue(cpu_counters['wait'] == 40)

    @patch('kstat.Kstat')
    def test_get_cpu_counters_with_unknown_cpu(self, mock_kstat):
        
        module = self.get_module(facet.modules.FACET_MODULE_CPU)
        
        mock_kstat_results = testsunos.MockKstatResults()
        mock_kstat_results.set_stats('unix', 0, 'system_misc', {'ncpus': 1}) 

        self.assertRaises(facet.FacetError, module.get_cpu_counters, cpu=1)

    @patch('kstat.Kstat')
    def test_get_cpu_counters_total(self, mock_kstat):
        
        module = self.get_module(facet.modules.FACET_MODULE_CPU)

        mock_kstat_results = testsunos.MockKstatResults()
        mock_kstat_results.set_stats('unix', 0, 'system_misc', {'ncpus': 2}) 
        mock_kstat_results.set_stats('cpu', 0, 'sys', {'cpu_ticks_idle': 10, 'cpu_ticks_kernel': 20, 'cpu_ticks_user': 30, 'cpu_ticks_wait': 40}) 
        mock_kstat_results.set_stats('cpu', 1, 'sys', {'cpu_ticks_idle': 10, 'cpu_ticks_kernel': 20, 'cpu_ticks_user': 30, 'cpu_ticks_wait': 40}) 
        mock_kstat.return_value.retrieve.side_effect = mock_kstat_results.retrieve_stats
        
        cpu_counters = module.get_cpu_counters()
        
        self.assertTrue(len(cpu_counters) == 4)
        self.assertTrue('user' in cpu_counters.keys())
        self.assertTrue('kernel' in cpu_counters.keys())
        self.assertTrue('idle' in cpu_counters.keys())
        self.assertTrue('wait' in cpu_counters.keys())
        self.assertTrue(cpu_counters['idle'] == 20)
        self.assertTrue(cpu_counters['kernel'] == 40)
        self.assertTrue(cpu_counters['user'] == 60)
        self.assertTrue(cpu_counters['wait'] == 80)

################################################################################
if __name__ == "__main__":
    unittest.main()
