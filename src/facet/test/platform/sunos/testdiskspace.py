import unittest
from mock import Mock
from mock import patch

import testfacet
import testsunos

import facet
import facet.modules

class SunOSDiskStatModuleTest(testsunos.AbstractSunOSTest):

    @patch('facet.utils.get_mounts')
    def test_get_mounts(self, mock_utils):
        module = self.get_module(facet.modules.FACET_MODULE_DISK) 
        mock_utils.return_value = [('/', 'zfs', 'dev=1f10002', 'rpool/ROOT/solaris', '0'), ('/var', 'zfs', 'rw,devices,setuid,nonbmand,exec,rstchown,xattr,atime,dev=1f10003', 'rpool/ROOT/solaris/var', '1347533822')]
        mounts = module.get_mounts()
        self.assertTrue(len(mounts) > 0)
        self.assertTrue(mounts[0][0] == '/')
        self.assertTrue(mounts[0][1] == 'zfs')
        self.assertTrue(mounts[0][3] == 'rpool/ROOT/solaris')

    def test_get_mounts_from_fixture(self):
        module = self.get_module(facet.modules.FACET_MODULE_DISK) 
        # TODO: Not sure if this is the right place for this

    @patch('kstat.Kstat')
    #@patch('facet.utils.get_physical_device_path')
    def test_get_disks(self, mock_kstat):
        module = self.get_module(facet.modules.FACET_MODULE_DISK) 
        
        #with patch('kstat.KstatIOData', spec=True) as MockKstatIOData:
        #    mock_kstat_data = MockKstatIOData.return_value
        #    mock_kstat_data.__getitem__
        #    mock_kstat_results = testsunos.MockKstatResults()
        #    mock_kstat_results.set_stats('sd', 0, 'sd0', {})
        #    mock_kstat_results.set_stats('sd', 1, 'sd1', {}) 
        #    mock_kstat.return_value.retrieve_all.side_effect = mock_kstat_results.retrieve_all_stats
        #    print module.get_disks()
        #    print mock_kstat_data 
       

    def test_get_disks_counters(self):
        module = self.get_module(facet.modules.FACET_MODULE_DISK) 
