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

class LinuxDiskStatModuleTest(testlinux.AbstractLinuxTest):

    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))
    def test_get_disks_should_open_proc_partitions(self, open_mock):
        
        module = self.get_module(facet.modules.FACET_MODULE_DISK) 
        
        open_mock.return_value = StringIO('')
    
        module.get_disks()

        open_mock.assert_called_once_with('/proc/partitions')
    
    @patch('__builtin__.open')
    @patch('os.access', Mock(return_value=True))
    def test_get_disk_counters_should_open_proc_diskstats(self, open_mock):
        
        module = self.get_module(facet.modules.FACET_MODULE_DISK) 
        
        open_mock.return_value = StringIO('')
   
        try: 
            module.get_disk_counters('foo')
        except:
            pass

        open_mock.assert_called_once_with('/proc/diskstats')

    def test_get_disks_should_work_with_mock_data(self):
        module = self.get_module(facet.modules.FACET_MODULE_DISK) 

        module._PROC_PARTITIONS = self.get_fixture_path('proc_partitions')

        disks = module.get_disks()
      
        self.assertEqual(sorted(disks), ['dm-0', 'dm-1', 'sda', 'sda1', 'sda2'])
    
    def test_get_disk_counters_should_work_with_mock_data(self):
        module = self.get_module(facet.modules.FACET_MODULE_DISK) 

        module._PROC_DISKSTATS = self.get_fixture_path('proc_diskstats_1')
        
        disk_stats = module.get_disk_counters('sda')

        self.assertEqual(sorted(disk_stats.keys()), ['io_in_progress', 
                                                    'io_milliseconds', 
                                                    'io_milliseconds_weighted', 
                                                    'reads', 
                                                    'reads_merged', 
                                                    'reads_milliseconds', 
                                                    'reads_sectors', 
                                                    'writes', 
                                                    'writes_merged', 
                                                    'writes_milliseconds', 
                                                    'writes_sectors'])

        self.assertEqual(sorted(disk_stats.values()), [0.0, 
                                                    1650390.0, 
                                                    2176303.0,
                                                    8213219.0, 
                                                    8426453.0, 
                                                    11766889.0, 
                                                    27366923.0, 
                                                    51741706.0, 
                                                    207996798.0,
                                                    216207918.0, 
                                                    313073680.0]) 
