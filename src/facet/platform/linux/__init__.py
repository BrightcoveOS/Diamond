import facet
import facet.modules
import re
import os

class LinuxProvider(facet.FacetProvider):

    def __init__(self, **kwargs):
        # Initialize super class
        facet.FacetProvider.__init__(self, **kwargs)
        
        # Initialize Facet modules in this provider
        self._load_provider_modules()
 
    class LinuxLoadAverageModule(facet.modules.LoadAverageModule):
        
        _RE = re.compile(r'([\d.]+) ([\d.]+) ([\d.]+) (\d+)/(\d+)')

        _PROC = '/proc/loadavg'

        def __init__(self, **kwargs):
            self._options = kwargs

        def get_load_average(self):
            if not os.access(self.PROC, os.R_OK):
                return None
            file = open(self._PROC)
            for line in file:
                match = self._RE.match(line)
                if match:
                    load_1m = float(match.group(1))
                    load_5m = float(match.group(2))
                    load_15m = float(match.group(3))
                    processes_running = int(match.group(4)) 
                    processes_total = int(match.group(5))
            file.close()
            return (load_1m, load_5m, load_15m, processes_total, processes_running) 
 
    class LinuxCPUStatModule(facet.modules.CPUStatModule):

        def __init__(self, **kwargs):
            self._options = kwargs
 
        def get_cpu_count(self):
            pass

        def get_cpu_usage(self, cpu=None):
            pass
