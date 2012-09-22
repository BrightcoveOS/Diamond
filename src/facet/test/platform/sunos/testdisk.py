import unittest
from mock import Mock, MagicMock
from mock import patch

import testfacet
import testsunos

import facet
import facet.modules

import kstat
from kstat.libkstat import KSTAT_TYPE_RAW, KSTAT_TYPE_IO, KSTAT_TYPE_NAMED 

class SunOSDiskStatModuleTest(testsunos.AbstractSunOSTest):
    
    def setUp(self):
        self._mock_kstat_start_patch()

    def tearDown(self):
        self._mock_kstat_stop_patch()

    @patch('facet.utils.get_mounts')
    def test_get_mounts(self, mock_utils):
        module = self.get_module(facet.modules.FACET_MODULE_DISK) 
        mock_utils.return_value = [('/', 'zfs', 'dev=1f10002', 'rpool/ROOT/solaris', '0'), ('/var', 'zfs', 'rw,devices,setuid,nonbmand,exec,rstchown,xattr,atime,dev=1f10003', 'rpool/ROOT/solaris/var', '1347533822')]
        mounts = module.get_mounts()
        self.assertTrue(len(mounts) > 0)
        self.assertTrue(mounts[0][0] == '/')
        self.assertTrue(mounts[0][1] == 'zfs')
        self.assertTrue(mounts[0][3] == 'rpool/ROOT/solaris')
        mock_utils.assert_called()

    def test_get_mounts_from_fixture(self):
        module = self.get_module(facet.modules.FACET_MODULE_DISK) 
        # TODO: Not sure if this is the right place for this

    @patch('facet.utils.get_physical_disk_path')
    def test_get_disks(self, mock_utils):
        module = self.get_module(facet.modules.FACET_MODULE_DISK) 

        # configure mock for facet.utils.get_physical_disk_path 
        def mock_map_disk(disk, drv):
            disk_map = {'sd0': '/dev/rdsk/c3t0d0s0', 'sd1': '/dev/rdsk/c3t1d0s0'}
            return disk_map[disk]
        mock_utils.side_effect = mock_map_disk

        self.add_mock_kstat_data('sd', '0', 'sd0', 'disk')
        self.add_mock_kstat_data('sd', '1', 'sd1', 'disk')

        # get disks
        disks = module.get_disks()       
        
        self.assertTrue(len(disks) == 2)
        self.assertTrue('c3t0d0s0' in disks)
        self.assertTrue('c3t1d0s0' in disks)
        mock_utils.assert_any_call('sd0', 'sd')
        mock_utils.assert_any_call('sd1', 'sd')
        self._mock_kstat.return_value.retrieve_all.assert_any_call('sd', -1, None)      
        self._mock_kstat.return_value.retrieve_all.assert_any_call('dad', -1, None)      
        self._mock_kstat.return_value.retrieve_all.assert_any_call('ssd', -1, None)      
 
    @patch('kstat.Kstat')
    @patch('facet.utils.get_physical_disk_path')
    def test_get_disk_counters(self, mock_kstat, mock_utils):
        pass
