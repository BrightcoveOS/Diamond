#!/usr/bin/python
# coding=utf-8
################################################################################
import unittest
from mock import Mock
from mock import patch

from cStringIO import StringIO

import testfacet
import testlinux

import facet
import facet.modules

class LinuxLoadAverageModuleTest(testlinux.AbstractLinuxTest):

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))
    def test_get_load_average_should_open_proc_loadavg(self, open_mock):
        
        module = self.get_module(facet.modules.FACET_MODULE_LOADAVG) 
        
        open_mock.return_value = StringIO('')
    
        module.get_load_average()    
     
        open_mock.assert_called_once_with('/proc/loadavg')

    def test_get_load_average_from_fixture(self):
        
        module = self.get_module(facet.modules.FACET_MODULE_LOADAVG) 
        module._PROC = self.get_fixture_path('proc_loadavg')

        (load_1m, load_5m, load_15m, proc_total, proc_run) = module.get_load_average() 

        results = {
            '01': 0.00,
            '05': 0.32,
            '15': 0.56,
            'processes_running': 1,
            'processes_total': 235
        }

        self.assertTrue(load_1m == results['01'])
        self.assertTrue(load_5m == results['05'])
        self.assertTrue(load_15m == results['15'])
        self.assertTrue(proc_run == results['processes_running'])
        self.assertTrue(proc_total == results['processes_total'])
