from mock import Mock, MagicMock
from mock import patch
import unittest

import testfacet

import facet.platform.sunos

class MockKstatResults(object):
    
    def __init__(self):
        self._stats = {}

    def set_stats(self, module, instance, name, stats):
        self._stats[(module, instance, name)] = stats 

    def retrieve_stats(self, module, instance, name):
        return self._stats[(module, instance, name)] 

    def retrieve_all_stats(self, module, instance, name):
        return self._stats.values() 

class AbstractSunOSTest(testfacet.AbstractFacetModuleTest):

    def _mock_kstat_start_patch(self):
        self._kstat_patch = patch('kstat.Kstat')
        self._mock_kstat = self._kstat_patch.start()
        self._mock_kstat_instance = self._mock_kstat.return_value
        self._mock_kstat_instance.retrieve.side_effect = self._mock_kstat_retrieve
        self._mock_kstat_instance.retrieve_all.side_effect = self._mock_kstat_retrieve_all
        self._mock_kstat_instance_data = []

    def _mock_kstat_stop_patch(self): 
        self._kstat_patch.stop()
    
    def _mock_kstat_retrieve(self, mod, inst, name):
        for d in self._mock_kstat_instance_data:
            if mod != None:
                if mod != d.module:
                    continue
            if inst != -1:
                if inst != d.instance:
                    continue
            if name != None:
                if name != d.name:
                    continue
            return d 

    def _mock_kstat_retrieve_all(self, mod, inst, name):
        for d in self._mock_kstat_instance_data:
            if mod != None:
                if mod != d.module:
                    continue
            if inst != -1:
                if inst != d.instance:
                    continue
            if name != None:
                if name != d.name:
                    continue
            yield d 

    def add_mock_kstat_data(self, mod, inst, name, data_class=None, data_type=None, data_count=None, data=None):
        mock_kstat_data = self.build_mock_kstat_data(mod, inst, name, data_class, data_type, data_count, data)
        self._mock_kstat_instance_data.append(mock_kstat_data())

    def build_mock_kstat_data(self, mod, inst, name, data_class, data_type, data_count, data):

        def mock_kstat_data_getitem(k):
            return data[k]

        mock_kstat_data = MagicMock(name='kstat.KstatData')
        mock_kstat_data_instance = mock_kstat_data.return_value
        mock_kstat_data_instance.module = mod 
        mock_kstat_data_instance.instance = inst
        mock_kstat_data_instance.name = name
        mock_kstat_data_instance.data_class = data_class
        mock_kstat_data_instance.data_type = data_type
        mock_kstat_data_instance.data_count = data_count
        mock_kstat_data_instance.data = data
        mock_kstat_data_instance.__getitem__.side_effect = mock_kstat_data_getitem
        return mock_kstat_data

    def get_platform_provider(self):
        return facet.platform.sunos.SunOSProvider 
    
