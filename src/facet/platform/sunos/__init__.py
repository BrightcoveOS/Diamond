import resource
import facet
import facet.modules
import kstat
import kstat.stats

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

    class SunOSMemoryStatModule(facet.modules.MemoryStatModule):
   
        def __init__(self, **kwargs):
            self._options = kwargs 
            self._kstat = kstat.Kstat()
            self._last_swap_used_timestamp = 0
            self._last_swap_used = 0 
            self._last_swap_total_timestamp = 0
            self._last_swap_total = 0 

        def _get_installed_pages(self):
            self._kstat.update()
            # kstat metric: lgrp:*:*
            installed_pages = 0L
            # Total installed pages can be obtained by summing installed_pages for all locality groups
            for kstat_lgrp in self._kstat.retrieve_all('lgrp', -1, None):
                installed_pages += kstat_lgrp['pages installed']
            return installed_pages

        def get_updates_since_boot(self):
            self._kstat.update()
            kstat_sysinfo = self._kstat.retrieve('unix', -1, 'sysinfo', kstat.stats.sysinfo_t)
            return kstat_sysinfo['updates']

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
 
        def get_swap_used(self):
            """
            Return the amount of swap in bytes that is in use. Returns none if no data is available.
            """
            self._kstat.update()
            kstat_vminfo = self._kstat.retrieve('unix', -1, 'vminfo', kstat.stats.vminfo_t)
            current_swap_used = kstat_vminfo['swap_resv']
            current_timestamp = kstat_vminfo['updates'] 
 
            if self._last_swap_used_timestamp > 0:
                swap_used_bytes = ((current_swap_used - self._last_swap_used) / (current_timestamp - self._last_swap_used_timestamp)) * resource.getpagesize()
            else:
                swap_used_bytes = None

            self._last_swap_used = current_swap_used 
            self._last_swap_used_timestamp = current_timestamp

            return swap_used_bytes 
 
        def get_swap_total(self):
            """
            Return the amount of swap in bytes that is available
            """
            kstat_vminfo = self._kstat.retrieve('unix', -1, 'vminfo', kstat.stats.vminfo_t)
            current_swap_total = kstat_vminfo['swap_free'] - kstat_vminfo['swap_resv']
            current_timestamp = kstat_vminfo['updates'] 
 
            if self._last_swap_total_timestamp > 0:
                swap_total_bytes = ((current_swap_total - self._last_swap_total) / (current_timestamp - self._last_swap_total_timestamp)) * resource.getpagesize()
            else:
                swap_total_bytes = None

            self._last_swap_total = current_swap_total
            self._last_swap_total_timestamp = current_timestamp

            return swap_total_bytes 

        def get_swap_free(self):
            """
            Return the amount of swap in bytes that is not in use
            """
            pass 
       
         

