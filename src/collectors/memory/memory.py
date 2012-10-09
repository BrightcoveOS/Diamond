# coding=utf-8

"""
This class collects data on memory utilization
"""

import diamond.collector
import diamond.convertor
import os

from facet import Facet

class MemoryCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(MemoryCollector, self).get_default_config_help()
        config_help.update({
            'detailed': 'Set to True to Collect all the nodes',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(MemoryCollector, self).get_default_config()
        config.update({
            'enabled':  'True',
            'path':     'memory',
            'method':   'Threaded',
            # Collect all the nodes or just a few standard ones?
            # Uncomment to enable
            #'detailed': 'True'
        })
        return config

    def collect(self):
        """
        Collect memory stats
        """
        facet = Facet()

        # Collect basic memory stats
        stats = dict()
        memory_total, memory_free, memory_used = facet.memory.get_memory_usage()
        swap_total, swap_free, swap_used = facet.memory.get_swap_usage() 
        stats['used'] = memory_used 
        stats['total'] = memory_total 
        stats['free'] = memory_free 
        stats['swap.used'] = swap_used 
        stats['swap.total'] = swap_total 
        stats['swap.free'] = swap_free 

        for name, value in stats.items():
            for unit in self.config['byte_unit']:
                value = diamond.convertor.binary.convert(value=value,
                                                         oldUnit='byte',
                                                         newUnit=unit)
                self.publish(name, value)
       
        # Optionally collect detailed memory stats
        if 'detailed' in self.config:
            # TODO: Detailed memory stats? 
            pass

        return True
