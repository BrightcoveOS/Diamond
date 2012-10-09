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

class LinuxMemoryStatModuleTest(testlinux.AbstractLinuxTest):

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))
    def test_get_memory_usage_should_open_proc_meminfo(self, open_mock):
        
        module = self.get_module(facet.modules.FACET_MODULE_MEMORY) 
        
        open_mock.return_value = StringIO('')
    
        module.get_memory_usage()

        open_mock.assert_called_once_with('/proc/meminfo')
    
    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))
    def test_get_swap_usage_should_open_proc_meminfo(self, open_mock):
        
        module = self.get_module(facet.modules.FACET_MODULE_MEMORY) 
        
        open_mock.return_value = StringIO('')
    
        module.get_swap_usage()

        open_mock.assert_called_once_with('/proc/meminfo')

    #@patch('os.access', Mock(return_value=True))
    #def test_get_memory_usage(self):
    #
    #    module = self.get_module(facet.modules.FACET_MODULE_MEMORY) 

        #metrics = {
        #    'MemTotal': 49554212,
        #    'MemFree': 35194496,
        #    'Buffers': 1526304,
        #    'Cached': 10726736,
        #    'Active': 10022168,
        #    'Dirty': 24748,
        #    'Inactive': 2524928,
        #    'SwapTotal': 262143996,
        #    'SwapFree': 262143996,
        #    'SwapCached': 0,
        #    'VmallocTotal': 34359738367,
        #    'VmallocUsed': 445452,
        #    'VmallocChunk': 34311049240
        #}

    #    with patch('__builtin__.open', Mock(return_value=StringIO('cpu 100 200 300 400 500 0 0 0 0 0'))):
    #        cpu_counters = module.get_cpu_counters()

    def test_get_memory_usage_from_fixture(self):
        module = self.get_module(facet.modules.FACET_MODULE_MEMORY) 
        module._PROC = self.get_fixture_path('proc_meminfo')

        memory_total, memory_free, memory_used = module.get_memory_usage()

        self.assertTrue(memory_total == 49554212 * 1024)
        self.assertTrue(memory_free ==  35194496 * 1024)
        self.assertTrue(memory_used == 14359716 * 1024)
    
    def test_get_swap_usage_from_fixture(self):
        module = self.get_module(facet.modules.FACET_MODULE_MEMORY) 
        module._PROC = self.get_fixture_path('proc_meminfo')

        swap_total, swap_free, swap_used = module.get_swap_usage()

        self.assertTrue(swap_total == 262143996 * 1024)
        self.assertTrue(swap_free == 262143996 * 1024)
        self.assertTrue(swap_used == 0)
