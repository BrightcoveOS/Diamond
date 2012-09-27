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

from facet import Facet
from diamond.collector import Collector
from loadavg import LoadAverageCollector

################################################################################


class TestLoadAverageCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('LoadAverageCollector', {
            'interval': 10
        })
        self.collector = LoadAverageCollector(config, None)

    @patch.object(Collector, 'publish')
    @patch('loadavg.Facet')
    def test_should_work_with_mock_facet_data(self, facet_mock, publish_mock):

        # Mock load average data in Facet
        facet_mock.return_value.loadavg.get_load_average = Mock(return_value=(56, 93, 0.1, 5, 10))
       
        # Collect using mock Facet 
        self.collector.collect()
    
        # Assert mock Facet data was published 
        self.assertPublishedMany(publish_mock, {
            '01': 56,
            '05': 93,
            '15': 0.1,
            'processes_total': 5.0, 
            'processes_running': 10.0
        })

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_facet_data(self, publish_mock):

        # Collect using real Facet
        self.collector.collect()
        
        # Assert real Facet data was published
        self.assertPublishedAny(publish_mock, '01')
        self.assertPublishedAny(publish_mock, '05')
        self.assertPublishedAny(publish_mock, '15')
        self.assertPublishedAny(publish_mock, 'processes_total')
        self.assertPublishedAny(publish_mock, 'processes_running')

################################################################################
if __name__ == "__main__":
    unittest.main()
