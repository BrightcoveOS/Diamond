import facet
import facet.modules
import kstat
import kstat.stats.sysinfo
import kstat.stats.cpu 

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
            # kstat metric: unix:0:system_misc:ncpu 
            system_misc = self._kstat.retrieve('unix', 0, 'system_misc')
            ncpus = system_misc['ncpus'] 
            return ncpus

        def get_cpu_usage(self, cpu=None):
            usage = {'idle': 0L, 'system':0L, 'user':0L, 'iowait':0L} 
            if cpu:
                return self._get_cpu_stats(cpu)     
            else: 
                for c in range(0, self.get_cpu_count()):
                    cpu_usage = self._get_cpu_stats(c)
                    usage['idle'] += cpu_usage['idle']
                    usage['system'] += cpu_usage['system']
                    usage['user'] += cpu_usage['user']
                    usage['iowait'] += cpu_usage['iowait']
            return usage 

        def _get_cpu_stats(self, cpu):
            # kstat metric: cpu:*:sys
            if cpu < 0 or cpu >= self.get_cpu_count(): 
                raise Exception("Unknown cpu: %d" % cpu) 
            usage = {}
            cpu_stat = self._kstat.retrieve('cpu', cpu, 'sys')
            usage['idle'] = cpu_stat['cpu_ticks_idle']
            usage['system'] = cpu_stat['cpu_ticks_kernel']
            usage['user'] = cpu_stat['cpu_ticks_user'] 
            usage['iowait'] = cpu_stat['cpu_ticks_wait']
            return usage 

    class SunOSMemoryStatModule(facet.modules.MemoryStatModule):
        pass

