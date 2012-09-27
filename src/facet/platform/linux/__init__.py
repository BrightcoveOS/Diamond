import platform
import re
import os

import facet
import facet.modules

if platform.architecture()[0] == '64bit':
    MAX_COUNTER = (2 ** 64) - 1
else:
    MAX_COUNTER = (2 ** 32) - 1

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
            load_1m = None
            load_5m = None
            load_15m = None
            processes_running = None
            processes_total = None 
 
            if not os.access(self._PROC, os.R_OK):
                raise facet.FacetError("Unable to read: %s" % (self._PROC))

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

        _PROC = '/proc/stat'

        _MAX_VALUES = {
            'user': MAX_COUNTER,
            'nice': MAX_COUNTER,
            'system': MAX_COUNTER,
            'idle': MAX_COUNTER,
            'iowait': MAX_COUNTER,
            'irq': MAX_COUNTER,
            'softirq': MAX_COUNTER,
            'steal': MAX_COUNTER,
            'guest': MAX_COUNTER,
            'guest_nice': MAX_COUNTER,
        }

        def __init__(self, **kwargs):
            self._options = kwargs

        def _get_cpu_stats(self):
            """
            Return cpu stats from '/proc/stat'            
            """
            
            # Check access file 
            if not os.access(self._PROC, os.R_OK):
                raise facet.FacetError("Unable to read: %s" % (self._PROC))

            results = {}

            # Open file
            file = open(self._PROC)

            for line in file:
                if not line.startswith('cpu'):
                    continue

                elements = line.split()
                
                cpu = elements[0]
                if cpu == 'cpu':
                    cpu = 'total'

                results[cpu] = {}

                if len(elements) >= 2:
                    results[cpu]['user'] = elements[1]
                if len(elements) >= 3:
                    results[cpu]['nice'] = elements[2]
                if len(elements) >= 4:
                    results[cpu]['system'] = elements[3]
                if len(elements) >= 5:
                    results[cpu]['idle'] = elements[4]
                if len(elements) >= 6:
                    results[cpu]['iowait'] = elements[5]
                if len(elements) >= 7:
                    results[cpu]['irq'] = elements[6]
                if len(elements) >= 8:
                    results[cpu]['softirq'] = elements[7]
                if len(elements) >= 9:
                    results[cpu]['steal'] = elements[8]
                if len(elements) >= 10:
                    results[cpu]['guest'] = elements[9]
                if len(elements) >= 11:
                    results[cpu]['guest_nice'] = elements[10]

            # Close File
            file.close()

            return results

        def get_cpu_count(self):
            """
            Return the number of cpu's in the system
            """
            cpu_stats = self._get_cpu_stats()
            return len(cpu_stats) - 1

        def get_cpu_counters(self, cpu=None):
            """
            Return a dict of cpu usage counters
            
            Arguments:
            cpu -- return count for the given cpu, or total cpu if none
            """
            cpu_stats = self._get_cpu_stats()
            if cpu_stats:
                if cpu is not None:
                    if cpu < 0 or cpu >= self.get_cpu_count(): 
                        raise facet.FacetError("Unknown cpu: %d" % int(cpu)) 
                    return cpu_stats["cpu%d" % (cpu)]
                else:
                    return cpu_stats['total']
            else:
                return None
 
        def get_cpu_counters_max(self, counter):
            """
            Return the max value for a cpu usage counter
            """
            return self._MAX_VALUES[counter]
    
    class LinuxMemoryStatModule(facet.modules.MemoryStatModule):

        _PROC = '/proc/meminfo'
    
        def get_memory_used(self):
            """
            Return the amount of memory in bytes that is in use 
            """
            raise NotImplementedError() 

        def get_memory_total(self):
            """
            Return the amount of memory in bytes is available
            """
            raise NotImplementedError() 

        def get_memory_free(self):
            """
            Return the amount of memory in bytes that is not in use
            """
            raise NotImplementedError() 

        def get_swap_used(self):
            """
            Return the amount of swap in bytes that is in use
            """
            raise NotImplementedError() 

        def get_swap_total(self):
            """
            Return the amount of swap in bytes that is available
            """
            raise NotImplementedError() 

        def get_swap_free(self):
            """
            Return the amount of swap in bytes that is not in use
            """
            raise NotImplementedError() 
