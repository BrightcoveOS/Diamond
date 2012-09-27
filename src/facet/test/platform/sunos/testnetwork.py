import unittest
from mock import Mock, MagicMock
from mock import patch

import testfacet
import testsunos

import facet
import facet.modules

class SunOSNetworkStatModuleTest(testsunos.AbstractSunOSTest):
    
    def setUp(self):
        self._mock_kstat_start_patch()

    def tearDown(self):
        self._mock_kstat_stop_patch()

    def test_get_interfaces(self):
        module = self.get_module(facet.modules.FACET_MODULE_NETWORK) 

        self.add_mock_kstat_data('link', '0', 'net0', 'net')
        self.add_mock_kstat_data('lo', '0', 'lo0', 'net')

        # get interfaces 
        interfaces = module.get_interfaces() 
        
        self.assertTrue(len(interfaces) == 2)
        self.assertTrue('net0' in interfaces)
        self.assertTrue('lo0' in interfaces)
        self._mock_kstat.return_value.retrieve_all.assert_any_call('link', -1, None)      
        self._mock_kstat.return_value.retrieve_all.assert_any_call('lo', -1, None)     

    def test_get_interface_counters(self):
        module = self.get_module(facet.modules.FACET_MODULE_NETWORK) 

        net0_test_data =   {'brdcstrcv': 0L,
                            'brdcstxmt': 886L,
                            'collisions': 0L,
                            'ierrors': 0L,
                            'ifspeed': 1000000000L,
                            'ipackets': 554083L,
                            'ipackets64': 554083L,
                            'link_duplex': 2L,
                            'link_state': 1L,
                            'multircv': 0L,
                            'multixmt': 3007L,  
                            'norcvbuf': 0L,
                            'noxmtbuf': 0L,
                            'obytes': 69178803L,
                            'obytes64': 69178803L,
                            'oerrors': 0L,
                            'opackets': 402261L,
                            'opackets64': 402261L,
                            'rbytes': 45784577L,
                            'rbytes64': 45784577L}

        self.add_mock_kstat_data('link', '0', 'net0', 'net', data=net0_test_data, data_count=len(net0_test_data))
        self.add_mock_kstat_data('lo', '0', 'lo0', 'net', data={'opackets': 12345, 'ipackets': 67890})

        # get interface counters
        interface_counters = module.get_interface_counters('net0')

        self.assertTrue(interface_counters['ipackets64'] == 554083L)       
        self.assertTrue(interface_counters['opackets64'] == 402261L)       
 
        self._mock_kstat.return_value.retrieve_all.assert_any_call('link', -1, None)      
        self._mock_kstat.return_value.retrieve_all.assert_any_call('lo', -1, None)    

        # get interface counters
        interface_counters = module.get_interface_counters('lo0')

        self.assertTrue(interface_counters['opackets'] == 12345L)
        self.assertTrue(interface_counters['ipackets'] == 67890L)
