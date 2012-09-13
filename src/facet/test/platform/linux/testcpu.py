#!/usr/bin/python
# coding=utf-8
################################################################################
import unittest
from mock import Mock
from mock import patch

from cStringIO import StringIO

import testlinux
import testfacet

import facet
import facet.modules

from facet.platform.linux import LinuxProvider 

class LinuxCPUStatModuleTest(testlinux.AbstractLinuxTest):

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))
    def test_get_cpu_counters_should_open_proc_stat(self, open_mock):
        
        module = self.get_module(facet.modules.FACET_MODULE_CPU) 
        
        open_mock.return_value = StringIO('')
    
        module.get_cpu_counters()

        open_mock.assert_called_once_with('/proc/stat')

    @patch('os.access', Mock(return_value=True))
    def test_get_cpu_counters_total(self):
    
        module = self.get_module(facet.modules.FACET_MODULE_CPU) 

        with patch('__builtin__.open', Mock(return_value=StringIO('cpu 100 200 300 400 500 0 0 0 0 0'))):
            cpu_counters = module.get_cpu_counters()

    def test_get_cpu_count_from_fixture(self):
        module = self.get_module(facet.modules.FACET_MODULE_CPU) 
        module._PROC = self.get_fixture_path('proc_stat_1')
        
        self.assertTrue(module.get_cpu_count() == 24)

    def test_get_cpu_counters_total_from_fixture(self):

        module = self.get_module(facet.modules.FACET_MODULE_CPU) 
        module._PROC = self.get_fixture_path('proc_stat_1')
        
        test_counters = {'softirq': '59032', 
                        'iowait': '575304', 
                        'system': '8454152', 
                        'guest': '0', 
                        'idle': '3925807593', 
                        'user': '29055787', 
                        'guest_nice': '0', 
                        'irq': '3', 
                        'steal': '0', 
                        'nice': '1104382'}

        cpu_counters = module.get_cpu_counters()
        
        for k in cpu_counters:
            self.assertTrue(cpu_counters[k] == test_counters[k])

    def test_get_cpu_counters_from_fixture(self):
        
        module = self.get_module(facet.modules.FACET_MODULE_CPU) 
        module._PROC = self.get_fixture_path('proc_stat_1')
       
        test_counters = {'softirq': '390', 
                        'iowait': '43098', 
                        'system': '708125', 
                        'guest': '0', 
                        'idle': '158813910', 
                        'user': '5549355', 
                        'guest_nice': '0', 
                        'irq': '0', 
                        'steal': '0', 
                        'nice': '101649'}  

        cpu_counters = module.get_cpu_counters(cpu=1)

        for k in cpu_counters:
            self.assertTrue(cpu_counters[k] == test_counters[k])
