#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from diamond.collector import Collector
from memory import MemoryCollector

################################################################################


class TestMemoryCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('MemoryCollector', {
            'interval': 10,
            'byte_unit': 'kilobyte'
        })

        self.collector = MemoryCollector(config, None)
    
    @patch.object(Collector, 'publish')
    @patch('memory.Facet')
    def test_should_work_with_mock_facet_data(self, facet_mock, publish_mock):
 
        # Mock cpu counter data 
        facet_mock.return_value.memory.get_memory_usage.return_value = (2048, 4098, 8192)
        facet_mock.return_value.memory.get_swap_usage.return_value = (1048576, 1048576, 1048576)

        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'total': 2,
            'free': 4,
            'used': 8,
            'swap.total': 1024,
            'swap.free': 1024,
            'swap.used': 1024,
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
