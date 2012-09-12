# coding=utf-8

"""
The CPUCollector collects CPU utilization metric using facet 
"""

import diamond.collector
import os

from facet import Facet

class CPUCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(CPUCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(CPUCollector, self).get_default_config()
        config.update({
            'enabled':  'True',
            'path':     'cpu'
        })
        return config

    def collect(self):
        """
        Collect cpu stats
        """
        facet = Facet()
       
        # Get individual cpu stats 
        for cpu in range(0, facet.cpu.get_cpu_count()):
            cpu_stats = facet.cpu.get_cpu_counters(cpu)
            for s in cpu_stats.keys():
                # Get Metric Name
                metric_name = '.'.join([str(cpu), s])
                # Publish Metric Derivative
                self.publish(metric_name,
                             self.derivative(metric_name, long(cpu_stats[s]),
                                             facet.cpu.get_cpu_counters_max(s)))
                
        # Get total cpu stats
        total_cpu_stats = facet.cpu.get_cpu_counters()
        for s in total_cpu_stats.keys():
            # Get Metric Name
            metric_name = '.'.join(['total', s])
            # Publish Metric Derivative
            self.publish(metric_name,
                         self.derivative(metric_name, long(total_cpu_stats[s]),
                                         facet.cpu.get_cpu_counters_max(s)))

        return True
