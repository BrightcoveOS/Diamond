import facet

FACET_MODULE_LOADAVG = 'loadavg'
FACET_MODULE_CPU = 'cpu'
FACET_MODULE_MEMORY = 'memory'
FACET_MODULE_NETWORK = 'network'

class LoadAverageModule(facet.FacetModule):
    
    def get_module_type(self):
        return FACET_MODULE_LOADAVG 
    
    def get_load_average(self):
        pass
    
    def get_running_processes(self):
        pass

    def get_total_processes(self):
        pass

class CPUStatModule(facet.FacetModule):

    def get_module_type(self):
        return FACET_MODULE_CPU

    def get_cpu_count(self):
        pass

    def get_cpu_usage(self, cpu=None):
        pass

class MemoryStatModule(facet.FacetModule):

    def get_module_type(self):
        return FACET_MODULE_MEMORY

class NetworkStatModule(facet.FacetModule):
    
    def get_module_type(self):
        return FACET_MODULE_NETWORK
