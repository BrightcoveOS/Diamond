import os
import sys
import re
import shlex
import subprocess
import resource

import kstat
import kstat.stats

import facet
import facet.modules

from facet.platform.sunos.native.utils import *
    
MAX_COUNTER_UINT64 = (2 ** 64) - 1

class SunOSProvider(facet.FacetProvider):

    def __init__(self, **kwargs):
        # Initialize super class
        facet.FacetProvider.__init__(self, **kwargs)
        
        # Initialize Facet modules in this provider
        self._load_provider_modules()
 
    class SunOSLoadAverageModule(facet.modules.LoadAverageModule):

        def __init__(self, **kwargs):
            self._options = kwargs
            self._kstat = kstat.Kstat()

        def get_load_average(self):
            # kstat metric unix:0:system_misc:*
            # NB: load avg values stored a uint32_t and must be scaled by 256 to floating points
            system_misc = self._kstat.retrieve('unix', 0, 'system_misc')
            load_1m = system_misc['avenrun_1min']/256.0
            load_5m = system_misc['avenrun_5min']/256.0
            load_15m = system_misc['avenrun_15min']/256.0
            processes_total = system_misc['nproc']
            processes_running = 0
            return (load_1m, load_5m, load_15m, processes_total, processes_running) 
 
    class SunOSCPUStatModule(facet.modules.CPUStatModule):
        
        _MAX_VALUES = {
            'user': MAX_COUNTER_UINT64, 
            'system': MAX_COUNTER_UINT64, 
            'idle': MAX_COUNTER_UINT64, 
            'iowait': MAX_COUNTER_UINT64 
        }

        def __init__(self, **kwargs):
            self._options = kwargs
            self._kstat = kstat.Kstat()       
 
        def get_cpu_count(self):
            """
            Return the number of cpu's in the system
            """
            # kstat metric: unix:0:system_misc:ncpu 
            system_misc = self._kstat.retrieve('unix', 0, 'system_misc')
            ncpus = system_misc['ncpus'] 
            return ncpus

        def get_cpu_counters(self, cpu=None):
            """
            Return a dict of cpu usage counters 
            """
            usage = {'idle': 0L, 'system':0L, 'user':0L, 'iowait':0L} 
            if cpu:
                return self._get_cpu_counters(cpu)     
            else: 
                for c in range(0, self.get_cpu_count()):
                    cpu_usage = self._get_cpu_counters(c)
                    usage['idle'] += cpu_usage['idle']
                    usage['system'] += cpu_usage['system']
                    usage['user'] += cpu_usage['user']
                    usage['iowait'] += cpu_usage['iowait']
            return usage 

        def _get_cpu_counters(self, cpu):
            # kstat metric: cpu:*:sys
            if cpu < 0 or cpu >= self.get_cpu_count(): 
                raise facet.FacetError("Unknown cpu: %d" % cpu) 
            usage = {}
            kstat_cpu_stat = self._kstat.retrieve('cpu', cpu, 'sys')
            usage['idle'] = kstat_cpu_stat['cpu_ticks_idle']
            usage['system'] = kstat_cpu_stat['cpu_ticks_kernel']
            usage['user'] = kstat_cpu_stat['cpu_ticks_user'] 
            usage['iowait'] = kstat_cpu_stat['cpu_ticks_wait']
            return usage 
        
        def get_cpu_counters_max(self, counter):
            """
            Return the max value for a cpu usage counter
            """
            return self._MAX_VALUES[counter]

    class SunOSMemoryStatModule(facet.modules.MemoryStatModule):

        _SWAP_COMMAND = '/usr/sbin/swap'
        _SWAP_COMMAND_RE = re.compile(r'([A-Za-z0-9/]+)\s(.+)\s([0-9]+)K\s([0-9]+)K\s([0-9]+)K')
 
        def __init__(self, **kwargs):
            self._options = kwargs 
            self._kstat = kstat.Kstat()
            self._last_swap_used_timestamp = 0
            self._last_swap_used = 0 
            self._last_swap_total_timestamp = 0
            self._last_swap_total = 0 
            self._last_swap_free_timestamp = 0
            self._last_swap_free = 0 

        def _get_installed_pages(self):
            self._kstat.update()
            # kstat metric: lgrp:*:*
            installed_pages = 0L
            # Total installed pages can be obtained by summing installed_pages for all locality groups
            for kstat_lgrp in self._kstat.retrieve_all('lgrp', -1, None):
                installed_pages += kstat_lgrp['pages installed']
            return installed_pages

        def get_memory_used(self):
            """
            Return the amount of memory in bytes that is in use 
            """
            self._kstat.update()
            kstat_system_pages = self._kstat.retrieve('unix', -1, 'system_pages')
            total_pages = self._get_installed_pages()
            free_pages = kstat_system_pages['freemem']
            used_pages = total_pages - free_pages 
            return used_pages * resource.getpagesize() 

        def get_memory_total(self):
            """
            Return the amount of memory in bytes is available
            """
            self._kstat.update()
            total_pages = self._get_installed_pages()
            return total_pages * resource.getpagesize() 

        def get_memory_free(self):
            """
            Return the amount of memory in bytes that is not in use
            """
            self._kstat.update()
            kstat_system_pages = self._kstat.retrieve('unix', -1, 'system_pages')
            free_pages = kstat_system_pages['freemem']
            return free_pages * resource.getpagesize() 

        def _run_swap_command(self):
            """
            Execute the swap command and return swaplo, blocks and free
            """
            # Ensure swap command is executable
            if not os.access(self._SWAP_COMMAND, os.X_OK):
                raise FacetError("Unable to execute: %s." % (self._SWAP_COMMAND))

            # Execute swap command
            command = "%s -lk" % (self._SWAP_COMMAND)
            p = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
            (stdout, stderr) = p.communicate()
            if not p or p.returncode != 0:
                raise facet.FacetError("Failed to execute: %s" % command)

            # Parse swap command output
            result = None
            for line in stdout.split('\n'):
                match = self._SWAP_COMMAND_RE.match(line)
                if match:
                    result = (int(match.group(3)), int(match.group(4)), int(match.group(5)))
            return result

        def get_swap_used(self):
            """
            Return the amount of swap in bytes that is in use
            """
            swap_low, swap_total, swap_free = self._run_swap_command()
            return ((swap_total - swap_free) * 1024)
 
        def get_swap_total(self):
            """
            Return the amount of swap in bytes that is available
            """
            swap_low, swap_total, swap_free = self._run_swap_command()
            return (swap_total * 1024) 

        def get_swap_free(self):
            """
            Return the amount of swap in bytes that is not in use
            """
            swap_low, swap_total, swap_free = self._run_swap_command()
            return (swap_free * 1024) 

    class SunOSDiskStatModule(facet.modules.DiskStatModule):

        def get_disks(self):
            print native.utils.get_mounts()
            print native.utils.get_physical_device_path("sd0", "sd")

        def get_disk_space_total(self, disk):
            raise NotImplementedError() 

        def get_disk_space_used(self, disk):
            raise NotImplementedError() 

        def get_disk_space_free(self, disk):
            raise NotImplementedError() 
