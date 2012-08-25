import facet

FACET_MODULE_LOADAVG = 'loadavg'
FACET_MODULE_CPU = 'cpu'
FACET_MODULE_MEMORY = 'memory'
FACET_MODULE_NETWORK = 'network'

class LoadAverageModule(facet.FacetModule):
    
    def get_module_type(self):
        return FACET_MODULE_LOADAVG 
    
    def get_load_average(self):
        """
        Return a tuple of (1 min load, 5 min load, 15 min load, total processes, running processes)
        """
        raise NotImplementedError() 
    
class CPUStatModule(facet.FacetModule):

    def get_module_type(self):
        return FACET_MODULE_CPU

    def get_cpu_count(self):
        """
        Return the number of cpu's in the system
        """
        raise NotImplementedError() 

    def get_cpu_usage(self, cpu=None):
        """
        Return a dict of cpu usage
        """
        raise NotImplementedError() 

class MemoryStatModule(facet.FacetModule):

    def get_module_type(self):
        return FACET_MODULE_MEMORY

class NetworkStatModule(facet.FacetModule):
    
    def get_module_type(self):
        return FACET_MODULE_NETWORK
