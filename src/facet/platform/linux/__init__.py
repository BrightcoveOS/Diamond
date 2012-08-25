import facet
import facet.modules
import kstat
import kstat.stats.sysinfo
import kstat.stats.cpu 

class LinuxProvider(facet.FacetProvider):

    def __init__(self, **kwargs):
        # Initialize super class
        facet.FacetProvider.__init__(self, **kwargs)
        
        # Initialize Facet modules in this provider
        self._load_provider_modules()
 
    class LinuxLoadAverageModule(facet.modules.LoadAverageModule):

        def __init__(self, **kwargs):
            self._options = kwargs

        def get_load_average(self):
            pass
 
    class LinuxCPUStatModule(facet.modules.CPUStatModule):

        def __init__(self, **kwargs):
            self._options = kwargs
 
        def get_cpu_count(self):
            pass

        def get_cpu_usage(self, cpu=None):
            pass
