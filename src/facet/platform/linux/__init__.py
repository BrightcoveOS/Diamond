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

        _KEYS = [
            'MemTotal',
            'MemFree',
            'Buffers',
            'Cached',
            'Active',
            'Dirty',
            'Inactive',
            'SwapTotal',
            'SwapFree',
            'SwapCached',
            'VmallocTotal',
            'VmallocUsed',
            'VmallocChunk'
        ]

        def _get_memory_stats(self):
        
            if not os.access(self._PROC, os.R_OK):
                raise facet.FacetError("Unable to read: %s" % (self._PROC))

            stats = dict((k,0) for k in self._KEYS) 

            file = open(self._PROC)
            data = file.read()
            file.close()
            for line in data.splitlines():
                try:
                    name, value, units = line.split()
                    name = name.rstrip(':')
                    value = int(value)
                    stats[name] = value 
                except ValueError:
                    continue
            return stats

        def get_memory_usage(self):
            """
            Return memory usage in bytes (total, free, used) 
            """
            stats = self._get_memory_stats()
            memory_total = stats['MemTotal']
            memory_free = stats['MemFree']
            memory_used = memory_total - memory_free
            return (memory_total * 1024, memory_free * 1024, memory_used * 1024) 

        def get_swap_usage(self):
            """
            Return swap usage in bytes (total, free, used) 
            """
            stats = self._get_memory_stats()
            swap_total = stats['SwapTotal']
            swap_free = stats['SwapFree']
            swap_used = swap_total - swap_free
            return (swap_total * 1024, swap_free * 1024, swap_used * 1024) 

    class LinuxDiskStatModule(facet.modules.DiskStatModule):

        _PROC_PARTITIONS = '/proc/partitions'
        _PROC_DISKSTATS = '/proc/diskstats' 

        def get_mounts(self):
            """
            Return a list of mounted filesystems
            """
            raise NotImplementedError() 

        def get_disks(self):
            """
            Return a list of disks
            """
            disks = [] 
            if os.access(self._PROC_PARTITIONS, os.R_OK):
                file = open(self._PROC_PARTITIONS)
                try:
                    for line in file:
                        try:
                            # major minor  #blocks  name
                            columns = line.split()
                            if len(columns) < 4:
                                continue
                            major = int(columns[0])
                            minor = int(columns[1])
                            device = columns[3]
                            if device != "name":
                                disks.append(device)
                        except ValueError:
                            continue
                finally:
                    file.close()      
            return disks

        def _get_disk_stats(self):
            """
            Create a map of disks in the machine.

            http://www.kernel.org/doc/Documentation/iostats.txt

            Returns:
              device -> (major, minor, DiskStatistics(...))
            """
            result = {}
            if os.access(self._PROC_DISKSTATS, os.R_OK):
                file = open(self._PROC_DISKSTATS)

                for line in file:
                    try:
                        columns = line.split()
                        # On early linux v2.6 versions, partitions have only 4
                        # output fields not 11. From linux 2.6.25 partitions have
                        # the full stats set.
                        if len(columns) < 14:
                            continue
                        major = int(columns[0])
                        minor = int(columns[1])
                        device = columns[2]

                        if device.startswith('ram') or device.startswith('loop'):
                            continue

                        result[device] = (major, minor, {
                            'reads': float(columns[3]),
                            'reads_merged': float(columns[4]),
                            'reads_sectors': float(columns[5]),
                            'reads_milliseconds': float(columns[6]),
                            'writes': float(columns[7]),
                            'writes_merged': float(columns[8]),
                            'writes_sectors': float(columns[9]),
                            'writes_milliseconds': float(columns[10]),
                            'io_in_progress': float(columns[11]),
                            'io_milliseconds': float(columns[12]),
                            'io_milliseconds_weighted': float(columns[13])
                        })
                    except ValueError:
                        continue
                file.close()
            return result       
 
        def get_disk_counters(self, disk):
            """
            Return a dict of disk stat counters for the specified disk
            """
            disk_stats = self._get_disk_stats()
            try:
                return disk_stats[disk][2] 
            except KeyError:
                raise facet.FacetError("Unknown disk: %s" % disk) 
 
        def get_disk_counters_max(self, disk, counter):
            """
            Return the max value for a disk usage counter
            """
            raise NotImplementedError()

        def get_disk_usage(self, disk):
            raise NotImplementedError()
        
