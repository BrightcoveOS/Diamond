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
from cpu import CPUCollector

################################################################################


class TestCPUCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('CPUCollector', {
            'interval': 10
        })

        self.collector = CPUCollector(config, None)

    @patch.object(Collector, 'publish')
    @patch('cpu.Facet')
    def test_should_work_with_mock_facet_data(self, facet_mock, publish_mock):
 
        # Mock cpu counter data 
        facet_mock.return_value.cpu.get_cpu_counters.return_value = {'idle': 100, 'iowait': 200, 'system': 300, 'nice': 400, 'user': 500}
        facet_mock.return_value.cpu.get_cpu_count.return_value = 1 

        self.collector.collect()

        # Increment cpu counters data 
        facet_mock.return_value.cpu.get_cpu_counters.return_value = {'idle': 200, 'iowait': 400, 'system': 600, 'nice': 800, 'user': 1000}

        self.assertPublishedMany(publish_mock, {})

        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'total.idle': 10,
            'total.iowait': 20,
            'total.system': 30, 
            'total.nice': 40,
            'total.user': 50 
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
