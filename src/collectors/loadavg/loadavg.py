# coding=utf-8

"""
Uses /proc/loadavg to collect data on load average

#### Dependencies

 * /proc/loadavg

"""

import diamond.collector
from facet import Facet

class LoadAverageCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(LoadAverageCollector,
                            self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(LoadAverageCollector, self).get_default_config()
        config.update({
            'enabled':  'True',
            'path':     'loadavg',
            'method':   'Threaded'
        })
        return config

    def collect(self):
        facet = Facet()
        load_1m, load_5m, load_15m, processes_total, processes_running = facet.loadavg.get_load_average()
        self.publish('01', float(load_1m), 2)
        self.publish('05', float(load_5m), 2)
        self.publish('15', float(load_15m), 2)
        self.publish('processes_running', int(processes_running))
        self.publish('processes_total',   int(processes_total))
